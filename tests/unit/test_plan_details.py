""" Tests for the Plan Details screen """

from unittest import mock
from PyQt5.QtWidgets import QMessageBox
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


def test_unlink_clears_link_on_confirmation(qtbot, monkeypatch):
    """
    When the unlink action is triggered, the link should be cleared and the change submitted
    after the user confirmed
    """
    # Given
    data_context = DataContext()
    screen = PlanDetails(data_context)
    qtbot.add_widget(screen)

    screen.link.setText("Foo")
    screen.mapper = mock.MagicMock()

    monkeypatch.setattr(screen.confirmation_dialog, "exec_", lambda: QMessageBox.Ok)

    # When
    screen.unlink_name()

    # Then
    assert screen.link.text() == ""
    screen.mapper.submit.assert_called()


def test_unlink_does_nothin_if_cancelled(qtbot, monkeypatch):
    """
    When the unlink action is triggered, the link should not be cleared if the user cancelled
    the dialog
    """
    # Given
    data_context = DataContext()
    screen = PlanDetails(data_context)
    qtbot.add_widget(screen)

    screen.link.setText("Foo")
    screen.mapper = mock.MagicMock()

    monkeypatch.setattr(screen.confirmation_dialog, "exec_", lambda: QMessageBox.Cancel)

    # When
    screen.unlink_name()

    # Then
    assert screen.link.text() != ""
    screen.mapper.submit.assert_not_called()
