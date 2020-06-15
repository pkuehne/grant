""" Test for the TreeNode """

from grant.models.tree_node import TreeNode
from types import SimpleNamespace


def test_empty_icon_returned_for_unknown_node_type():
    """ Return an empty QIcon if the type is invalid """
    # Given
    node = TreeNode("foo", None, None, 0)

    # When
    icon = node.get_icon()

    # Then
    assert icon.isNull()


def test_ancestor_returns_empty_for_plan():
    """ get_ancestor() returns an empty string for a plan """
    # Given
    data = SimpleNamespace(tasks=[], ancestor="foo")
    node = TreeNode("plan", data, None, 0)

    # Then
    assert node.get_ancestor() == ""


def test_ancestor_returns_parent_ancestor_name_for_task():
    """ For a task, get_ancestor() returns the ancestor value of the parent plan """
    data = SimpleNamespace(tasks=[], ancestor="foo")
    plan = TreeNode("plan", data, None, 0)
    task = TreeNode("task", None, plan, 1)

    # Then
    assert task.get_ancestor() == "foo"
