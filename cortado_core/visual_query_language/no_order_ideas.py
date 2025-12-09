"""
NoOrderGroup: (QUERY ONLY) matches elements in any order (can span sequential and parallel)
- it's a query pattern to find activities regardless of order

Example query: [NoOrderGroup([LeafGroup(['b']), LeafGroup(['c']), LeafGroup(['d'])])](http://vscodecontentref/6) matches:

- [b, c, d] or [d, c, b] (any permutation in sequence)
- ParallelGroup([b, c, d])
- ParallelGroup([b, d]), c (mixed)

"""

from typing import List

from cortado_core.utils.split_graph import (
    Group,
    StartGroup,
    EndGroup,
    ParallelGroup,
    SequenceGroup,
    LeafGroup,
    AnythingGroup,
)
from cortado_core.visual_query_language.matching_functions import match


# Import NoOrderGroup from test file (it's a mockup that extends SequenceGroup)
# We detect it by checking if it's a SequenceGroup subclass but not exactly SequenceGroup
def _is_no_order_group(group: Group) -> bool:
    """Check if group is a NoOrderGroup (subclass of SequenceGroup but not SequenceGroup itself)."""
    return isinstance(group, SequenceGroup) and type(group).__name__ == "NoOrderGroup"


def _dfs_match(
    query_list: List[Group],
    variant_list: List[Group],
    q_idx: int,
    v_idx: int,
    q_end: int,
    must_consume_all: bool,
) -> bool:
    # --- Handle NoOrderGroup: matches elements in any order ---
    # NoOrderGroup is a subclass of SequenceGroup, so check this BEFORE SequenceGroup
    if _is_no_order_group(current_query):
        return _match_no_order_group(
            query_list, variant_list, q_idx, v_idx, q_end, must_consume_all
        )


def _match_no_order_group(
    query_list: List[Group],
    variant_list: List[Group],
    q_idx: int,
    v_idx: int,
    q_end: int,
    must_consume_all: bool,
) -> bool:
    """
    Handle NoOrderGroup matching. NoOrderGroup contains elements that must all
    appear in the variant, but in any order. The elements can be spread across
    sequential positions or inside a ParallelGroup.

    For example, NoOrderGroup([b, c, d]) matches:
    - Sequential: [b, c, d], [c, b, d], [d, c, b], etc.
    - Parallel: ParallelGroup([b, c, d])
    - Mixed: ParallelGroup([b, d]), c

    Args:
        query_list: List of query elements
        variant_list: List of variant elements
        q_idx: Index of the NoOrderGroup in query
        v_idx: Current index in variant
        q_end: Last index in query to match (inclusive)
        must_consume_all: If True, variant must be fully consumed when query ends

    Returns:
        True if NoOrderGroup can be matched and rest of query succeeds
    """
    no_order_group = query_list[q_idx]
    required_elements = list(no_order_group)  # Elements that must all be matched
    num_required = len(required_elements)

    if num_required == 0:
        # Empty NoOrderGroup - just continue
        return _dfs_match(
            query_list, variant_list, q_idx + 1, v_idx, q_end, must_consume_all
        )

    # Try to match all required elements against variant starting at v_idx
    # We need to find how many variant elements to consume
    remaining_variant = len(variant_list) - v_idx

    # We need at least enough variant elements to potentially contain all required
    # But a ParallelGroup can contain multiple, so minimum is 1
    if remaining_variant < 1:
        return False

    # Try consuming different numbers of variant elements
    for consume_count in range(1, remaining_variant + 1):
        variant_slice = variant_list[v_idx : v_idx + consume_count]

        # Collect all leaf activities from the variant slice
        variant_activities = _collect_activities_from_variant(variant_slice)

        # Check if all required elements can be matched
        if _can_match_no_order(required_elements, variant_activities):
            # This consumption works, try to match the rest
            new_v_idx = v_idx + consume_count
            if _dfs_match(
                query_list, variant_list, q_idx + 1, new_v_idx, q_end, must_consume_all
            ):
                return True

    return False


def _collect_activities_from_variant(variant_slice: List[Group]) -> List[str]:
    """
    Collect all leaf activity names from a slice of variant elements.
    Flattens ParallelGroups and SequenceGroups to get all activities.

    Args:
        variant_slice: List of variant elements (LeafGroup, ParallelGroup, SequenceGroup)

    Returns:
        List of activity names found in the slice
    """
    activities = []
    for elem in variant_slice:
        if isinstance(elem, LeafGroup):
            # LeafGroup contains activity name(s)
            activities.extend(list(elem))
        elif isinstance(elem, ParallelGroup):
            # Recursively collect from parallel branches
            activities.extend(_collect_activities_from_variant(list(elem)))
        elif isinstance(elem, SequenceGroup):
            # Recursively collect from sequence elements
            activities.extend(_collect_activities_from_variant(list(elem)))
    return activities


def _can_match_no_order(
    required_elements: List[Group], variant_activities: List[str]
) -> bool:
    """
    Check if all required elements from NoOrderGroup can be found in variant activities.
    Each required element must be matched exactly once (no duplicates, no extras).

    Args:
        required_elements: List of Groups from NoOrderGroup (typically LeafGroups)
        variant_activities: List of activity names from variant

    Returns:
        True if exact match (same activities, same count)
    """
    # Extract required activity names
    required_activities = []
    for elem in required_elements:
        if isinstance(elem, LeafGroup):
            required_activities.extend(list(elem))
        else:
            # For non-leaf elements in NoOrderGroup, we'd need more complex matching
            # For now, assume NoOrderGroup contains only LeafGroups
            return False

    # Check if activities match exactly (same elements, same count)
    # Sort both to compare regardless of order
    return sorted(required_activities) == sorted(variant_activities)
