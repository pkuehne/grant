""" Test for the TreeNode """

from grant.models.tree_node import TreeNode


def test_empty_icon_returned_for_unknown_node_type():
    """ Return an empty QIcon if the type is invalid """
    # Given
    node = TreeNode("foo", None, None, 0)

    # When
    icon = node.get_icon()

    # Then
    assert icon.isNull()
