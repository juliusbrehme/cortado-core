from typing import List

from cortado_core.utils.split_graph import SequenceGroup
# from cortado_core.visual_query_language.matching_algorithm import match_sequential
from cortado_core.visual_query_language.dfs_matching import match_sequential
from cortado_core.visual_query_language.unfold_tree import unfold_tree

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
    # Unfold the query to handle OptionalGroup and LoopGroup
    # This creates multiple query variants (e.g., with and without optional parts)
    unfolded_queries = unfold_tree(query)
    
    # Check if ANY unfolded query matches the variant
    for unfolded_query in unfolded_queries:
        if match_sequential(unfolded_query, variant):
            return True
    
    return False
