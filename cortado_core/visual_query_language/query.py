from typing import List

from cortado_core.utils.split_graph import SequenceGroup
from cortado_core.visual_query_language.matching_algorithm import match_sequential
from cortado_core.visual_query_language.unfold_tree import unfold_tree


def start_query(variant: SequenceGroup, query: SequenceGroup) -> bool:
    """
    Starting point of the query.
     Args:
        variant (Group): The variant to be checked.
        query (Group): The query pattern.
    First unfolds the tree and then checks the variants.
    Returns:
        bool: True if one variant matches the query, False otherwise.
    """

    unfolded_tree_list = unfold_tree(query)
    for variant_tree in unfolded_tree_list:
        if check_variant(variant_tree, query):
            return True
    return False


def check_variant(
    variant: SequenceGroup, query: SequenceGroup, activities: List[str] = []
) -> bool:
    """
    Check if the given variant matches the query pattern.

    Args:
        variant (Group): The variant to be checked.
        query (Group): The query pattern.
        activities (List[str]): List of all possible activites in the variant.

    Returns:
        bool: True if the variant matches the query, False otherwise.
    """

    return match_sequential(query, variant)
