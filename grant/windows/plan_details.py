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
        form_layout.addRow(QLabel("Ancestor:"), self.title)

        self.goal = QTextEdit()
        form_layout.addRow(QLabel("Goal:"), self.goal)

        form_group = QGroupBox("Plan")
        form_group.setLayout(form_layout)

        layout = QVBoxLayout()
        layout.addWidget(form_group)

        self.setLayout(layout)

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.data_model)
        self.mapper.addMapping(self.title, 0)
        self.mapper.addMapping(self.goal, 1)
        self.mapper.toFirst()
