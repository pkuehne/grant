""" Tests for the ProjectOverview dialog """

from grant.windows.project_overview_dialog import ProjectOverviewDialog
from grant.windows.data_context import DataContext
from grant.research import ResearchProject


def test_dialog_builds(qtbot):
    """ a """
    # Given
    dialog = ProjectOverviewDialog(DataContext(), ResearchProject("Foobar"), None)
    qtbot.add_widget(dialog)

    # When

    # Then
    assert dialog.filename_label.text() == "Foobar"


def test_show_classmethod(monkeypatch):
    """ Check the function does what it says """
    # Given

    monkeypatch.setattr(ProjectOverviewDialog, "exec_", lambda _: None)

    # When
    ProjectOverviewDialog.show(DataContext(), ResearchProject("Foobar"), None)

    # Then
