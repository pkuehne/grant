""" Contains the MainWindow implementation """

import os
import yaml
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from grant.research import ResearchProject
from grant.windows.gedcom_manager import GedcomManager
from grant.windows.data_context import DataContext
from grant.windows.project_overview_dialog import ProjectOverviewDialog
from grant.windows.link_updater import LinkUpdater
from .main_window_menu_bar import MenuBar
from .main_screen import MainScreen
from .project_file_manager import ProjectFileManager

TEST_DATA = """
gedcom:
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
        self.data_context = DataContext()
        self.main_screen = None
        self.project_manager = ProjectFileManager(self)
        self.gedcom_manager = GedcomManager(self.data_context, self)
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
                os.path.basename(self.project_manager.project.filename)
            )[0]
            title += "*" if self.project_manager.needs_saving else ""
        else:
            title += " The Genealogical Research AssistaNT"
        self.setWindowTitle(title)

    def setup_window(self):
        """ Sets up all widgets and window stuff """
        self.setWindowIcon(QIcon(":/icons/grant.ico"))

        self.main_screen = MainScreen(self, self.data_context)
        self.setCentralWidget(self.main_screen)

        self.project_manager.project_changed.connect(self.project_changed_handler)
        self.project_manager.project_saved.connect(self.setup_window_title)

        def model_changed():
            self.project_manager.needs_saving = True
            self.setup_window_title()

        self.data_context.data_model.dataChanged.connect(model_changed)
        self.data_context.data_model.layoutChanged.connect(model_changed)
        self.data_context.data_model.rowsRemoved.connect(model_changed)

    def setup_menubar(self):
        """ Sets up the menu bar """
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        self.menu_bar.file_create_new_action.triggered.connect(
            self.project_manager.create_new_project
        )
        self.menu_bar.file_open_project_action.triggered.connect(
            self.project_manager.open_project
        )
        self.menu_bar.file_project_overview_action.triggered.connect(
            lambda: ProjectOverviewDialog.show(
                self.data_context, self.project_manager.project, self
            )
        )
        self.menu_bar.file_save_project_action.triggered.connect(
            self.project_manager.save_project
        )
        self.menu_bar.file_save_project_as_action.triggered.connect(
            self.project_manager.save_project_as
        )
        self.menu_bar.gedcom_link_action.triggered.connect(
            self.project_manager.link_gedcom_file
        )
        self.menu_bar.gedcom_unlink_action.triggered.connect(
            self.project_manager.unlink_gedcom_file
        )
        self.menu_bar.gedcom_refresh_action.triggered.connect(
            lambda: self.gedcom_manager.refresh_link(
                self.project_manager.project.gedcom
            )
        )

        self.menu_bar.view_project_action.triggered.connect(
            lambda: self.main_screen.change_selection_screen("tree")
        )
        self.menu_bar.view_filter_action.triggered.connect(
            lambda: self.main_screen.change_selection_screen("filter")
        )

        def enable_on_project_load():
            self.menu_bar.file_project_overview_action.setDisabled(
                self.project_manager.project is None
            )
            self.menu_bar.file_save_project_action.setDisabled(
                self.project_manager.project is None
            )
            self.menu_bar.file_save_project_as_action.setDisabled(
                self.project_manager.project is None
            )
            self.menu_bar.gedcom_link_action.setDisabled(
                self.project_manager.project is None
            )
            self.menu_bar.gedcom_unlink_action.setDisabled(
                self.project_manager.project is None
                or not self.project_manager.project.has_gedcom()
            )
            self.menu_bar.gedcom_refresh_action.setDisabled(
                self.project_manager.project is None
                or not self.project_manager.project.has_gedcom()
            )

        self.project_manager.project_changed.connect(enable_on_project_load)

    def project_changed_handler(self):
        """ Updates all the screens with the new project information """
        if (
            self.project_manager.project is None
            or self.project_manager.project.gedcom == ""
        ):
            self.gedcom_manager.clear_link()
        else:
            self.gedcom_manager.load_link(self.project_manager.project.gedcom)
        self.data_context.data_model.set_project(self.project_manager.project)
        self.main_screen.set_project(self.project_manager.project)
        updater = LinkUpdater(self.data_context)
        updater.calculate_updates()
        if updater.has_pending_updates():
            updater.commit_updates()
        self.setup_window_title()
