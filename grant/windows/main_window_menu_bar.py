""" MenuBar for the MainWindow """

import sys
from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMessageBox
from version import MAJOR, MINOR, PATCH


class MenuBar(QMenuBar):
    """ MainWindow MenuBar """

    about_string = "Copyright (c) 2020 by Peter Kühne\nIcons from https://icons8.com"

    def __init__(self, parent):
        super().__init__(parent)
        self.setup_file_menu()
        self.setup_gedcom_menu()
        self.setup_view_menu()
        self.setup_help_menu()

    def setup_file_menu(self):
        """ Create the File menu """
        self.file_create_new_action = QAction("&New Project", self)
        self.file_create_new_action.setShortcut("CTRL+N")

        self.file_open_project_action = QAction("&Open Project", self)
        self.file_open_project_action.setShortcut("CTRL+O")

        self.file_project_overview_action = QAction("&Project Overview", self)
        self.file_project_overview_action.setShortcut("CTRL+P")
        self.file_project_overview_action.setDisabled(True)

        self.file_save_project_action = QAction("&Save Project", self)
        self.file_save_project_action.setShortcut("CTRL+S")
        self.file_save_project_action.setDisabled(True)

        self.file_save_project_as_action = QAction("Save &As ...", self)
        self.file_save_project_as_action.setShortcut("CTRL+A")
        self.file_save_project_as_action.setDisabled(True)

        self.file_quit_action = QAction("&Quit", self)
        self.file_quit_action.setShortcut("CTRL+Q")
        self.file_quit_action.triggered.connect(sys.exit)

        file_menu = self.addMenu("&File")
        file_menu.addAction(self.file_create_new_action)
        file_menu.addAction(self.file_open_project_action)
        file_menu.addAction(self.file_project_overview_action)
        file_menu.addAction(self.file_save_project_action)
        file_menu.addAction(self.file_save_project_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.file_quit_action)

    def setup_gedcom_menu(self):
        """ Create the gedcom menu """
        self.gedcom_link_action = QAction("&Link Gedcom File", self)
        self.gedcom_link_action.setDisabled(True)
        self.gedcom_unlink_action = QAction("&Unlink Gedcom File", self)
        self.gedcom_unlink_action.setDisabled(True)
        self.gedcom_refresh_action = QAction("&Reload Gedcom File", self)
        self.gedcom_refresh_action.setDisabled(True)

        gedcom_menu = self.addMenu("&Gedcom")
        gedcom_menu.addAction(self.gedcom_link_action)
        gedcom_menu.addAction(self.gedcom_unlink_action)
        gedcom_menu.addAction(self.gedcom_refresh_action)

    def setup_view_menu(self):
        """ Create the View menu """
        self.view_project_action = QAction("&Tree View", self)

        self.view_filter_action = QAction("&Filter View", self)

        view_menu = self.addMenu("&View")
        view_menu.addAction(self.view_project_action)
        view_menu.addAction(self.view_filter_action)

    def setup_help_menu(self):
        """ Create the Help menu """
        self.help_about_action = QAction("&About", self)
        about_text = f"Version: {MAJOR}.{MINOR}.{PATCH}\n\n{MenuBar.about_string}"
        self.help_about_action.triggered.connect(
            lambda: QMessageBox.about(self, "About", about_text)
        )
        help_menu = self.addMenu("&Help")
        help_menu.addAction(self.help_about_action)
