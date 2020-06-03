""" Tests for the Task Details screen """

from grant.windows.task_details import TaskDetails
from grant.windows.data_context import DataContext


def test_source_edit_has_completer(qtbot):
    """ Check that the source edit has a completer """
    # Given
    data_context = DataContext()

    # When
    screen = TaskDetails(data_context)
    qtbot.add_widget(screen)

    # Then
    assert screen.source.completer() is not None
    assert screen.source.completer().model() is not None
