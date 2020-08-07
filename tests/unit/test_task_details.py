""" Tests for the Task Details screen """

from unittest import mock
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


def test_link_updated_sets_link_edit(qtbot):
    """
    When the link_updated() function is triggered, it updates the _link_
    QLineEdit and calls the mapper to submit the changes
    """
    # Given
    data_context = DataContext()
    screen = TaskDetails(data_context)
    qtbot.add_widget(screen)

    screen.link.setText("Foo")
    screen.mapper = mock.MagicMock()

    # When
    screen.link_updated("Bar")

    # Then
    assert screen.link.text() == "Bar"
    screen.mapper.submit.assert_called()
