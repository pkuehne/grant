""" Class for Tree Selection Screen """

from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QVBoxLayout
from gene.windows.base_screens import SelectionScreen


class TreeSelectionScreen(SelectionScreen):
    """ Shows all plans and tasks in a tree view """

    def __init__(self):
        super(TreeSelectionScreen, self).__init__()

        def not_implemented():
            raise NotImplementedError

        self.plan_model = QStandardItemModel()
        self.plan_model.setHorizontalHeaderLabels(["Plan", "Open Tasks"])
        self.plan_table = QTableView()
        self.plan_table.setModel(self.plan_model)
        self.plan_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.plan_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.plan_table.verticalHeader().hide()
        self.plan_table.doubleClicked.connect(not_implemented)
        self.plan_table.selectionModel().selectionChanged.connect(not_implemented)

        layout = QVBoxLayout()
        layout.addWidget(self.plan_table)

        self.setLayout(layout)
