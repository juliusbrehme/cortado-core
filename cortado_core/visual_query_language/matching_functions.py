from typing import cast

from cortado_core.utils.split_graph import (
    ChoiceGroup,
    LeafGroup,
    WildcardGroup,
    Group,
    FallthroughGroup,
)


def match(node_query: Group, node_variant: Group) -> bool:
    """
    Checks the two Group have the same type and calls the matching function to compare if both are leafs.
    Else it just checks if the types are the same.
    Args:
        node_query: The Group of the query.
        node_variant: The Group of the variant.

    Returns:
        bool: True if the types are equal or if the leafs match.
    """
    if type(node_query) is ChoiceGroup and type(node_variant) is LeafGroup:
        return match_choice_group_operator(
            cast(ChoiceGroup, node_query), cast(LeafGroup, node_variant)
        )
    elif type(node_query) is WildcardGroup and type(node_variant) is LeafGroup:
        return match_wildcard_group_operator(
            cast(WildcardGroup, node_query), cast(LeafGroup, node_variant)
        )
    elif (
        type(node_query) is FallthroughGroup and type(node_variant) is FallthroughGroup
    ):
        return match_no_order(
            cast(FallthroughGroup, node_query), cast(FallthroughGroup, node_variant)
        )
    elif type(node_query) is LeafGroup and type(node_variant) is LeafGroup:
        return match_leaf_group(
            cast(LeafGroup, node_query), cast(LeafGroup, node_variant)
        )
    elif type(node_query) is type(node_variant):
        # Just check the type, because we can only check the exact match when we encounter two leafs.
        return True
    else:
        return False


def match_leaf_group(leaf_query: LeafGroup, leaf_variant: LeafGroup) -> bool:
    """
    Checks if the two leafs match.
    Args:
        leaf_query: The LeafGroup of the query.
        leaf_variant: The LeafGroup of the variant.

    Returns:
        bool: True if the two leafs match.
    """
    if not type(leaf_query) is LeafGroup and type(leaf_variant) is LeafGroup:
        return False

    if leaf_variant[0] == leaf_query[0]:
        return True
    return False


def match_choice_group_operator(
    node_query: ChoiceGroup, leaf_variant: LeafGroup
) -> bool:
    """
    Checks if the leaf matches one of the children of the choice group.
    Args:
        node_query: The ChoiceGroup of the query.
        leaf_variant: The LeafGroup of the variant.

    Returns:
        bool: True if the leaf_variant matches one of the ChoiceGroup children.
    """
    if not (type(node_query) is ChoiceGroup and type(leaf_variant) is LeafGroup):
        return False

    children = list(node_query)

    for child in children:
        if leaf_variant[0] == child[0]:
            return True
    return False


def match_wildcard_group_operator(
    leaf_query: WildcardGroup, leaf_variant: LeafGroup
) -> bool:
    """
    Checks if the leaf_variant can match the wildcard group.
    Args:
        leaf_query: The WildcardGroup of the query.
        leaf_variant: The LeafGroup of the variant.

    Returns:
        bool: True if the leaf_variant matches the wildcard group.
    """
    if not (type(leaf_query) is WildcardGroup and type(leaf_variant) is LeafGroup):
        return False
    return True


def match_no_order(
    node_query: FallthroughGroup, node_variant: FallthroughGroup
) -> bool:
    """
        Checks if the node_variant matches the node_query.
    Args:
        node_query: The FallthroughGroup of the query.
        node_variant: The FallthroughGroup of the variant.

    Returns:
        bool: True if the node_variant matches the node_query.
    """
    if not (
        type(node_query) is FallthroughGroup and type(node_variant) is FallthroughGroup
    ):
        return False

    children_query = set(list(node_query))
    children_variant = list(node_variant)

    if children_query.list_length() != children_variant.list_length():
        return False

    for child in children_variant:
        if not child in children_query:
            return False
    return True
