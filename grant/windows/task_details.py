""" Detail View for a plan """

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QGroupBox
from PyQt5.QtWidgets import QDataWidgetMapper
from PyQt5.QtWidgets import QCompleter
from grant.windows.base_screens import DetailScreen
from grant.windows.result_widget import ResultWidget
from grant.models.sources_model import SourcesModelColumns


class TaskDetails(DetailScreen):
    """ Displays all current Research Plans """

    def __init__(self, data_context):
        super().__init__(data_context)

        form_layout = QFormLayout()
        self.source = QLineEdit()
        form_layout.addRow(QLabel("Source:"), self.source)
        completer = QCompleter()
        completer.setModel(self.data_context.sources_model)
        completer.setCompletionRole(Qt.DisplayRole)
        completer.setCompletionColumn(SourcesModelColumns.AUTOCOMPLETE)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setFilterMode(Qt.MatchContains)
        self.source.setCompleter(completer)

        self.description = QTextEdit()
        form_layout.addRow(QLabel("Description:"), self.description)

        self.result = ResultWidget()
        form_layout.addRow(QLabel("Results:"), self.result)

        form_group = QGroupBox("Task")
        form_group.setLayout(form_layout)

        layout = QVBoxLayout()
        layout.addWidget(form_group)

        self.setLayout(layout)

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.data_context.data_model)
        self.mapper.addMapping(self.source, 0)
        self.mapper.addMapping(self.description, 1)
        self.mapper.addMapping(self.result, 2)
        self.result.result_changed.connect(self.mapper.submit)
        self.mapper.toFirst()
