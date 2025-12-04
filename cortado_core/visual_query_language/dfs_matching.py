"""
DFS-based matching algorithm for visual query language.

This module provides depth-first search based matching of query patterns against
process variants. The query can contain special constructs like:
- LeafGroup: matches a specific activity
- ChoiceGroup: matches any of several activities  
- WildcardGroup: matches any single activity
- AnythingGroup: matches 1 or more consecutive elements (leaves or subtrees)
- ParallelGroup: matches parallel branches (order doesn't matter)
- StartGroup/EndGroup: anchors the match to start/end of variant

The variant only contains: LeafGroup, SequenceGroup, ParallelGroup (nested).

NOTE: LoopGroup and OptionalGroup are handled by unfold_tree.py which expands
them into multiple query variants before this matching code is called.
LoopGroup is unrolled for any number of nested subgroups.
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


def match_sequential(query: SequenceGroup, variant: SequenceGroup) -> bool:
    """
    Main entry point: Check if query pattern exists in variant using DFS.
    
    Args:
        query: The query pattern (SequenceGroup, may contain special groups)
        variant: The variant to search in (SequenceGroup with only Leaf/Sequence/Parallel)
    
    Returns:
        True if query matches somewhere in variant, False otherwise.
    """
    query_list = list(query)
    variant_list = list(variant)
    
    # Handle empty cases
    if len(query_list) == 0:
        return True
    if len(variant_list) == 0:
        return False
    
    # Check for StartGroup and EndGroup anchors
    has_start = isinstance(query_list[0], StartGroup)
    has_end = isinstance(query_list[-1], EndGroup)
    
    # Determine the actual query content (excluding Start/End markers)
    # query_start: first index of actual content
    # query_end: last index of actual content (inclusive)
    query_start = 1 if has_start else 0
    query_end = len(query_list) - 2 if has_end else len(query_list) - 1
    
    # Edge case: query is only StartGroup and/or EndGroup with no content
    if query_start > query_end:
        return True
    
    # If anchored to start, we must begin matching at variant index 0
    if has_start:
        return _dfs_match(
            query_list, variant_list,
            query_start, 0,
            query_end, has_end
        )
    
    # If not anchored to start, try matching from each position in variant
    for variant_start in range(len(variant_list)):
        if _dfs_match(
            query_list, variant_list,
            query_start, variant_start,
            query_end, has_end
        ):
            return True
    
    return False


def _dfs_match(
    query_list: List[Group],
    variant_list: List[Group],
    q_idx: int,
    v_idx: int,
    q_end: int,
    must_consume_all: bool
) -> bool:
    """
    Recursive DFS matching function.
    
    Args:
        query_list: List of query elements
        variant_list: List of variant elements
        q_idx: Current index in query (what we're trying to match)
        v_idx: Current index in variant (where we're looking)
        q_end: Last index in query to match (inclusive)
        must_consume_all: If True, variant must be fully consumed when query ends
    
    Returns:
        True if we can match query[q_idx:q_end+1] against variant starting at v_idx
    """
    # Base case 1: We've matched all query elements
    if q_idx > q_end:
        if must_consume_all:
            # With EndGroup, variant must also be fully consumed
            return v_idx >= len(variant_list)
        else:
            # Without EndGroup, we're done (remaining variant is OK)
            return True
    
    # Base case 2: Variant exhausted but query has more elements
    if v_idx >= len(variant_list):
        # Check if remaining query is all AnythingGroups that could match empty
        # Actually, AnythingGroup needs at least 1 element, so this fails
        return False
    
    current_query = query_list[q_idx]
    current_variant = variant_list[v_idx]
    
    # --- Handle AnythingGroup: matches 1 or more variant elements ---
    if isinstance(current_query, AnythingGroup):
        return _match_anything_group(
            query_list, variant_list,
            q_idx, v_idx,
            q_end, must_consume_all
        )
    
    # --- Handle ParallelGroup in query ---
    if isinstance(current_query, ParallelGroup):
        # Variant element must also be ParallelGroup
        if not isinstance(current_variant, ParallelGroup):
            return False
        
        # Check if the parallel groups match
        if not match_parallel(current_query, current_variant):
            return False
        
        # Continue with next elements
        return _dfs_match(
            query_list, variant_list,
            q_idx + 1, v_idx + 1,
            q_end, must_consume_all
        )
    
    # --- Handle SequenceGroup nested in query ---
    if isinstance(current_query, SequenceGroup):
        # Variant element must also be SequenceGroup
        if not isinstance(current_variant, SequenceGroup):
            return False
        
        # Recursively match the nested sequences
        if not match_sequential(current_query, current_variant):
            return False
        
        # Continue with next elements
        return _dfs_match(
            query_list, variant_list,
            q_idx + 1, v_idx + 1,
            q_end, must_consume_all
        )
    
    # --- Handle leaf-level matching (LeafGroup, ChoiceGroup, WildcardGroup, etc.) ---
    # Use the match() function from matching_functions.py
    if match(current_query, current_variant):
        # Match succeeded, continue to next elements
        return _dfs_match(
            query_list, variant_list,
            q_idx + 1, v_idx + 1,
            q_end, must_consume_all
        )
    
    # No match at this position
    return False


def _match_anything_group(
    query_list: List[Group],
    variant_list: List[Group],
    q_idx: int,
    v_idx: int,
    q_end: int,
    must_consume_all: bool
) -> bool:
    """
    Handle AnythingGroup matching. AnythingGroup matches 1 or more consecutive
    variant elements (can be leaves or entire subtrees).
    
    We try consuming 1 element, then 2, then 3, etc. until we find a valid
    continuation or run out of variant elements.
    
    Args:
        query_list: List of query elements
        variant_list: List of variant elements
        q_idx: Index of the AnythingGroup in query
        v_idx: Current index in variant
        q_end: Last index in query to match (inclusive)
        must_consume_all: If True, variant must be fully consumed when query ends
    
    Returns:
        True if AnythingGroup can be matched and rest of query succeeds
    """
    remaining_variant = len(variant_list) - v_idx
    
    # Try consuming 1, 2, 3, ... elements with AnythingGroup
    # We need at least 1 element for AnythingGroup
    for consume_count in range(1, remaining_variant + 1):
        # After consuming 'consume_count' elements, try to match the rest
        new_v_idx = v_idx + consume_count
        
        if _dfs_match(
            query_list, variant_list,
            q_idx + 1, new_v_idx,
            q_end, must_consume_all
        ):
            return True
    
    # No valid consumption amount worked
    return False


def match_parallel(query: ParallelGroup, variant: ParallelGroup) -> bool:
    """
    Match a ParallelGroup query against a ParallelGroup variant.
    
    For parallel matching: every branch in the query must find a matching
    branch in the variant, AND every branch in the variant must be matched.
    This ensures exact structural match (no extra branches in variant).
    Order doesn't matter.
    
    Args:
        query: ParallelGroup from the query
        variant: ParallelGroup from the variant
    
    Returns:
        True if query and variant have matching branches (bijective match)
    """
    query_branches = list(query)
    variant_branches = list(variant)
    
    # Must have same number of branches for exact match
    if len(query_branches) != len(variant_branches):
        return False
    
    # Track which variant branches have been used
    used = [False] * len(variant_branches)
    
    # For each query branch, find a matching variant branch
    for q_branch in query_branches:
        found_match = False
        
        for i, v_branch in enumerate(variant_branches):
            if used[i]:
                continue  # This variant branch already matched another query branch
            
            if _branches_match(q_branch, v_branch):
                used[i] = True
                found_match = True
                break
        
        if not found_match:
            # This query branch has no matching variant branch
            return False
    
    return True


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
