""" Tests for the MainWindow """

from grant.windows.main_window import MainWindow


def test_statusbar_is_initialized(qtbot):
    """ Statusbar should not be empty """
    # Given
    window = MainWindow()
    window.show()
    qtbot.addWidget(window)

    # Then
    assert window.statusBar().currentMessage() != ""


def test_project_doesnt_need_saving_by_default(qtbot):
    """ Statusbar should not be empty """
    # Given
    window = MainWindow()
    window.show()
    qtbot.addWidget(window)

    # Then
    assert window.project_needs_saving is False


def test_sample_data_is_loaded_when_os_variable_set(qtbot, monkeypatch):
    """ When the GRANT_TEST variable is set, sample data is loaded """
    # Given
    monkeypatch.setenv("GRANT_TEST", "TRUE")
    window = MainWindow()
    qtbot.addWidget(window)

    # When
    window.show()

    # Then
    assert window.project is not None