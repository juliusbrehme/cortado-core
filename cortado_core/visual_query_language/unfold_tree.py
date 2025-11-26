from cortado_core.utils.split_graph import Group


def unfold_tree(tree_query: Group) -> Group:
    """
    Turns the given query tree into a query tree to be used for filtering a variant.
    Args:
        tree_query: The query given as a tree.

    Returns:
        Group: A tree that is unfolded to be used for filtering.
    """
    return tree_query
