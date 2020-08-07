""" Tests for the LinkedLineEdit widget """

from PyQt5.QtWidgets import QMessageBox
from grant.windows.linkedlineedit_widget import LinkedLineEdit
from grant.windows.data_context import DataContext
from grant.models.individuals_model import IndividualsModel
from grant.models.individuals_model import Individual


def test_completer_set(qtbot):
    """ Check that the ancestor edit has a completer """
    # Given
    data_context = DataContext()

    # When
    widget = LinkedLineEdit(data_context.individuals_model, 0, 0)
    qtbot.add_widget(widget)

    # Then
    assert widget.completer() is not None
    assert widget.completer().model() is not None


def test_set_link_visible_updates_action_visibility(qtbot):
    """ When the link_visible() slot is called, it updates the action's visibility """
    # Given
    data_context = DataContext()
    widget = LinkedLineEdit(data_context.individuals_model, 0, 0)
    qtbot.add_widget(widget)
    widget.link_action.setVisible(False)

    # When
    widget.set_link_visible(True)

    # Then
    assert widget.link_action.isVisible() is True


def test_unlink_clears_link_on_confirmation(qtbot, monkeypatch):
    """
    When the unlink action is triggered, the link should be cleared and the change submitted
    after the user confirmed
    """
    # Given
    data_context = DataContext()
    widget = LinkedLineEdit(data_context.individuals_model, 0, 0)
    qtbot.add_widget(widget)
    monkeypatch.setattr(widget.confirmation_dialog, "exec_", lambda: QMessageBox.Ok)

    # When
    with qtbot.waitSignals([widget.link_updated]):
        widget.unlink_name()

    # Then


def test_unlink_does_nothin_if_cancelled(qtbot, monkeypatch):
    """
    When the unlink action is triggered, the link should not be cleared if the user cancelled
    the dialog
    """
    # Given
    data_context = DataContext()
    widget = LinkedLineEdit(data_context.individuals_model, 0, 0)
    qtbot.add_widget(widget)
    monkeypatch.setattr(widget.confirmation_dialog, "exec_", lambda: QMessageBox.Cancel)

    # When
    with qtbot.assertNotEmitted(widget.link_updated):
        widget.unlink_name()

    # Then


def test_autocomplete_activated_emits_pointer_value(qtbot):
    """
    When the autocomplete_activated signal is processed, the item's pointer value
    should be emitted as the link value
    """
    # Given
    record = Individual("I123", "Foo1", "Person", 1901, 1951)
    model = IndividualsModel([record])
    data_context = DataContext(individuals_model=model)
    widget = LinkedLineEdit(data_context.individuals_model, 0, 0)
    qtbot.add_widget(widget)
    index = model.index(0, 1)

    def check_individual(text: str):
        return text == record.pointer

    # When
    with qtbot.waitSignal(widget.link_updated, check_params_cb=check_individual):
        widget.autocomplete_activated(index)

    # Then
