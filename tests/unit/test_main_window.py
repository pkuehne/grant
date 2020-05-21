""" Tests for the MainWindow """

from PyQt5.QtCore import QModelIndex
from grant.windows.main_window import MainWindow
from grant.research import ResearchProject


def test_sample_data_is_loaded_when_os_variable_set(qtbot, monkeypatch):
    """ When the GRANT_TEST variable is set, sample data is loaded """
    # Given
    monkeypatch.setenv("GRANT_TEST", "TRUE")
    window = MainWindow()
    qtbot.addWidget(window)

    # When
    window.show()

    # Then
    assert window.project_manager.project is not None


def test_menu_title_contains_splash_text_instead_of_project(qtbot):
    """ When no project is set, the splash text should be shown """
    # Given
    window = MainWindow()
    qtbot.addWidget(window)
    window.project_manager.project = None

    # When
    window.setup_window_title()

    # Then
    assert "Grant" in window.windowTitle()
    assert "Genealogical Research AssistaNT" in window.windowTitle()


def test_menu_title_contains_project_name(qtbot):
    """ When a project is set, the filename should be shown """
    # Given
    filename = "foo"
    window = MainWindow()
    qtbot.addWidget(window)
    window.project_manager.project = ResearchProject(
        "/home/bar/test/" + filename + ".gra")

    # When
    window.setup_window_title()

    # Then
    assert "Grant" in window.windowTitle()
    assert filename in window.windowTitle()
    assert "*" not in window.windowTitle()


def test_menu_title_contains_asterisk_if_unsaved(qtbot):
    """ When a project is set and unsaved, an asterisk should be shown """
    # Given
    filename = "foo"
    window = MainWindow()
    qtbot.addWidget(window)
    window.project_manager.project = ResearchProject(
        "/home/bar/test/" + filename + ".gra")
    window.project_manager.needs_saving = True

    # When
    window.setup_window_title()

    # Then
    assert "Grant" in window.windowTitle()
    assert filename in window.windowTitle()
    assert "*" in window.windowTitle()


def test_model_data_change_sets_dirty_flag(qtbot):
    """
    When the main model's underlying data changes, the dirty flag should be set on the project file
    """
    # Given
    window = MainWindow()
    qtbot.addWidget(window)

    # When
    window.data_model.dataChanged.emit(QModelIndex(), QModelIndex())

    # Then
    assert window.project_manager.needs_saving is True
