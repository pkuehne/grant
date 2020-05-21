""" Tests for the main screen widget """

from types import SimpleNamespace
from unittest import mock
import pytest
from PyQt5.QtCore import QModelIndex
from grant.windows.main_screen import MainScreen
from grant.models.tree_model import TreeModel
from grant.windows.base_screens import DetailScreen
from grant.research import ResearchProject


def test_selection_change_picks_blank_detail_screen(qtbot):
    """ When changing the selection screen, the blank details screen should be loaded """
    # Given
    screen = MainScreen(None, TreeModel())
    qtbot.add_widget(screen)

    # When
    screen.change_selection_screen("tree")

    # Then
    assert screen.detail_stack.currentWidget() == screen.screens["blank"]


def test_selection_change_picks_selection_screen(qtbot):
    """ When changing the selection screen, the blank details screen should be loaded """
    # Given
    screen = MainScreen(None, TreeModel())
    qtbot.add_widget(screen)

    # When
    screen.change_selection_screen("tree")

    # Then
    assert screen.selection_stack.currentWidget() == screen.screens["tree"]


def test_detail_change_sets_screen(qtbot):
    """ When changing the selection screen, the blank details screen should be loaded """
    # Given
    screen = MainScreen(None, TreeModel())
    qtbot.add_widget(screen)

    # When
    screen.change_detail_screen("blank", QModelIndex())

    # Then
    assert screen.detail_stack.currentWidget() == screen.screens["blank"]


@pytest.mark.parametrize("node_type, screen_name", [("gedcom", "blank"), ("plan", "plan"), ("task", "task"), ("Foo", "blank")])
def test_selection_changed_handler_updates_detail_screen(qtbot, node_type, screen_name):
    """ Given a particular node type, what detail screen is being shown """
    # Given
    node = SimpleNamespace()
    node.type = node_type
    item = mock.MagicMock()
    item.internalPointer = mock.MagicMock(return_value=node)

    screen = MainScreen(None, TreeModel())
    screen.change_detail_screen = mock.MagicMock()
    qtbot.add_widget(screen)

    # When
    screen.selection_changed(item)

    # Then
    screen.change_detail_screen.assert_called_with(screen_name, item)


def test_update_project_updates_screens(qtbot):
    """ When caling update_project, this is passed to the screens """
    # Given
    screen = MainScreen(None, TreeModel())
    qtbot.add_widget(screen)
    project = ResearchProject("")
    assert screen.screens["blank"].project is None

    # When
    screen.set_project(project)

    # Then
    assert screen.screens["blank"].project == project
