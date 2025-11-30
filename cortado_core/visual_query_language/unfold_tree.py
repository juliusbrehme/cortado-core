import copy
import itertools
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
)


# TODO: always add start and end points ParallelGroups
# TODO: test functionality
def unfold_tree(tree_query: Group) -> List[Group]:
    """
    Turns the given query tree into a query tree to be used for filtering a variant.
    Args:
        tree_query: The query given as a tree.

    Returns:
        Group: A tree that is unfolded to be used for filtering.
    """
    children = list(tree_query)
    new_trees: List[List[Group]] = []

    for child, index in enumerate(children):
        if check_leaf(child):
            new_trees = add_to_tree_list(child, new_trees)
        elif type(child) is OptionalGroup:
            new_trees_copy = copy.deepcopy(new_trees)
            unfold_tree_list = unfold_tree(list(child)[0])
            for tree in unfold_tree_list:
                new_trees = add_to_tree_list(tree, new_trees_copy)
            new_trees.extend(new_trees_copy)
        elif type(child) is LoopGroup:
            tree = list(child)[0]
            unfold_tree_list = unfold_tree(tree)
            for tree in unfold_tree_list:
                new_trees = add_to_tree_list(tree, new_trees)
        elif type(child) is SequenceGroup:
            unfold_tree_list = unfold_tree(child)
            for tree in unfold_tree_list:
                new_trees = add_to_tree_list(tree, new_trees)
        elif type(child) is ParallelGroup:
            list_of_unfolded_trees = unfold_tree(child)
            for tree in list_of_unfolded_trees:
                new_trees = add_to_tree_list(tree, new_trees)

        else:
            raise Exception(
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
    elif type(tree_query) is WildcardGroup:
        for list_of_nodes in new_trees:
            list_of_groups.append(WildcardGroup(lst=list_of_nodes))
        return list_of_groups
    elif type(tree_query) is AnythingGroup:
        for list_of_nodes in new_trees:
            list_of_groups.append(AnythingGroup(lst=list_of_nodes))
        return list_of_groups
    elif type(tree_query) is FallthroughGroup:
        for list_of_nodes in new_trees:
            list_of_groups.append(FallthroughGroup(lst=list_of_nodes))
        return list_of_groups
    elif type(tree_query) is LeafGroup:
        for list_of_nodes in new_trees:
            list_of_groups.append(LeafGroup(lst=list_of_nodes))
        return list_of_groups
    else:
        raise Exception(
            f"Unexpected input type {type(tree_query)}. This should never happen."
        )


def add_to_tree_list(node: Group, tree_list: List[List[Group]]) -> List[List[Group]]:
    if len(tree_list) == 0:
        tree_list.append([node])
    for tree in tree_list:
        tree.append(node)
    return tree_list


def check_leaf(node: Group) -> bool:
    if (
        type(node) is LeafGroup
        or type(node) is FallthroughGroup
        or type(node) is WildcardGroup
        or type(node) is AnythingGroup
        or type(node) is ChoiceGroup
    ):
        return True
    else:
        return False
