""" Detail View for a plan """

from PyQt5.QtWidgets import QVBoxLayout, QFormLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QGroupBox
# from PyQt5.QtWidgets import QTableView, QAbstractItemView
# from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSignal
from gene.research import ResearchPlan
from .base_screens import DetailScreen


class PlanDetails(DetailScreen):
    """ Displays all current Research Plans """
    close_clicked = pyqtSignal()
    plan_changed = pyqtSignal()

    def __init__(self):
        super(PlanDetails, self).__init__()
        self.index = 0

        form_layout = QFormLayout()
        self.title = QLineEdit()
        self.title.editingFinished.connect(self.save_plan)
        form_layout.addRow(QLabel("Title:"), self.title)

        self.goal = QTextEdit()
        self.goal.textChanged.connect(self.save_plan)
        form_layout.addRow(QLabel("Goal:"), self.goal)

        form_group = QGroupBox("Details")
        form_group.setLayout(form_layout)

        layout = QVBoxLayout()
        layout.addWidget(form_group)

        self.setLayout(layout)

    def set_selected_item(self, item):
        """ Receive selected item from main window """
        if self.project is None:
            return

        self.index = item["plan"]
        plan: ResearchPlan = self.project.plans[self.index]
        print("Selecting " + str(self.index) + " -> " + str(plan))
        self.title.setText(plan.title)
        self.goal.setText(plan.goal)

    def save_plan(self):
        """ Save the plan """
        plan = self.project.plans[self.index]
        plan.title = self.title.text()
        plan.goal = self.goal.document().toPlainText()
        self.plan_changed.emit()
