""" Contains the MainWindow implementation """

import sys
import os
import yaml
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QAction
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from gene.research import ResearchProject


class MainWindow(QMainWindow):
    """ The Main Window where we start """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.project = None
        self.discard_dialog = None
        self.setup_window()
        self.setup_window_title()
        self.setup_menubar()
        self.setup_statusbar()
        self.setup_dialogs()

    def setup_window_title(self):
        """ Sets the window title from project name """
        title = "Gene - "
        if self.project is not None:
            title += os.path.splitext(
                os.path.basename(self.project.filename))[0]
        else:
            title += " The Genealogical Research Assistant"
        self.setWindowTitle(title)

    def setup_window(self):
        """ Sets up all widgets and window stuff """
        self.root = QWidget(self)
        self.setCentralWidget(self.root)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("title"))
        layout.addWidget(QLabel("goal"))

        self.root.setLayout(layout)

    def setup_dialogs(self):
        """ Create re-usable dialogs """
        self.discard_dialog = QMessageBox()
        self.discard_dialog.setIcon(QMessageBox.Warning)
        self.discard_dialog.setText(
            "This will discard your current project without saving")
        self.discard_dialog.setWindowTitle("Are you sure?")
        self.discard_dialog.setStandardButtons(
            QMessageBox.Ok | QMessageBox.Cancel)

    def setup_statusbar(self):
        """ Create status bar """
        self.statusBar()

    def setup_menubar(self):
        """ Sets up the menu bar """
        create_new_action = QAction("&New Project", self)
        create_new_action.setShortcut("CTRL+N")
        create_new_action.triggered.connect(self.create_new_project)

        open_project_action = QAction("&Open Project", self)
        open_project_action.setShortcut("CTRL+O")
        open_project_action.triggered.connect(self.open_project)

        save_project_action = QAction("&Save Project", self)
        save_project_action.setShortcut("CTRL+S")
        save_project_action.triggered.connect(self.save_project)

        quit_action = QAction("&Quit", self)
        quit_action.setShortcut("CTRL+Q")
        quit_action.triggered.connect(sys.exit)

        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(create_new_action)
        file_menu.addAction(open_project_action)
        file_menu.addAction(save_project_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

    def create_new_project(self):
        """ Creates a new Research Project """
        if self.project is not None:
            button = self.discard_dialog.exec_()
            if button == QMessageBox.Cancel:
                return

        (file_name, _) = QFileDialog.getSaveFileName(
            self, "Create a project", ".", "Gene Project (*.gra)")
        if file_name == "":
            print("Cancelled creation")
            return

        self.project = ResearchProject(file_name)
        self.save_project()
        self.setup_window_title()

    def save_project(self):
        """ Saves the currently loaded project """
        if self.project is None:
            print("No project to save")
            return

        with open(self.project.filename, 'w') as file:
            yaml.dump(self.project.to_py(), file)
        print("Saved project: " + self.project.filename)

    def open_project(self):
        """ Opens an existing project """
        if self.project is not None:
            button = self.discard_dialog.exec_()
            if button == QMessageBox.Cancel:
                return

        (file_name, _) = QFileDialog.getOpenFileName(
            self, "Open a project", ".", "Gene Project (*.gra)")
        if file_name == "":
            print("Cancelled opening")
            return

        self.project = ResearchProject(file_name)
        with open(self.project.filename) as file:
            self.project.from_py(yaml.safe_load(file))
        self.setup_window_title()
