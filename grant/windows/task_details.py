""" Detail View for a plan """

from PyQt5.QtWidgets import QVBoxLayout, QFormLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QGroupBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QDataWidgetMapper
from .base_screens import DetailScreen


class TaskDetails(DetailScreen):
    """ Displays all current Research Plans """
    plan_changed = pyqtSignal()

    def __init__(self, model):
        super(TaskDetails, self).__init__(model)

        self.status_model = QStringListModel(
            ["active", "completed", "abandoned"])

        form_layout = QFormLayout()
        self.title = QLineEdit()
        form_layout.addRow(QLabel("Title:"), self.title)

        self.description = QTextEdit()
        form_layout.addRow(QLabel("Description:"), self.description)

        self.status = QComboBox()
        self.status.setModel(self.status_model)
        form_layout.addRow(QLabel("Status:"), self.status)

        form_group = QGroupBox("Task")
        form_group.setLayout(form_layout)

        layout = QVBoxLayout()
        layout.addWidget(form_group)

        self.setLayout(layout)

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.data_model)
        self.mapper.addMapping(self.title, 0)
        self.mapper.addMapping(self.description, 1)
        self.mapper.addMapping(self.status, 2, b"currentText")
        self.mapper.toFirst()
