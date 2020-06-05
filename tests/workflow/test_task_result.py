""" Integration test for Research Results """

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QTreeView
from grant.windows.main_window import MainWindow
from grant.windows.result_dialog import ResultDialog


def test_research_result(qtbot, monkeypatch, tmpdir):
    """
    Test Schedule:
    * Create Main Window
    * Create new project
    * Add a Plan
    * Add three tasks
    * Make task 1 nil result
    * Make task 2 success result
    """

    # Setup
    window = MainWindow()
    qtbot.addWidget(window)

    filename = tmpdir.join("new_project.gra").ensure()
    monkeypatch.setattr(
        QFileDialog, "getSaveFileName", lambda _, __, ___, ____: (str(filename), False)
    )

    def plan_index(row: int):
        return window.data_context.data_model.index(
            row, 0, window.data_context.data_model.plans_index
        )

    def task_index(row: int, plan_index):
        return window.data_context.data_model.index(row, 0, plan_index)

    # Begin
    window.show()

    # Create new project
    window.menu_bar.file_create_new_action.trigger()
    assert window.project_manager.project.filename == filename
    assert (
        window.main_screen.selection_stack.currentWidget()
        == window.main_screen.screens["tree"]
    )

    # Add a new plan
    qtbot.mouseClick(window.main_screen.screens["tree"].button_add_plan, Qt.LeftButton)
    assert len(window.project_manager.project.plans) == 1

    # Expand all nodes
    tree_view: QTreeView = window.main_screen.screens["tree"].tree_view
    tree_view.expandAll()

    tree_view.selectionModel().select(
        plan_index(0), QItemSelectionModel.ClearAndSelect,
    )

    # Add first task
    qtbot.mouseClick(window.main_screen.screens["tree"].button_add_task, Qt.LeftButton)
    assert len(window.project_manager.project.plans[0].tasks) == 1

    # Select task
    tree_view.selectionModel().select(
        task_index(0, plan_index(0)), QItemSelectionModel.ClearAndSelect,
    )
    assert (
        window.main_screen.detail_stack.currentWidget()
        == window.main_screen.screens["task"]
    )

    # Press "OK" button on ResultDialog
    def handle_press_ok():
        qtbot.mouseClick(ResultDialog.dialog_reference.ok_button, Qt.LeftButton)

    # Press "Nil" button in result widget
    QTimer.singleShot(50, handle_press_ok)
    qtbot.mouseClick(
        window.main_screen.screens["task"].result.result_nil, Qt.LeftButton
    )

    # Check the result is now nil
    assert window.project_manager.project.plans[0].tasks[0].result.is_nil()

    # Select plan
    tree_view.selectionModel().select(
        plan_index(0), QItemSelectionModel.ClearAndSelect,
    )

    # Add second task
    qtbot.mouseClick(window.main_screen.screens["tree"].button_add_task, Qt.LeftButton)
    assert len(window.project_manager.project.plans[0].tasks) == 2

    # Select task
    tree_view.selectionModel().select(
        task_index(1, plan_index(0)), QItemSelectionModel.ClearAndSelect,
    )
    assert (
        window.main_screen.detail_stack.currentWidget()
        == window.main_screen.screens["task"]
    )

    # Press "Success" button in result widget
    QTimer.singleShot(50, handle_press_ok)
    qtbot.mouseClick(
        window.main_screen.screens["task"].result.result_success, Qt.LeftButton
    )

    # Check the result is now nil
    assert window.project_manager.project.plans[0].tasks[1].result.is_nil() is False
