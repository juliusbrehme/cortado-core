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
    Given a pattern [query] and a variant [variant], checks if the variant matches the query pattern.
    """

    query_sorted = query.sort()
    variant_sorted = variant.sort()

    return match_sequential(query_sorted, variant_sorted)
