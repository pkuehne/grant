""" MenuBar for the MainWindow """

import sys
from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMessageBox


class MenuBar(QMenuBar):
    """ MainWindow MenuBar """
    about_string = "Copyright (c) 2020 by Peter Kühne\nIcons from https://icons8.com"
    version_number = "0.1"

    def __init__(self, parent):
        super().__init__(parent)
        self.setup_file_menu()
        self.setup_view_menu()
        self.setup_help_menu()

    def setup_file_menu(self):
        """ Create the File menu """
        self.file_create_new_action = QAction("&New Project", self)
        self.file_create_new_action.setShortcut("CTRL+N")

        self.file_open_project_action = QAction("&Open Project", self)
        self.file_open_project_action.setShortcut("CTRL+O")

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
        file_menu.addAction(self.file_save_project_action)
        file_menu.addAction(self.file_save_project_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.file_quit_action)

    def setup_view_menu(self):
        """ Create the View menu """
        self.view_project_action = QAction("Project &Overview", self)

        self.view_filter_action = QAction("Tasks Filter", self)

        view_menu = self.addMenu("&View")
        view_menu.addAction(self.view_project_action)
        view_menu.addAction(self.view_filter_action)

    def setup_help_menu(self):
        """ Create the Help menu """
        self.help_about_action = QAction("&About", self)
        about_text = "Version: " + MenuBar.version_number + "\n\n" + MenuBar.about_string
        self.help_about_action.triggered.connect(lambda:
                                                 QMessageBox.about(self, "About", about_text))
        help_menu = self.addMenu("&Help")
        help_menu.addAction(self.help_about_action)
