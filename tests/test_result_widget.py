""" Tests for the ResultWidget class """

import pytest
from grant.windows.result_widget import ResultWidget
from grant.windows.result_dialog import ResultDialog
from grant.research import ResearchResult


def test_result_is_none_by_default(qtbot):
    """ Test that the result stored in the widget is none by default """

    # Given
    widget = ResultWidget()
    widget.show()
    qtbot.add_widget(widget)

    # Then
    assert widget.result is None


@pytest.mark.parametrize("result, textbox_visible, result_nil_visible, result_success_visible",
                         [
                             (ResearchResult(False), True, False, False),
                             (ResearchResult(True), True, False, False),
                             (None, False, True, True)
                         ])
def test_setter_hides_and_shows_widget_based_on_result(result,
                                                       textbox_visible,
                                                       result_nil_visible,
                                                       result_success_visible,
                                                       qtbot):
    """ Test that setting a nil result shows the text box """

    # Given
    widget = ResultWidget()
    widget.show()
    qtbot.addWidget(widget)

    # When
    widget.result = result

    # Then
    assert widget.textbox.isVisible() is textbox_visible
    assert widget.result_nil.isVisible() is result_nil_visible
    assert widget.result_success.isVisible() is result_success_visible


def test_show_result_dialog_emits_changed_signal(qtbot, monkeypatch):
    """ When show_result_dialog is called, a changed signal is emitted """
    # Given
    widget = ResultWidget()
    widget.show()
    qtbot.add_widget(widget)
    initial_result = ResearchResult(True)
    widget.result = initial_result

    monkeypatch.setattr(
        ResultDialog, "get_result", classmethod(lambda *args: (widget.result))
    )

    # When
    with qtbot.waitSignals([widget.result_changed]):
        widget.show_result_dialog()

    # Then
    assert widget.result == initial_result


@pytest.mark.parametrize("result_type", [True, False])
def test_record_result_creates_result_object(result_type, qtbot, monkeypatch):
    """ When show_result_dialog is called, a changed signal is emitted """
    # Given
    widget = ResultWidget()
    widget.show()
    qtbot.add_widget(widget)

    def fake_dialog(_, result, __):
        assert result is not None
        assert result.is_nil() is not result_type
        return result

    monkeypatch.setattr(
        ResultDialog, "get_result", classmethod(fake_dialog)
    )

    # When
    with qtbot.waitSignals([widget.result_changed]):
        widget.record_result(result_type)

    # Then
    assert widget.result is not None
    assert widget.result.is_nil() is not result_type
