from cortado_core.utils.split_graph import (
    Group,
    StartGroup,
    EndGroup,
    ParallelGroup,
    SequenceGroup,
    LeafGroup,
)
from cortado_core.visual_query_language.matching_functions import match
from collections import Counter
from typing import List


def check_start_point(query: List[Group], variant: List[Group]) -> bool:
    """Checks if the start point in the variant matches just after the start node in the query."""

    if len(variant) == 0:
        return False

    if not match(query[1], variant[0]):
        return False

    return True


def check_end_point(query: List[Group], variant: List[Group]) -> bool:
    """Checks if the end point in the variant matches just before the end node in the query."""

    if len(variant) == 0:
        return False

    if not match(query[-2], variant[-1]):
        return False

    return True


def match_sequential(query: SequenceGroup, variant: SequenceGroup) -> bool:
    """
    Given a pattern [query] and a variant [variant], checks if the variant matches the query pattern.
    """
    # Cannot use len() because it computes not the elements of the list but the "longest path"
    query_length = query.list_length()
    variant_length = variant.list_length()

    if query_length == 0:
        return True

    has_start_point = isinstance(query[0], StartGroup)
    has_end_point = isinstance(query[-1], EndGroup)

    # Edge case: Query only consists of a start or end point -> matches anything
    if variant_length == 1 and (has_start_point or has_end_point):
        return True

    if has_start_point and not check_start_point(query, variant):
        return False

    if has_end_point and not check_end_point(query, variant):
        return False

    # Walk the query and varianat backwards
    if has_end_point:
        query = SequenceGroup(lst=query[::-1])
        variant = SequenceGroup(lst=variant[::-1])
        query_length = query.list_length()
        variant_length = variant.list_length()

    candidates = []  # Possible candidates with unchecked subproblems
    subproblems = []  # Subproblems/Subtrees of possible candidate for later checking

    idxQuery = 0 + (has_start_point or has_end_point)
    idxVariant = 0

    while idxQuery < query_length and idxVariant < variant_length:
        if not match(query[idxQuery], variant[idxVariant]):
            if idxQuery == 0 + (has_start_point or has_end_point):
                idxVariant += 1
            idxQuery = 0 + (has_start_point or has_end_point)
            subproblems = []

        else:
            # Parallel are treated as subproblems -> only needs to be checked if the sequential parts match
            if isinstance(variant[idxVariant], ParallelGroup):
                subproblems.append((query[idxQuery], variant[idxVariant]))

            idxQuery += 1
            idxVariant += 1

            # End of query reached -> all sequential parts matched -> possible candiate found
            if idxQuery == query_length:
                # Match must be from start to end -> variant must also be fully consumed
                if has_start_point and has_end_point:
                    if idxVariant == variant_length:
                        candidates.append(subproblems)
                    else:
                        return False

                else:
                    candidates.append(subproblems)
                    subproblems = []

                    idxVariant -= query_length - has_start_point - has_end_point - 1
                    idxQuery = 0 + (has_start_point or has_end_point)

                # If start or end point is present, we are done after first match (other candidates would not be aligned to start/end)
                if has_start_point or has_end_point:
                    break

    for candidate in candidates:
        for subquery, subvariant in candidate:
            if not match_parallel(subquery, subvariant):
                break
        else:
            return True

    return False


def match_parallel(query: ParallelGroup, variant: ParallelGroup) -> bool:
    """
    Match a ParallelGroup query against a ParallelGroup variant.

    For parallel matching: every branch in the query must find a matching
    branch in the variant, AND every branch in the variant must be matched.
    This ensures exact structural match (no extra branches in variant).
    Order doesn't matter.

    Uses backtracking DFS to correctly handle overlapping ChoiceGroups where
    a single variant branch could potentially match multiple query branches.

    Args:
        query: ParallelGroup from the query
        variant: ParallelGroup from the variant

    Returns:
        True if query and variant have matching branches (bijective match)
    """
    query_branches = query
    variant_branches = variant

    # Use backtracking to find a valid assignment
    def backtrack(q_idx: int, used: set) -> bool:
        """
        Recursively try to match remaining query branches to unused variant branches.

        Args:
            q_idx: Current query branch index
            used: Set of variant branch indices already assigned

        Returns:
            True if remaining query branches can be matched to remaining variant branches
        """
        # Base case: all query branches have been matched
        if q_idx == len(query_branches):
            # All variant branches should be used (bijective match)
            return len(used) == variant_branches.list_length()

        q_branch = query_branches[q_idx]

        # Try matching this query branch against each unused variant branch
        for v_idx in range(variant_branches.list_length()):
            if v_idx not in used:
                if _branches_match(q_branch, variant_branches[v_idx]):
                    # Found a match, mark it as used and continue
                    used.add(v_idx)
                    if backtrack(q_idx + 1, used):
                        return True
                    # Backtrack: remove from used set and try next variant branch
                    used.remove(v_idx)

        return False

    return backtrack(0, set())


def _branches_match(q_branch: Group, v_branch: Group) -> bool:
    """
    Check if a single query branch matches a single variant branch.

    Args:
        q_branch: A branch from the query ParallelGroup
        v_branch: A branch from the variant ParallelGroup

    Returns:
        True if the branches match
    """
    # Both are SequenceGroups - use sequential matching
    if isinstance(q_branch, SequenceGroup) and isinstance(v_branch, SequenceGroup):
        return match_sequential(q_branch, v_branch)

    # Both are ParallelGroups - recursive parallel matching
    if isinstance(q_branch, ParallelGroup) and isinstance(v_branch, ParallelGroup):
        return match_parallel(q_branch, v_branch)

    # Leaf-level comparison (LeafGroup, ChoiceGroup, WildcardGroup, etc.)
    # Use match() from matching_functions.py
    return match(q_branch, v_branch)
