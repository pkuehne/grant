""" Tests for the base screens """

from gene.research import ResearchProject
from gene.windows.base_screens import BaseScreen


def test_base_screen_has_no_project_by_default(qtbot):
    """ creating a base screen does not set a project """
    # Given
    screen = BaseScreen()
    qtbot.addWidget(screen)

    # When

    # Then
    assert screen.project is None


def test_update_project_sets_project(qtbot):
    """ update_project() slot sets the screen's project reference """
    # Given
    screen = BaseScreen()
    project = ResearchProject("")
    qtbot.addWidget(screen)

    # When
    screen.update_project(project)

    # Then
    assert screen.project is not None
    assert screen.project == project
