""" Tests for the project file manager """

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from grant.windows.project_file_manager import ProjectFileManager
from grant.research import ResearchProject


def test_needs_save(qtbot):
    """ Test default value of needs save """
    # Given
    manager = ProjectFileManager()
    qtbot.add_widget(manager)

    # Then
    assert manager.needs_saving is False


def test_save_does_nothing_if_no_project(qtbot):
    """ Saving requires a project """
    # Given
    manager = ProjectFileManager()
    qtbot.add_widget(manager)

    # When
    manager.save_project()


def test_save_resets_need_saving(qtbot, tmpdir):
    """ When saving, the needs_saving flag is reset """
    # Given
    filename = tmpdir.join("test_save_resets_need_saving.txt")
    manager = ProjectFileManager()
    qtbot.add_widget(manager)
    project = ResearchProject(str(filename))
    manager.project = project
    manager.needs_saving = True

    # When
    manager.save_project()

    # Then
    assert manager.needs_saving is False


def test_save_writes_project(qtbot, tmpdir):
    """ When saving, the file is written"""
    # Given
    filename = tmpdir.join("test_save_resets_need_saving.txt")
    manager = ProjectFileManager()
    qtbot.add_widget(manager)
    project = ResearchProject(str(filename))
    manager.project = project

    # When
    with qtbot.waitSignals([manager.project_saved]):
        manager.save_project()

    # Then
    assert filename.read() != ""


def test_save_emits_signal(qtbot, tmpdir):
    """ When saving, the signal is raised """
    # Given
    filename = tmpdir.join("test_save_resets_need_saving.txt")
    manager = ProjectFileManager()
    qtbot.add_widget(manager)
    project = ResearchProject(str(filename))
    manager.project = project

    # When
    with qtbot.waitSignals([manager.project_saved]):
        manager.save_project()


def test_save_as_changes_filename(qtbot, tmpdir, monkeypatch):
    """ When saving, the signal is raised """
    # Given
    filename = tmpdir.join("test_save_resets_need_saving.txt")
    manager = ProjectFileManager()
    qtbot.add_widget(manager)
    project = ResearchProject("")
    manager.project = project

    monkeypatch.setattr(
        QFileDialog, "getSaveFileName", lambda _, __, ___, ____: (str(filename), True)
    )

    # When
    manager.save_project_as()

    # Then
    assert manager.project.filename == str(filename)


def test_save_as_does_nothing_if_no_project_set(qtbot, monkeypatch):
    """ When saving, the signal is raised """
    # Given
    manager = ProjectFileManager()
    qtbot.add_widget(manager)
    monkeypatch.delattr(QFileDialog, "getSaveFileName")

    # When
    manager.save_project_as()

    # Then
    assert manager.project is None


def test_save_as_aborts_on_empty_filename(qtbot, monkeypatch):
    """ When saving, the signal is raised """
    # Given
    filename = "Foo"
    manager = ProjectFileManager()
    qtbot.add_widget(manager)
    project = ResearchProject(filename)
    manager.project = project

    monkeypatch.setattr(
        QFileDialog, "getSaveFileName", lambda _, __, ___, ____: ("", True)
    )

    # When
    with qtbot.assertNotEmitted(manager.project_saved):
        manager.save_project_as()

    # Then
    assert manager.project.filename == filename


def test_create_new_confirms_discard_and_aborts(qtbot, monkeypatch):
    """ When saving, the signal is raised """
    # Given
    manager = ProjectFileManager()
    manager.needs_saving = True
    qtbot.add_widget(manager)
    monkeypatch.delattr(QFileDialog, "getSaveFileName")
    monkeypatch.setattr(manager.project_discard, "exec_", lambda: QMessageBox.Cancel)

    # When
    with qtbot.assertNotEmitted(manager.project_saved):
        manager.create_new_project()

    # Then
    assert manager.project is None


def test_create_new_saves_after_confirming(qtbot, monkeypatch, tmpdir):
    """ When creating new, confirm discarding unsaved changes will then create new """
    # Given
    filename = tmpdir.join("test_save_resets_need_saving.txt")
    manager = ProjectFileManager()
    manager.needs_saving = True
    monkeypatch.setattr(manager.project_discard, "exec_", lambda: QMessageBox.Ok)
    monkeypatch.setattr(
        QFileDialog, "getSaveFileName", lambda _, __, ___, ____: (str(filename), False)
    )

    # When
    with qtbot.waitSignals([manager.project_saved]):
        manager.create_new_project()

    # Then
    assert manager.project is not None
    assert manager.project.filename == filename


def test_create_new_aborts_empty_filename(qtbot, monkeypatch):
    """ When creating, an empty filename will abort the creation """
    # Given
    manager = ProjectFileManager()
    monkeypatch.setattr(
        QFileDialog, "getSaveFileName", lambda _, __, ___, ____: ("", False)
    )

    # When
    with qtbot.assertNotEmitted(manager.project_saved):
        manager.create_new_project()

    # Then
    assert manager.project is None


def test_create_new_creates_new_project_with_signal(qtbot, monkeypatch, tmpdir):
    """ Creating a new project sets the project attribute """
    # Given
    filename = tmpdir.join("test_save_resets_need_saving.txt")
    manager = ProjectFileManager()
    monkeypatch.setattr(
        QFileDialog, "getSaveFileName", lambda _, __, ___, ____: (str(filename), False)
    )

    # When
    with qtbot.waitSignals([manager.project_saved]):
        manager.create_new_project()

    # Then
    assert manager.project is not None
    assert manager.project.filename == filename


def test_open_confirms_discard_and_aborts(qtbot, monkeypatch):
    """ When saving, the signal is raised """
    # Given
    manager = ProjectFileManager()
    manager.needs_saving = True
    qtbot.add_widget(manager)
    monkeypatch.delattr(QFileDialog, "getOpenFileName")
    monkeypatch.setattr(manager.project_discard, "exec_", lambda: QMessageBox.Cancel)

    # When
    with qtbot.assertNotEmitted(manager.project_changed):
        manager.open_project()

    # Then
    assert manager.project is None


def test_open_saves_after_confirming(qtbot, monkeypatch, tmpdir):
    """ When creating new, confirm discarding unsaved changes will then create new """
    # Given
    filename = tmpdir.join("test_open_saves_after_confirming.txt")
    filename.write("gedcom: none\n" + "plans: []\n" + "version: '1.0'")
    manager = ProjectFileManager()
    manager.needs_saving = True
    monkeypatch.setattr(manager.project_discard, "exec_", lambda: QMessageBox.Ok)
    monkeypatch.setattr(
        QFileDialog, "getOpenFileName", lambda _, __, ___, ____: (str(filename), False)
    )

    # When
    with qtbot.waitSignals([manager.project_changed]):
        manager.open_project()

    # Then
    assert manager.project is not None
    assert manager.project.filename == filename


def test_open_aborts_empty_filename(qtbot, monkeypatch):
    """ When creating, an empty filename will abort the creation """
    # Given
    manager = ProjectFileManager()
    monkeypatch.setattr(
        QFileDialog, "getOpenFileName", lambda _, __, ___, ____: ("", False)
    )

    # When
    with qtbot.assertNotEmitted(manager.project_changed):
        manager.open_project()

    # Then
    assert manager.project is None


def test_open_creates_new_project_with_signal(qtbot, monkeypatch, tmpdir):
    """ Creating a new project sets the project attribute """
    # Given
    filename = tmpdir.join("test_save_resets_need_saving.txt")
    filename.write("gedcom: none\n" + "plans: []\n" + "version: '1.0'")
    manager = ProjectFileManager()
    monkeypatch.setattr(
        QFileDialog, "getOpenFileName", lambda _, __, ___, ____: (str(filename), False)
    )

    # When
    with qtbot.waitSignals([manager.project_changed]):
        manager.open_project()

    # Then
    assert manager.project is not None
    assert manager.project.filename == filename


def test_link_gedcom_does_nothing_if_no_project_set(monkeypatch, qtbot):
    """ If the project is None, no gedcom link should be done """
    # Given
    manager = ProjectFileManager()
    monkeypatch.delattr(QFileDialog, "getOpenFileName")

    # when
    with qtbot.assertNotEmitted(manager.project_changed):
        manager.link_gedcom_file()

    # Then
    assert manager.project is None


def test_link_gedcom_discard_cancel_stops(monkeypatch, qtbot):
    """ When a link already exists, ask the user to overwrite it and stop on cancel """
    # Given
    manager = ProjectFileManager()
    manager.project = ResearchProject("")
    manager.project.gedcom = "Foo"
    monkeypatch.delattr(QFileDialog, "getOpenFileName")
    monkeypatch.setattr(manager.gedcom_discard, "exec_", lambda: QMessageBox.Cancel)

    # when
    with qtbot.assertNotEmitted(manager.project_changed):
        manager.link_gedcom_file()

    # Then
    assert manager.project.gedcom == "Foo"


def test_link_gedcom_discard_ok_proceeds(monkeypatch, qtbot):
    """ When a link already exists, ask the user to overwrite it and continue on ok """
    # Given
    manager = ProjectFileManager()
    manager.project = ResearchProject("")
    manager.project.gedcom = "Bar"
    file_name = "Foo"
    monkeypatch.setattr(manager.gedcom_discard, "exec_", lambda: QMessageBox.Ok)
    monkeypatch.setattr(
        QFileDialog, "getOpenFileName", lambda _, __, ___, ____: (file_name, True)
    )

    # When
    with qtbot.waitSignals([manager.project_changed]):
        manager.link_gedcom_file()

    # Then
    assert manager.project.gedcom == file_name
    assert manager.needs_saving is True


def test_link_gedcom_sets_selected_link(monkeypatch, qtbot):
    """ When a new link is selected it should be set on the project """
    # Given
    manager = ProjectFileManager()
    manager.project = ResearchProject("")
    file_name = "Foo"
    monkeypatch.setattr(
        QFileDialog, "getOpenFileName", lambda _, __, ___, ____: (file_name, True)
    )

    # When
    with qtbot.waitSignals([manager.project_changed]):
        manager.link_gedcom_file()

    # Then
    assert manager.project.gedcom == file_name
    assert manager.needs_saving is True


def test_link_gedcom_does_nothing_on_cancel(monkeypatch, qtbot):
    """ When the fileopen dialog is cancelled, the gedcom path is not changed """
    # Given
    manager = ProjectFileManager()
    manager.project = ResearchProject("")
    monkeypatch.setattr(
        QFileDialog, "getOpenFileName", lambda _, __, ___, ____: ("", False)
    )

    # When
    with qtbot.assertNotEmitted(manager.project_changed):
        manager.link_gedcom_file()

    # Then
    assert manager.project.gedcom == ""


def test_unlink_gedcom_does_nothing_if_no_project_set(qtbot):
    """ If the project is None, no gedcom link should be removed """
    # Given
    manager = ProjectFileManager()
    # monkeypatch.delattr(manager.gedcom_discard, "exec_")

    # when
    with qtbot.assertNotEmitted(manager.project_changed):
        manager.unlink_gedcom_file()

    # Then
    assert manager.project is None


def test_unlink_gedcom_does_nothing_if_no_gedcom_link_set(qtbot):
    """ If there is no gedcom link, nothing should happen """
    # Given
    manager = ProjectFileManager()
    manager.project = ResearchProject("")
    # monkeypatch.delattr(manager.gedcom_discard, "exec_")

    # when
    with qtbot.assertNotEmitted(manager.project_changed):
        manager.unlink_gedcom_file()

    # Then
    assert manager.project.gedcom == ""


def test_unlink_discard_cancel_makes_no_change(monkeypatch, qtbot):
    """ When a link exists and the confirmation dialog cancels, nothing should happen """
    # Given
    manager = ProjectFileManager()
    manager.project = ResearchProject("")
    manager.project.gedcom = "Foo"
    monkeypatch.setattr(manager.gedcom_discard, "exec_", lambda: QMessageBox.Cancel)

    # when
    with qtbot.assertNotEmitted(manager.project_changed):
        manager.unlink_gedcom_file()

    # Then
    assert manager.project.gedcom == "Foo"


def test_unlink_discard_ok_removes_link(monkeypatch, qtbot):
    """ When a link exists and the confirmation dialog accepted, the link is removed """
    # Given
    manager = ProjectFileManager()
    manager.project = ResearchProject("")
    manager.project.gedcom = "Foo"
    monkeypatch.setattr(manager.gedcom_discard, "exec_", lambda: QMessageBox.Ok)

    # when
    with qtbot.waitSignals([manager.project_changed]):
        manager.unlink_gedcom_file()

    # Then
    assert manager.project.gedcom == ""
    assert manager.needs_saving is True
