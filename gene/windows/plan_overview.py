""" Widget to show Research Plans """

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWidgets import QTableView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSignal
from gene.research import ResearchProject  # , ResearchPlan


class PlanOverview(QWidget):
    """ Displays all current Research Plans """

    plan_selected = pyqtSignal(int)

    def __init__(self):
        super(PlanOverview, self).__init__()
        self.project: ResearchProject = None
        self.plan_model = QStandardItemModel()
        self.plan_model.setHorizontalHeaderLabels(["Plan", "Open Tasks"])
        self.plan_table = QTableView()
        self.plan_table.setModel(self.plan_model)
        self.plan_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.plan_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.plan_table.verticalHeader().hide()
        self.plan_table.doubleClicked.connect(self.select_plan)

        layout = QVBoxLayout()
        layout.addWidget(self.plan_table)

        self.setLayout(layout)

    def load_project(self, project: ResearchProject):
        """ Slot for when project changes """
        self.project = project
        self.populate_plan_table()

    def populate_plan_table(self):
        """ Populates the plan table with all plans """
        print("populate_plan_table called")
        if self.project is None:
            return

        self.plan_model.clear()
        for plan in self.project.plans:
            row = []
            row.append(QStandardItem(plan.title))
            row.append(QStandardItem(str(len(plan.tasks))))
            self.plan_model.appendRow(row)

    def select_plan(self, index):
        """ Double-click on row, open up plan """
        # print(self.plan_model.data(index.siblingAtColumn(0)))
        print(self.project.plans[index.row()])
        self.plan_selected.emit(index.row())
