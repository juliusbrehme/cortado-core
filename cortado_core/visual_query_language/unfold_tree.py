from cortado_core.utils.split_graph import Group


def unfold_tree(tree_query: Group) -> Group:
    """
    Turns the given tree into a tree to be used for filtering a query.
    Args:
        tree_query: The query given as a tree.

    Returns:
        Group: A tree that is unfolded to be used for filtering.
    """
    return tree_query
