""" Contains the MainWindow implementation """

import sys
import os
import yaml
from PyQt5.QtWidgets import QMainWindow, QAction
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from grant.research import ResearchProject
from .plan_details import PlanDetails
from .task_details import TaskDetails
from .base_screens import DetailScreen
from .tree_selection_screen import TreeSelectionScreen
from .filter_selection_screen import FilterSelectionScreen
from .tree_model import TreeModel

VERSION_NUMBER = "0.1"
ABOUT_STRING = "Copyright (c) 2020 by Peter Kühne\nIcons from https://icons8.com"
TEST_DATA = """
gedcom: none
plans:
- goal: To be a goood test plan
  tasks:
  - status: active
    title: Task 1
  - status: active
    title: Task 2
  title: Test Plan 1
- goal: Another test plan
  tasks: []
  title: Test Plan 2
version: '1.0'
"""


class MainWindow(QMainWindow):
    """ The Main Window where we start """
    project_changed = pyqtSignal()
    plan_changed = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.project = None
        self.data_model = TreeModel()
        self.discard_dialog = None
        self.selection_screens = {}
        self.selection_stack = None
        self.detail_screens = {}
        self.detail_stack = None
        self.project_needs_saving = False
        self.setup_window()
        self.setup_window_title()
        self.setup_menubar()
        self.setup_statusbar()
        self.setup_dialogs()

        if os.getenv("GRANT_TEST", "") != "":
            self.project = ResearchProject("test_data")
            self.project.from_py(yaml.safe_load(TEST_DATA))
            self.project_changed.emit()

    def setup_window_title(self):
        """ Sets the window title from project name """
        title = "Grant - "
        if self.project is not None:
            title += os.path.splitext(
                os.path.basename(self.project.filename))[0]
            title += "*" if self.project_needs_saving else ""
        else:
            title += " The Genealogical Research AssistaNT"
        self.setWindowTitle(title)

    def setup_window(self):
        """ Sets up all widgets and window stuff """
        self.setWindowIcon(QIcon(":/icons/books.ico"))
        self.selection_stack = QStackedWidget()

        self.selection_screens["tree"] = TreeSelectionScreen(self.data_model)
        self.selection_stack.addWidget(self.selection_screens["tree"])

        self.selection_screens["filter"] = FilterSelectionScreen(
            self.data_model)
        self.selection_stack.addWidget(self.selection_screens["filter"])

        def selection_changed(item):
            node = item.internalPointer()
            if node.type == "gedcom":
                self.detail_stack.setCurrentWidget(
                    self.detail_screens["blank"])
                return
            if node.type == "task":
                self.detail_stack.setCurrentWidget(
                    self.detail_screens["task"])
                self.detail_screens["task"].set_selected_item(item)
                return
            if node.type == "plan":
                self.detail_stack.setCurrentWidget(self.detail_screens["plan"])
                self.detail_screens["plan"].set_selected_item(item)
                return
            self.detail_stack.setCurrentWidget(self.detail_screens["blank"])

        self.selection_screens["tree"].item_selected.connect(selection_changed)

        self.detail_stack = QStackedWidget()

        self.detail_screens["blank"] = DetailScreen(self.data_model)
        self.detail_stack.addWidget(self.detail_screens["blank"])
        self.detail_screens["plan"] = PlanDetails(self.data_model)
        self.detail_stack.addWidget(self.detail_screens["plan"])
        self.detail_screens["task"] = TaskDetails(self.data_model)
        self.detail_stack.addWidget(self.detail_screens["task"])

        self.detail_stack.setCurrentWidget(self.detail_screens["blank"])

        central_widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.selection_stack)
        layout.addWidget(self.detail_stack)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self.project_changed.connect(self.project_changed_handler)

        def model_changed():
            print("model changed")
            self.project_needs_saving = True
            self.setup_window_title()
        self.data_model.dataChanged.connect(model_changed)
        self.data_model.layoutChanged.connect(model_changed)
        self.data_model.rowsRemoved.connect(model_changed)

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
        self.statusBar().showMessage("Ready...")

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
            about_text = "Version: " + VERSION_NUMBER + "\n\n" + ABOUT_STRING
            about_action.triggered.connect(lambda:
                                           QMessageBox.about(self, "About", about_text))
            help_menu = self.menuBar().addMenu("&Help")
            help_menu.addAction(about_action)

        create_file_menu()
        create_help_menu()

    def project_changed_handler(self):
        """ Updates all the screens with the new project information """
        self.data_model.set_project(self.project)
        for screen in self.selection_screens.values():
            screen.update_project(self.project)
        for screen in self.detail_screens.values():
            screen.update_project(self.project)

        self.project_needs_saving = False
        self.setup_window_title()

    def create_new_project(self):
        """ Creates a new Research Project """
        if self.project_needs_saving:
            button = self.discard_dialog.exec_()
            if button == QMessageBox.Cancel:
                return

        (file_name, _) = QFileDialog.getSaveFileName(
            self, "Create a project", ".", "Grant Project (*.gra)")
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
        self.project_needs_saving = False
        self.setup_window_title()
        self.statusBar().showMessage("Project saved...")

    def save_project_as(self):
        """ Saves the currently loaded project as a new name """
        if self.project is None:
            print("No project to save")
            return

        (file_name, _) = QFileDialog.getSaveFileName(
            self, "Save as ", ".", "Grant Project (*.gra)")
        if file_name == "":
            print("Cancelled saving")
            return

        self.project.filename = file_name
        self.save_project()

        self.project_changed.emit()

    def open_project(self):
        """ Opens an existing project """
        if self.project_needs_saving:
            button = self.discard_dialog.exec_()
            if button == QMessageBox.Cancel:
                return

        (file_name, _) = QFileDialog.getOpenFileName(
            self, "Open a project", ".", "Grant Project (*.gra)")
        if file_name == "":
            print("Cancelled opening")
            return

        self.project = ResearchProject(file_name)
        with open(self.project.filename) as file:
            self.project.from_py(yaml.safe_load(file))

        self.project_changed.emit()
