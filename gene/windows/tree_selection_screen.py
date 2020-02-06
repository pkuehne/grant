""" Class for Tree Selection Screen """

from PyQt5.QtWidgets import QTreeView
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QVBoxLayout
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

        layout = QVBoxLayout()
        layout.addWidget(self.plan_table)

        self.setLayout(layout)

    def selection_changed(self, selected, _):
        """ Handle changed selection """
        if len(selected.indexes()) != 1:
            return
        self.item_selected.emit(selected.indexes()[0])
