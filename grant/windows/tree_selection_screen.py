""" Class for Tree Selection Screen """

from PyQt5.QtWidgets import QTreeView
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from .base_screens import SelectionScreen


class TreeSelectionScreen(SelectionScreen):
    """ Shows all plans and tasks in a tree view """

    def __init__(self, model):
        super(TreeSelectionScreen, self).__init__(model)

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.data_context.data_model)
        self.tree_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tree_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tree_view.selectionModel().selectionChanged.connect(self.selection_changed)
        self.tree_view.hideColumn(1)
        self.tree_view.hideColumn(2)
        self.tree_view.hideColumn(3)

        self.button_add_plan = QPushButton()
        self.button_add_plan.setText("Add Plan")
        self.button_add_plan.setIcon(QIcon(":/icons/plan.ico"))
        self.button_add_plan.setDisabled(True)
        self.button_add_plan.pressed.connect(self.add_plan)
        self.button_add_task = QPushButton()
        self.button_add_task.setText("Add Task")
        self.button_add_task.setIcon(QIcon(":/icons/task.ico"))
        self.button_add_task.setDisabled(True)
        self.button_add_task.pressed.connect(self.add_task)
        self.button_delete_selection = QPushButton()
        self.button_delete_selection.setText("Delete")
        self.button_delete_selection.setIcon(QIcon(":/icons/delete.ico"))
        self.button_delete_selection.setDisabled(True)
        self.button_delete_selection.pressed.connect(self.delete_selection)

        button_box = QHBoxLayout()
        button_box.addWidget(self.button_add_plan)
        button_box.addWidget(self.button_add_task)
        button_box.addWidget(self.button_delete_selection)

        layout = QVBoxLayout()
        layout.addWidget(self.tree_view)
        layout.addLayout(button_box)

        self.setLayout(layout)

    def reload_screen(self):
        """ Called when project changes """
        self.button_add_plan.setDisabled(self.project is None)

    def selection_changed(self, selected, _):
        """ Handle changed selection """
        if len(selected.indexes()) < 1:
            return
        index = selected.indexes()[0]
        self.item_selected.emit(index)

        node = index.internalPointer()
        self.button_add_task.setEnabled(node.type == "plan")
        self.button_delete_selection.setEnabled(
            node.type == "plan" or node.type == "task"
        )

    def delete_selection(self):
        """ Deletes the selected row if valid """
        if len(self.tree_view.selectedIndexes()) == 0:
            return
        self.data_context.data_model.delete_node(self.tree_view.selectedIndexes()[0])

    def add_plan(self):
        """ Create a new plan in the project """
        self.data_context.data_model.add_node(self.data_context.data_model.plans_index)

    def add_task(self):
        """ Create a new task in the project """
        if len(self.tree_view.selectedIndexes()) == 0:
            return
        self.data_context.data_model.add_node(self.tree_view.selectedIndexes()[0])

    def clear_selection(self):
        """ Called when screen is being switched to """
        self.tree_view.selectionModel().clearSelection()
