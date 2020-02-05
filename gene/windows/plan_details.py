""" Detail View for a plan """

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton, QGroupBox
# from PyQt5.QtWidgets import QTableView, QAbstractItemView
# from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSignal
from gene.research import ResearchProject, ResearchPlan
from .task_overview import TaskOverview


class PlanDetails(QWidget):
    """ Displays all current Research Plans """
    close_clicked = pyqtSignal()
    plan_changed = pyqtSignal()

    def __init__(self):
        super(PlanDetails, self).__init__()
        self.project = None
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

        self.tasks = TaskOverview()
        task_layout = QVBoxLayout()
        task_layout.addWidget(self.tasks)

        task_group = QGroupBox("Tasks")
        task_group.setLayout(task_layout)

        self.close_button = QPushButton()
        self.close_button.setText("Close")
        self.close_button.pressed.connect(self.close_clicked.emit)

        button_box = QHBoxLayout()
        button_box.addStretch()
        button_box.addWidget(self.close_button)

        layout = QVBoxLayout()
        layout.addWidget(form_group)
        layout.addWidget(task_group)
        layout.addLayout(button_box)

        self.setLayout(layout)

    def load_project(self, project: ResearchProject):
        """ Slot for when project changes """
        self.project = project

    def select_plan(self, index: int):
        """ Slot for when the selected plan changes """
        if self.project is None:
            return

        self.index = index
        plan: ResearchPlan = self.project.plans[self.index]
        print("Selecting " + str(index) + " -> " + str(plan))
        self.title.setText(plan.title)
        self.goal.setText(plan.goal)
        self.tasks.load_plan(plan)

    def save_plan(self):
        """ Save the plan """
        plan = self.project.plans[self.index]
        plan.title = self.title.text()
        plan.goal = self.goal.document().toPlainText()
        self.plan_changed.emit()
