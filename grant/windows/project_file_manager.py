""" Utility class to manage the opening and saving of projects """

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
import yaml
from grant.research import ResearchProject


class ProjectFileManager(QObject):
    """ Wraps file actions on project """
    project_changed = pyqtSignal()
    project_saved = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.needs_saving = False
        self.project = None
        self.discard_dialog = None

        self.setup_discard_dialogs()

    def setup_discard_dialogs(self):
        """ Create re-usable dialogs """
        self.discard_dialog = QMessageBox()
        self.discard_dialog.setIcon(QMessageBox.Warning)
        self.discard_dialog.setText(
            "This will discard your current project without saving")
        self.discard_dialog.setWindowTitle("Are you sure?")
        self.discard_dialog.setStandardButtons(
            QMessageBox.Ok | QMessageBox.Cancel)

    def save_project(self):
        """ Saves the currently loaded project """
        if self.project is None:
            print("No project to save")
            return

        with open(self.project.filename, 'w') as file:
            yaml.dump(self.project.to_py(), file)
        print("Saved project: " + self.project.filename)
        self.needs_saving = False
        self.project_saved.emit()

    def save_project_as(self):
        """ Saves the currently loaded project as a new name """
        if self.project is None:
            print("No project to save")
            return

        (file_name, _) = QFileDialog.getSaveFileName(
            self.parent(), "Save as ", ".", "Grant Project (*.gra)")
        if file_name == "":
            print("Cancelled saving")
            return

        self.project.filename = file_name
        self.save_project()

        self.project_changed.emit()

    def create_new_project(self):
        """ Creates a new Research Project """
        if self.needs_saving:
            button = self.discard_dialog.exec_()
            if button == QMessageBox.Cancel:
                return

        (file_name, _) = QFileDialog.getSaveFileName(
            self.parent(), "Create a project", ".", "Grant Project (*.gra)")
        if file_name == "":
            print("Cancelled creation")
            return

        self.project = ResearchProject(file_name)
        self.save_project()

        self.project_changed.emit()

    def open_project(self):
        """ Opens an existing project """
        if self.needs_saving:
            button = self.discard_dialog.exec_()
            if button == QMessageBox.Cancel:
                return

        (file_name, _) = QFileDialog.getOpenFileName(
            self.parent(), "Open a project", ".", "Grant Project (*.gra)")
        if file_name == "":
            print("Cancelled opening")
            return

        self.project = ResearchProject(file_name)
        with open(self.project.filename) as file:
            self.project.from_py(yaml.safe_load(file))

        self.project_changed.emit()
