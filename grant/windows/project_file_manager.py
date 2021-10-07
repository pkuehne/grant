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
        self.project_discard = None
        self.gedcom_discard = None

        self.setup_project_discards()

    def setup_project_discards(self):
        """ Create re-usable dialogs """
        self.project_discard = QMessageBox()
        self.project_discard.setIcon(QMessageBox.Warning)
        self.project_discard.setText(
            "This will discard your current project without saving"
        )
        self.project_discard.setWindowTitle("Are you sure?")
        self.project_discard.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        self.gedcom_discard = QMessageBox()
        self.gedcom_discard.setIcon(QMessageBox.Warning)
        self.gedcom_discard.setText("This will remove your current gedcom file link")
        self.gedcom_discard.setWindowTitle("Are you sure?")
        self.gedcom_discard.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    def save_project(self):
        """ Saves the currently loaded project """
        if self.project is None:
            return

        with open(self.project.filename, "w") as file:
            yaml.dump(self.project.to_py(), file)
        self.needs_saving = False
        self.project_saved.emit()

    def save_project_as(self):
        """ Saves the currently loaded project as a new name """
        if self.project is None:
            return

        (file_name, _) = QFileDialog.getSaveFileName(
            self.parent(), "Save as ", ".", "Grant Project (*.gra)"
        )
        if file_name == "":
            return

        self.project.filename = file_name
        self.save_project()

        self.project_changed.emit()

    def create_new_project(self):
        """ Creates a new Research Project """
        if self.needs_saving:
            button = self.project_discard.exec_()
            if button == QMessageBox.Cancel:
                return

        (file_name, _) = QFileDialog.getSaveFileName(
            self.parent(), "Create a project", ".", "Grant Project (*.gra)"
        )
        if file_name == "":
            return

        self.project = ResearchProject(file_name)
        self.save_project()

        self.project_changed.emit()

    def open_project(self):
        """ Opens an existing project """
        if self.needs_saving:
            button = self.project_discard.exec_()
            if button == QMessageBox.Cancel:
                return

        (file_name, _) = QFileDialog.getOpenFileName(
            self.parent(), "Open a project", ".", "Grant Project (*.gra)"
        )
        if file_name == "":
            return

        self.project = ResearchProject(file_name)
        with open(self.project.filename) as file:
            self.project.from_py(yaml.safe_load(file))

        self.project_changed.emit()

    def link_gedcom_file(self):
        """ Asks for the filename and then links that to the project """
        if self.project is None:
            return

        if self.project.gedcom != "":
            button = self.gedcom_discard.exec_()
            if button == QMessageBox.Cancel:
                return

        (file_name, _) = QFileDialog.getOpenFileName(
            self.parent(), "Select file link", ".", "Gedcom File (*.ged)"
        )
        if file_name == "":
            return

        self.project.gedcom = file_name
        self.needs_saving = True
        self.project_changed.emit()

    def unlink_gedcom_file(self):
        """ Remove a gedcom file link """
        if self.project is None:
            return

        if self.project.gedcom == "":
            return

        button = self.gedcom_discard.exec_()
        if button == QMessageBox.Cancel:
            return

        self.project.gedcom = ""
        self.needs_saving = True
        self.project_changed.emit()
