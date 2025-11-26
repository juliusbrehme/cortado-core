from cortado_core.utils.split_graph import Group, StartGroup, EndGroup, ParallelGroup
from cortado_core.visual_query_language.matching_functions import match
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


def match_sequential(query: List[Group], variant: List[Group]) -> bool:
    """
    Given a pattern [query] and a variant [variant], checks if the variant matches the query pattern.
    It is expected [variant] as well as [query] are the children of a SequentialGroup.
    """

    if len(query) == 0:
        return True

    has_start_point = isinstance(query[0], StartGroup)
    has_end_point = isinstance(query[-1], EndGroup)

    # Edge case: Query only consists of a start or end point -> matches anything
    if len(query) == 1 and (has_start_point or has_end_point):
        return True

    if has_start_point and not check_start_point(query, variant):
        return False

    if has_end_point and not check_end_point(query, variant):
        return False

    # Walk the query and varianat backwards
    if has_end_point:
        query = query[:-1]
        variant = variant[:-1]

    candidates = []  # Possible candidates with unchecked subproblems
    subproblems = []  # Subproblems/Subtrees of possible candidate for later checking

    idxQuery = 0 + (has_start_point or has_end_point)
    idxVariant = 0

    while idxQuery < len(query) and idxVariant < len(variant):
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
            if idxQuery == len(query):
                # Match must be from start to end -> variant must also be fully consumed
                if has_start_point and has_end_point:
                    if idxVariant == len(variant):
                        candidates.append(subproblems)
                    else:
                        return False

                else:
                    candidates.append(subproblems)
                    subproblems = []

                    idxVariant -= len(query) - has_start_point - has_end_point - 1
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


def match_parallel(query: Group, variant: Group) -> bool:
    """Matches if a parallel group in the variant matches the query parallel group."""

    raise NotImplementedError()
