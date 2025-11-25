from cortado_core.utils.split_graph import ChoiceGroup, LeafGroup, WildcardGroup, Group, FallthroughGroup


def match(node_query: Group, node_variant: Group) -> bool:
    """
    Checks the two Group have the same type and calls the matching function to compare
    the nodes, if not a ParallelGroup or SequenceGroup.
    Args:
        node_query: The Group of the query.
        node_variant: The Group of the variant.

    Returns:
        bool: True if the leaf matches one of the ChoiceGroup children.
    """
    return True

def match_choice_group_operator(node_query: ChoiceGroup, leaf_variant: LeafGroup) -> bool:
    """
    Checks if the leaf matches one of the children of the choice group.
    Args:
        node_query: The ChoiceGroup of the query.
        leaf_variant: The LeafGroup of the variant.

    Returns:
        bool: True if the leaf_variant matches one of the ChoiceGroup children.
    """
    return True

def match_wildcard_group_operator(leaf_query: WildcardGroup, leaf_variant: LeafGroup) -> bool:
    """
    Checks if the leaf_variant can match the wildcard group.
    Args:
        leaf_query: The WildcardGroup of the query.
        leaf_variant: The LeafGroup of the variant.

    Returns:
        bool: True if the leaf_variant matches the wildcard group.
    """
    return True

def match_no_order(node_query: FallthroughGroup, node_variant: FallthroughGroup) -> bool:
    """
        Checks if the node_variant matches the node_query.
    Args:
        node_query: The FallthroughGroup of the query.
        node_variant: The FallthroughGroup of the variant.

    Returns:
        bool: True if the node_variant matches the node_query.
    """
    return True
