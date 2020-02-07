""" Class for Tree Selection Screen """

from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QVBoxLayout
from grant.windows.base_screens import SelectionScreen


class FilterSelectionScreen(SelectionScreen):
    """ Shows all plans and tasks in a tree view """

    def __init__(self, model):
        super(FilterSelectionScreen, self).__init__(model)

        self.plan_model = QStandardItemModel()
        self.plan_model.setHorizontalHeaderLabels(["Plan", "Open Tasks"])
        self.plan_table = QTableView()
        self.plan_table.setModel(self.plan_model)
        self.plan_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.plan_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.plan_table.verticalHeader().hide()
        self.plan_table.selectionModel().selectionChanged.connect(self.selection_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.plan_table)

        self.setLayout(layout)

    def reload_screen(self):
        """ Loads the screen """
        self.plan_model.setRowCount(0)
        for plan in self.project.plans:
            row = []
            row.append(QStandardItem(plan.title))
            row.append(QStandardItem(str(len(plan.tasks))))
            self.plan_model.appendRow(row)

    def selection_changed(self, selected, _):
        """ Handle changed selection """
        item = {
            # "plan": self.plan_table.selectionModel().selectedIndexes()[0].row()
            "plan": selected.indexes()[0].row()
        }
        self.item_selected.emit(item)
