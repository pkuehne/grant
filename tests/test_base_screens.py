""" Tests for the base screens """

from unittest import mock
import pytest
from PyQt5.QtCore import QModelIndex
from grant.research import ResearchProject
from grant.windows.base_screens import BaseScreen, DetailScreen, SelectionScreen


def test_base_screen_has_no_project_by_default(qtbot):
    """ creating a base screen does not set a project """
    # Given
    screen = BaseScreen(None)
    qtbot.addWidget(screen)

    # When

    # Then
    assert screen.project is None


def test_update_project_sets_project(qtbot):
    """ update_project() slot sets the screen's project reference """
    # Given
    screen = BaseScreen(None)
    project = ResearchProject("")
    qtbot.addWidget(screen)

    # When
    screen.update_project(project)

    # Then
    assert screen.project is not None
    assert screen.project == project


def test_setting_selected_item_on_detail_screen_checks_for_mapper(qtbot):
    """ Detail screens may not have a mapper, so check before using it """
    # Given
    screen = DetailScreen(None)
    screen.project = ResearchProject("")
    qtbot.addWidget(screen)

    # When
    screen.set_selected_item(QModelIndex())


def test_setting_selected_item_on_detail_screen_updates_mapper(qtbot):
    """ Mapper should be set for Detail screen """
    # Given
    screen = DetailScreen(None)
    screen.project = ResearchProject("")
    screen.mapper = mock.MagicMock()
    qtbot.addWidget(screen)

    # When
    screen.set_selected_item(QModelIndex())
    screen.mapper.setRootIndex.assert_called()


def test_setting_selected_item_on_detail_screen_requires_project_set(qtbot):
    """ Mapper should be set for Detail screen """
    # Given
    screen = DetailScreen(None)
    screen.project = None
    screen.mapper = mock.MagicMock()
    qtbot.addWidget(screen)

    # When
    screen.set_selected_item(QModelIndex())
    screen.mapper.setRootIndex.assert_not_called()


def test_derived_screens_must_implement_clear_selection(qtbot):
    """ The clear_selection function should not be called directly """
    # Given
    screen = SelectionScreen(None)
    qtbot.addWidget(screen)

    # When
    with pytest.raises(NotImplementedError):
        screen.clear_selection()
