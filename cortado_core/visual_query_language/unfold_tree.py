import copy
from typing import List

from cortado_core.utils.split_graph import (
    Group,
    LeafGroup,
    FallthroughGroup,
    WildcardGroup,
    AnythingGroup,
    ChoiceGroup,
    SequenceGroup,
    LoopGroup,
    ParallelGroup,
    OptionalGroup,
    StartGroup,
    EndGroup,
)


def unfold_tree(tree_query: Group | List[Group]) -> List[Group]:
    """
    Turns the given query tree into a query tree to be used for filtering a variant.
    Args:
        tree_query: The query given as a tree.

    Returns:
        Group: A tree that is unfolded to be used for filtering.
    """
    if check_leaf(tree_query):
        return [tree_query]

    tree_query = add_start_end_to_parallel_group(tree_query)

    new_trees: List[List[Group]] = []
    for child in tree_query:
        if check_leaf(child):
            new_trees = add_to_tree_list(child, new_trees)
        elif type(child) is OptionalGroup:
            new_trees_copy = copy.deepcopy(new_trees)
            unfold_tree_list = unfold_tree(child[0])
            for tree in unfold_tree_list:
                new_trees = add_to_tree_list(tree, new_trees)
            new_trees.extend(new_trees_copy)
        elif type(child) is LoopGroup:
            unfold_tree_list = unfold_tree(child[0])
            for _ in range(child.max_count):
                new_trees = merge_and_flatten(new_trees, unfold_tree_list)
        elif type(child) is SequenceGroup:
            unfold_tree_list = unfold_tree(child)
            new_trees = merge_and_flatten(new_trees, unfold_tree_list)
        elif type(child) is ParallelGroup:
            list_of_unfolded_trees = unfold_tree(child)
            new_trees = merge_and_flatten(new_trees, list_of_unfolded_trees)

        else:
            raise TypeError(
                f"Unexpected type {type(child)}. Should be implemented in unfold_tree."
            )
    list_of_groups: List[Group] = []
    if type(tree_query) is ParallelGroup:
        for list_of_nodes in new_trees:
            list_of_groups.append(ParallelGroup(lst=list_of_nodes))
        return list_of_groups

    elif type(tree_query) is SequenceGroup:
        for list_of_nodes in new_trees:
            list_of_groups.append(SequenceGroup(lst=list_of_nodes))
        return list_of_groups
    elif type(tree_query) is list:
        return tree_query
    else:
        raise Exception(
            f"Unexpected input type {type(tree_query)}. This should never happen."
        )


def add_to_tree_list(node: Group, tree_list: List[List[Group]]) -> List[List[Group]]:
    if len(tree_list) == 0:
        tree_list.append([node])
    else:
        for tree in tree_list:
            tree.append(node)
    return tree_list


def add_start_end_to_parallel_group(variant: Group):
    if type(variant) is ParallelGroup:
        for child in variant:
            if type(child) is SequenceGroup:
                child.append(EndGroup())
                child.insert(0, StartGroup())
    return variant


def merge_and_flatten(list1: List[Group], list2: List[Group]) -> List[Group]:
    result: List[Group] = []
    if len(list1) == 0:
        for item2 in list2:
            result.append([item2])
        return result
    for item1 in list1:
        for item2 in list2:
            # wrapped in [], because else the Operator is lost because Group inherits from list
            combine = item1 + [item2]

            result.append(combine)
    return result


def check_leaf(node: Group) -> bool:
    if (
        type(node) is LeafGroup
        or type(node) is FallthroughGroup
        or type(node) is WildcardGroup
        or type(node) is AnythingGroup
        or type(node) is ChoiceGroup
        or type(node) is StartGroup
        or type(node) is EndGroup
    ):
        return True
    else:
        return False
