""" Class for Tree Selection Screen """

from PyQt5.QtWidgets import QTreeView
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from gene.windows.base_screens import SelectionScreen


class TreeSelectionScreen(SelectionScreen):
    """ Shows all plans and tasks in a tree view """

    def __init__(self, model):
        super(TreeSelectionScreen, self).__init__(model)

        self.plan_table = QTreeView()
        self.plan_table.setModel(self.data_model)
        self.plan_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.plan_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.plan_table.selectionModel().selectionChanged.connect(self.selection_changed)
        self.plan_table.hideColumn(1)

        self.button_add_plan = QPushButton()
        self.button_add_plan.setText("Add Plan")
        self.button_add_plan.setIcon(QIcon("icons/plan.ico"))
        self.button_add_task = QPushButton()
        self.button_add_task.setText("Add Task")
        self.button_add_task.setIcon(QIcon("icons/task.ico"))
        self.button_add_task.setDisabled(True)
        self.button_delete_selection = QPushButton()
        self.button_delete_selection.setText("Delete")
        self.button_delete_selection.setIcon(QIcon("icons/delete.ico"))
        self.button_delete_selection.setDisabled(True)

        button_box = QHBoxLayout()
        button_box.addWidget(self.button_add_plan)
        button_box.addWidget(self.button_add_task)
        button_box.addWidget(self.button_delete_selection)

        layout = QVBoxLayout()
        layout.addWidget(self.plan_table)
        layout.addLayout(button_box)

        self.setLayout(layout)

    def selection_changed(self, selected, _):
        """ Handle changed selection """
        if len(selected.indexes()) != 1:
            return
        index = selected.indexes()[0]
        self.item_selected.emit(index)

        node = index.internalPointer()
        self.button_add_task.setEnabled(node.type == "plan")
        self.button_delete_selection.setEnabled(
            node.type == "plan" or node.type == "task")
