""" Tests for the Plan Details screen """

from unittest import mock
from grant.windows.plan_details import PlanDetails
from grant.windows.data_context import DataContext


def test_ancestor_edit_has_completer(qtbot):
    """ Check that the ancestor edit has a completer """
    # Given
    data_context = DataContext()

    # When
    screen = PlanDetails(data_context)
    qtbot.add_widget(screen)

    # Then
    assert screen.ancestor.completer() is not None
    assert screen.ancestor.completer().model() is not None


def test_link_updated_sets_link_edit(qtbot):
    """
    When the link_updated() function is triggered, it updates the _link_
    QLineEdit and calls the mapper to submit the changes
    """
    # Given
    data_context = DataContext()
    screen = PlanDetails(data_context)
    qtbot.add_widget(screen)

    screen.link.setText("Foo")
    screen.mapper = mock.MagicMock()

    # When
    screen.link_updated("Bar")

    # Then
    assert screen.link.text() == "Bar"
    screen.mapper.submit.assert_called()
