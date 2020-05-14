""" Tests for the ResultDialog window """

import pytest
from grant.windows.result_dialog import ResultDialog
from grant.research import ResearchResult


@pytest.mark.parametrize("text, value", [("success", ResearchResult(True)),
                                         ("nil", ResearchResult(False)),
                                         ("<remove>", None)])
def test_status_is_success(qtbot, text, value):
    """ When the result passed in as success, the status field should be success """
    # Given
    result = value

    # When
    dialog = ResultDialog(result)
    qtbot.add_widget(dialog)

    # Then
    assert dialog.status.currentText() == text


@pytest.mark.parametrize("text, value", [("success", True), ("nil", False)])
def test_result_fields_are_set(qtbot, text, value):
    """ The fields from the result should be set on the dialog """
    # Given
    result = ResearchResult(value)
    result.summary = "SUMMARY"
    result.document = "DOCUMENT"

    # When
    dialog = ResultDialog(result)
    qtbot.add_widget(dialog)

    # Then
    assert dialog.status.currentText() == text
    assert dialog.summary.toPlainText() == result.summary
    assert dialog.document.text() == result.document


def test_ok_sets_result_to_none_on_remove_selected(qtbot):
    """ When the OK button is pressed and the status is set to remove, the result is None'd """
    # Given
    result = ResearchResult(False)
    result.summary = "SUMMARY"
    result.document = "DOCUMENT"

    dialog = ResultDialog(result)
    qtbot.add_widget(dialog)
    dialog.status.setCurrentText("<remove>")

    # When
    dialog.ok_pressed()

    # Then
    assert dialog.result is None


@pytest.mark.parametrize("text, value", [("success", False), ("nil", True)])
def test_ok_sets_result_to_based_on_selection(qtbot, text, value):
    """ When the OK button is pressed and the status is not remove, the right Result is set """
    # Given
    result = ResearchResult(value)
    result.summary = "SUMMARY"
    result.document = "DOCUMENT"

    dialog = ResultDialog(result)
    qtbot.add_widget(dialog)
    dialog.status.setCurrentText(text)

    # When
    dialog.ok_pressed()

    # Then
    assert dialog.result is not None
    assert dialog.result.nil is value


@pytest.mark.parametrize("text", ["success", "nil"])
def test_ok_sets_creates_result_if_none_set(qtbot, text):
    """
    When the OK button is pressed and there is no result, one will be created for success/nil
    """
    # Given
    dialog = ResultDialog(None)
    qtbot.add_widget(dialog)
    dialog.status.setCurrentText(text)

    # When
    dialog.ok_pressed()

    # Then
    assert dialog.result is not None


def test_get_result_classmethod(monkeypatch):
    """ Check the function does what it says """
    # Given

    def exec_func(self):
        self.result = ResearchResult(True)
    monkeypatch.setattr(ResultDialog, 'exec_', exec_func)

    # When
    result = ResultDialog.get_result(None, None)

    # Then
    assert result is not None
    assert result.is_nil() is False
