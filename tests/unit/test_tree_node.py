""" Test for the TreeNode """

from types import SimpleNamespace
import pytest
from grant.models.tree_node import TreeNode


def test_empty_icon_returned_for_unknown_node_type():
    """ Return an empty QIcon if the type is invalid """
    # Given
    node = TreeNode("foo", None, None, 0)

    # When
    icon = node.get_icon()

    # Then
    assert icon.isNull()


@pytest.mark.parametrize("node_type", ["plan", "task"])
def test_icon_returned_for_node_type(node_type):
    """ Return an empty QIcon if the type is invalid """
    # Given
    data = SimpleNamespace(tasks=[])
    node = TreeNode(node_type, data, None, 0)

    # When
    icon = node.get_icon()

    # Then
    assert icon.isNull() is False


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


def test_get_link_returns_link_id():
    """ get_link() returns the relevant gedcom link """
    plan_data = SimpleNamespace(tasks=[], ancestor_link=123)
    task_data = SimpleNamespace(source_link=123)
    plan = TreeNode("plan", plan_data, None, 0)
    task = TreeNode("task", task_data, plan, 1)
    bad = TreeNode("other", None, None, 2)

    # Then
    assert plan.get_link() == plan_data.ancestor_link
    assert task.get_link() == task_data.source_link
    assert bad.get_link() == ""


def test_set_link_updates_link_id():
    """ set_link() updates the relevant gedcom link """
    # Given
    plan_data = SimpleNamespace(tasks=[], ancestor_link=1)
    task_data = SimpleNamespace(source_link=2)
    plan = TreeNode("plan", plan_data, None, 0)
    task = TreeNode("task", task_data, plan, 1)
    bad = TreeNode("other", None, None, 2)

    # When
    plan.set_link(1234)
    task.set_link(2345)
    bad.set_link(3456)

    # Then
    assert plan_data.ancestor_link == 1234
    assert task_data.source_link == 2345
