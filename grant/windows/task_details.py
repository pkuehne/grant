""" Detail View for a plan """

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QGroupBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDataWidgetMapper
from .base_screens import DetailScreen


class TaskDetails(DetailScreen):
    """ Displays all current Research Plans """
    plan_changed = pyqtSignal()

    def __init__(self, model):
        super(TaskDetails, self).__init__(model)

        #from PyQt5.QtWidgets import QComboBox
        #from PyQt5.QtCore import QStringListModel
        # self.status_model = QStringListModel(
        #     ["active", "completed", "abandoned"])
        # self.status = QComboBox()
        # self.status.setModel(self.status_model)
        # self.mapper.addMapping(self.status, 2, b"currentText")

        form_layout = QFormLayout()
        self.source = QLineEdit()
        form_layout.addRow(QLabel("Source:"), self.source)

        self.description = QTextEdit()
        form_layout.addRow(QLabel("Description:"), self.description)

        result_box = QHBoxLayout()
        self.result = QLineEdit()
        self.result.setEnabled(False)
        result_box.addWidget(self.result)
        self.result_edit = QPushButton("Edit")
        result_box.addWidget(self.result_edit)
        form_layout.addRow(QLabel("Results:"), result_box)

        form_group = QGroupBox("Task")
        form_group.setLayout(form_layout)

        layout = QVBoxLayout()
        layout.addWidget(form_group)

        self.setLayout(layout)

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.data_model)
        self.mapper.addMapping(self.source, 0)
        self.mapper.addMapping(self.description, 1)
        self.mapper.addMapping(self.result, 2)
        self.mapper.toFirst()
