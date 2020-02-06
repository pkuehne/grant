""" Detail View for a plan """

from PyQt5.QtWidgets import QVBoxLayout, QFormLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QGroupBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDataWidgetMapper
from .base_screens import DetailScreen


class PlanDetails(DetailScreen):
    """ Displays all current Research Plans """
    plan_changed = pyqtSignal()

    def __init__(self, model):
        super(PlanDetails, self).__init__(model)

        form_layout = QFormLayout()
        self.title = QLineEdit()
        # self.title.editingFinished.connect(self.save_plan)
        form_layout.addRow(QLabel("Title:"), self.title)

        self.goal = QTextEdit()
        # self.goal.textChanged.connect(self.save_plan)
        form_layout.addRow(QLabel("Goal:"), self.goal)

        form_group = QGroupBox("Details")
        form_group.setLayout(form_layout)

        layout = QVBoxLayout()
        layout.addWidget(form_group)

        self.setLayout(layout)

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.data_model)
        self.mapper.addMapping(self.goal, 0)
        self.mapper.toLast()

    def set_selected_item(self, item):
        """ Receive selected item from main window """
        if self.project is None:
            return
        print("Setting mapper model index " +
              str(item.row()) + " " + str(item.column()))
        # self.mapper.setCurrentModelIndex(item)
        self.mapper.toLast()

    def save_plan(self):
        """ Save the plan """
        plan = self.project.plans[self.index]
        plan.title = self.title.text()
        plan.goal = self.goal.document().toPlainText()
        self.plan_changed.emit()
