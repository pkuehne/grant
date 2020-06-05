""" Common test fixtures """

import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from grant.windows.main_window import MainWindow
from grant.windows.result_dialog import ResultDialog


class WindowDriver:
    """ Test class automating common steps """

    def __init__(self, qtbot, monkeypatch):
        self.window = MainWindow()
        self.qtbot = qtbot
        self.monkeypatch = monkeypatch

    def project(self):
        """ Returns a reference to the project """
        return self.window.project_manager.project

    def _plan_index(self, row: int):
        """ Returns QModelIndex for given Plan """
        return self.window.data_context.data_model.index(
            row, 0, self.window.data_context.data_model.plans_index
        )

    def _task_index(self, row: int, plan_index):
        """ Returns QModelIndex for given Task within given Plan """
        return self.window.data_context.data_model.index(row, 0, plan_index)

    def create_new_project(self, filename):
        """ Creates a new project """
        self.monkeypatch.setattr(
            QFileDialog,
            "getSaveFileName",
            lambda _, __, ___, ____: (str(filename), False),
        )
        self.window.menu_bar.file_create_new_action.trigger()
        assert self.window.project_manager.project.filename == filename
        assert (
            self.window.main_screen.selection_stack.currentWidget()
            == self.window.main_screen.screens["tree"]
        )

    def link_gedcom(self, filename):
        """ Creates a new project """
        self.monkeypatch.setattr(
            QFileDialog,
            "getOpenFileName",
            lambda _, __, ___, ____: (str(filename), False),
        )
        self.window.menu_bar.gedcom_link_action.trigger()
        assert self.window.project_manager.project.gedcom == filename

    def unlink_gedcom(self):
        """ Unlinks a gedcom again """
        self.monkeypatch.setattr(
            self.window.project_manager.gedcom_discard, "exec_", lambda: QMessageBox.Ok
        )
        self.window.menu_bar.gedcom_unlink_action.trigger()
        assert self.window.project_manager.project.gedcom == ""

    def add_plan(self):
        """ Adds a new plan """
        previous_plan_count = len(self.window.project_manager.project.plans)
        self.qtbot.mouseClick(
            self.window.main_screen.screens["tree"].button_add_plan, Qt.LeftButton
        )
        new_plan_count = len(self.window.project_manager.project.plans)
        assert new_plan_count == previous_plan_count + 1

    def select_plan(self, plan_id: int):
        """ Select a plan in the tree view """
        tree_view: QTreeView = self.window.main_screen.screens["tree"].tree_view
        tree_view.expandAll()
        tree_view.selectionModel().select(
            self._plan_index(plan_id), QItemSelectionModel.ClearAndSelect,
        )
        assert (
            self.window.main_screen.detail_stack.currentWidget()
            == self.window.main_screen.screens["plan"]
        )

    def select_task(self, plan_id: int, task_id: int):
        """" Select a task in the tree view """
        tree_view: QTreeView = self.window.main_screen.screens["tree"].tree_view
        tree_view.selectionModel().select(
            self._task_index(task_id, self._plan_index(plan_id)),
            QItemSelectionModel.ClearAndSelect,
        )
        assert (
            self.window.main_screen.detail_stack.currentWidget()
            == self.window.main_screen.screens["task"]
        )

    def add_task(self, plan_id: int):
        """ Adds a task to the plan """
        previous_task_count = len(
            self.window.project_manager.project.plans[plan_id].tasks
        )
        self.qtbot.mouseClick(
            self.window.main_screen.screens["tree"].button_add_task, Qt.LeftButton
        )
        new_task_count = len(self.window.project_manager.project.plans[plan_id].tasks)
        assert new_task_count == previous_task_count + 1

    def press_button_in_result_widget(self, button: str, callback=None):
        """ Pressed the nil button in the result widget """
        assert (
            self.window.main_screen.detail_stack.currentWidget()
            == self.window.main_screen.screens["task"]
        )
        # Press "OK" button on ResultDialog
        def handle_press_ok():
            if callback is not None:
                callback()
            self.qtbot.mouseClick(
                ResultDialog.dialog_reference.ok_button, Qt.LeftButton
            )

        # Press "Nil" button in result widget
        QTimer.singleShot(50, handle_press_ok)
        self.qtbot.mouseClick(
            getattr(self.window.main_screen.screens["task"].result, button),
            Qt.LeftButton,
        )


@pytest.fixture
def window_driver(qtbot, monkeypatch):
    """ Create a main_window """
    driver = WindowDriver(qtbot, monkeypatch)
    qtbot.addWidget(driver.window)
    driver.window.show()
    return driver
