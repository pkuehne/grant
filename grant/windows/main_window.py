""" Contains the MainWindow implementation """

import os
import yaml
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import pyqtSignal
from grant.research import ResearchProject
from grant.models.tree_model import TreeModel
from .main_window_menu_bar import MenuBar
from .main_screen import MainScreen
from .project_file_manager import ProjectFileManager

TEST_DATA = """
gedcom: none
plans:
- goal: Identify any bastard children
  tasks:
  - source: Granthill Church Books, Baptisms 1810-1837
    description: Check for any bastards born at this time to a Maria
    result:
        nil: true
        summary: "nothing found"
  - source: Granthill Church Books, Baptisms 1838-1855
    description: Check for any bastards born at this time to a Maria
    result:
  ancestor: William Fitzhugh (1801-1854)
- goal: Another test plan
  tasks: []
  ancestor: Guillaume Demarre (1765-1808)
version: '1.0'
"""


class MainWindow(QMainWindow):
    """ The Main Window where we start """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.data_model = TreeModel()
        self.main_screen = None
        self.project_manager = ProjectFileManager(self)
        self.setup_window()
        self.setup_window_title()
        self.setup_menubar()

        if os.getenv("GRANT_TEST", "") != "":
            self.project_manager.project = ResearchProject("test_data")
            self.project_manager.project.from_py(yaml.safe_load(TEST_DATA))
            self.project_manager.project_changed.emit()

    def setup_window_title(self):
        """ Sets the window title from project name """
        title = "Grant - "
        if self.project_manager.project is not None:
            title += os.path.splitext(
                os.path.basename(self.project_manager.project.filename))[0]
            title += "*" if self.project_manager.needs_saving else ""
        else:
            title += " The Genealogical Research AssistaNT"
        self.setWindowTitle(title)

    def setup_window(self):
        """ Sets up all widgets and window stuff """
        self.setWindowIcon(QIcon(":/icons/books.ico"))

        self.main_screen = MainScreen(self, self.data_model)
        self.setCentralWidget(self.main_screen)

        self.project_manager.project_changed.connect(
            self.project_changed_handler)
        self.project_manager.project_saved.connect(self.setup_window_title)

        def model_changed():
            self.project_manager.needs_saving = True
            self.setup_window_title()
        self.data_model.dataChanged.connect(model_changed)
        self.data_model.layoutChanged.connect(model_changed)
        self.data_model.rowsRemoved.connect(model_changed)

    def setup_menubar(self):
        """ Sets up the menu bar """
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        self.menu_bar.file_create_new_action.triggered.connect(
            self.project_manager.create_new_project)
        self.menu_bar.file_open_project_action.triggered.connect(
            self.project_manager.open_project)
        self.menu_bar.file_save_project_action.triggered.connect(
            self.project_manager.save_project)
        self.menu_bar.file_save_project_as_action.triggered.connect(
            self.project_manager.save_project_as)

        self.menu_bar.view_project_action.triggered.connect(
            lambda: self.main_screen.change_selection_screen("tree"))
        self.menu_bar.view_filter_action.triggered.connect(
            lambda: self.main_screen.change_selection_screen("filter"))

        def enable_on_project_load():
            self.menu_bar.file_save_project_action.setDisabled(
                self.project_manager.project is None)
            self.menu_bar.file_save_project_as_action.setDisabled(
                self.project_manager.project is None)
        self.project_manager.project_changed.connect(enable_on_project_load)

    def project_changed_handler(self):
        """ Updates all the screens with the new project information """
        self.data_model.set_project(self.project_manager.project)
        self.main_screen.set_project(self.project_manager.project)

        self.setup_window_title()
