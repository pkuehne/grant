""" Widget to show Research Plans """

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtWidgets import QTableView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSignal
from gene.research import ResearchProject, ResearchPlan
from gene.windows.base_screens import DetailSecreen


class PlanOverview(DetailSecreen):
    """ Displays all current Research Plans """

    plan_edited = pyqtSignal(int)
    plan_deleted = pyqtSignal()
    plan_added = pyqtSignal(int)

    def __init__(self):
        super(PlanOverview, self).__init__()
        self.plan_model = QStandardItemModel()
        self.plan_model.setHorizontalHeaderLabels(["Plan", "Open Tasks"])
        self.plan_table = QTableView()
        self.plan_table.setModel(self.plan_model)
        self.plan_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.plan_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.plan_table.verticalHeader().hide()
        self.plan_table.doubleClicked.connect(self.edit_plan)
        self.plan_table.selectionModel().selectionChanged.connect(self.selection_changed)

        self.add_button = QPushButton()
        self.add_button.setText("Add")
        self.add_button.setDisabled(True)
        self.add_button.pressed.connect(self.add_plan)
        self.edit_button = QPushButton()
        self.edit_button.setText("Edit")
        self.edit_button.setDisabled(True)
        self.edit_button.pressed.connect(lambda: self.edit_plan(
            self.plan_table.selectionModel().selectedIndexes()[0]))
        self.delete_button = QPushButton()
        self.delete_button.setText("Delete")
        self.delete_button.setDisabled(True)
        self.delete_button.pressed.connect(lambda: self.delete_plan(
            self.plan_table.selectionModel().selectedIndexes()[0]))

        button_box = QVBoxLayout()
        button_box.addWidget(self.add_button)
        button_box.addWidget(self.edit_button)
        button_box.addWidget(self.delete_button)
        button_box.addStretch()

        layout = QHBoxLayout()
        layout.addWidget(self.plan_table)
        layout.addLayout(button_box)

        self.setLayout(layout)

    def update_project(self, project: ResearchProject):
        """ Slot for when project changes """
        super(PlanOverview, self).update_project(project)
        self.load_plans()

    def load_plans(self):
        """ Populates the plan table with all plans """
        self.add_button.setDisabled(self.project is None)
        if self.project is None:
            return

        self.plan_model.setRowCount(0)
        for plan in self.project.plans:
            row=[]
            row.append(QStandardItem(plan.title))
            row.append(QStandardItem(str(len(plan.tasks))))
            self.plan_model.appendRow(row)

    def edit_plan(self, index):
        """ Double-click on row, open up plan """
        # print(self.plan_model.data(index.siblingAtColumn(0)))
        self.plan_edited.emit(index.row())

    def add_plan(self):
        """ Add a new plan """
        self.project.plans.append(ResearchPlan())
        self.load_plans()
        self.plan_added.emit(len(self.project.plans)-1)

    def delete_plan(self, index):
        """ Delete the selected plan """
        del self.project.plans[index.row()]
        self.plan_table.selectionModel().clearSelection()
        self.load_plans()
        self.plan_deleted.emit()

    def selection_changed(self, selected, _):
        """ Handle changed selection """
        self.edit_button.setEnabled(selected.count())
        self.delete_button.setEnabled(selected.count())
