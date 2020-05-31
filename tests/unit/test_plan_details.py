""" Tests for the Plan Details screen """

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
