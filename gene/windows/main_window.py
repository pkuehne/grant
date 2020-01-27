""" Contains the MainWindow implementation """

import sys
import os
import yaml
from PyQt5.QtWidgets import QMainWindow, QAction
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtCore import pyqtSignal
from gene.research import ResearchProject
from .plan_overview import PlanOverview
from .plan_details import PlanDetails

ABOUT_STRING = "Copyright (c) 2020 by Peter Kuehne"


class MainWindow(QMainWindow):
    """ The Main Window where we start """
    project_changed = pyqtSignal()
    plan_changed = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.project = None
        self.discard_dialog = None
        self.screens = {}
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
        self.stack = QStackedWidget()

        self.plan_details_screen = PlanDetails()
        self.screens["details"] = self.stack.addWidget(
            self.plan_details_screen)
        self.plan_details_screen.plan_changed.connect(self.plan_changed.emit)
        self.plan_details_screen.close_clicked.connect(
            lambda: self.stack.setCurrentIndex(self.screens["plans"]))

        self.plan_overview_screen = PlanOverview()
        self.screens["plans"] = self.stack.addWidget(self.plan_overview_screen)
        self.plan_changed.connect(
            self.plan_overview_screen.load_plans)

        def select_plan(index: int):
            self.plan_details_screen.select_plan(index)
            self.stack.setCurrentIndex(self.screens["details"])
        self.plan_overview_screen.plan_edited.connect(select_plan)
        self.plan_overview_screen.plan_added.connect(select_plan)
        self.plan_overview_screen.plan_deleted.connect(
            self.plan_overview_screen.load_plans)

        self.stack.setCurrentIndex(self.screens["plans"])
        self.setCentralWidget(self.stack)

        self.project_changed.connect(self.project_changed_handler)

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
        def create_file_menu():
            create_new_action = QAction("&New Project", self)
            create_new_action.setShortcut("CTRL+N")
            create_new_action.triggered.connect(self.create_new_project)

            open_project_action = QAction("&Open Project", self)
            open_project_action.setShortcut("CTRL+O")
            open_project_action.triggered.connect(self.open_project)

            save_project_action = QAction("&Save Project", self)
            save_project_action.setShortcut("CTRL+S")
            save_project_action.triggered.connect(self.save_project)
            save_project_action.setDisabled(True)

            save_project_as_action = QAction("Save &As ...", self)
            save_project_as_action.setShortcut("CTRL+A")
            save_project_as_action.triggered.connect(self.save_project_as)
            save_project_as_action.setDisabled(True)

            quit_action = QAction("&Quit", self)
            quit_action.setShortcut("CTRL+Q")
            quit_action.triggered.connect(sys.exit)

            file_menu = self.menuBar().addMenu("&File")
            file_menu.addAction(create_new_action)
            file_menu.addAction(open_project_action)
            file_menu.addAction(save_project_action)
            file_menu.addAction(save_project_as_action)
            file_menu.addSeparator()
            file_menu.addAction(quit_action)

            def enable_on_project_load():
                save_project_action.setDisabled(self.project is None)
                save_project_as_action.setDisabled(self.project is None)
            self.project_changed.connect(enable_on_project_load)

        def create_help_menu():
            about_action = QAction("&About", self)
            about_action.triggered.connect(lambda:
                                           QMessageBox.about(self, "About", ABOUT_STRING))
            help_menu = self.menuBar().addMenu("&Help")
            help_menu.addAction(about_action)

        create_file_menu()
        create_help_menu()

    def project_changed_handler(self):
        """ Updates all the screens with the new project information """
        self.setup_window_title()
        self.plan_overview_screen.load_project(self.project)
        self.plan_details_screen.load_project(self.project)

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

        self.project_changed.emit()

    def save_project(self):
        """ Saves the currently loaded project """
        if self.project is None:
            print("No project to save")
            return

        with open(self.project.filename, 'w') as file:
            yaml.dump(self.project.to_py(), file)
        print("Saved project: " + self.project.filename)

    def save_project_as(self):
        """ Saves the currently loaded project as a new name """
        if self.project is None:
            print("No project to save")
            return

        (file_name, _) = QFileDialog.getSaveFileName(
            self, "Save as ", ".", "Gene Project (*.gra)")
        if file_name == "":
            print("Cancelled saving")
            return

        self.project.filename = file_name
        self.save_project()

        self.project_changed.emit()

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

        self.project_changed.emit()
