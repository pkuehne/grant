""" Tests for the ProjectOverview dialog """

from grant.windows.project_overview_dialog import ProjectOverviewDialog
from grant.windows.data_context import DataContext


def test_a(qtbot):
    """ a """
    # Given
    dialog = ProjectOverviewDialog(DataContext())
    qtbot.add_widget(dialog)

    # When

    # Then
