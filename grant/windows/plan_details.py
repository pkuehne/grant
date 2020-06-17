""" Detail View for a plan """

from PyQt5.QtWidgets import QVBoxLayout, QFormLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QGroupBox
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtWidgets import QDataWidgetMapper
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from grant.windows.base_screens import DetailScreen
from grant.models.individuals_model import IndividualsModelColumns
from grant.models.tree_model import TreeModelCols


class PlanDetails(DetailScreen):
    """ Displays all current Research Plans """

    plan_changed = pyqtSignal()

    def __init__(self, data_context):
        super(PlanDetails, self).__init__(data_context)

        form_layout = QFormLayout()
        self.ancestor = QLineEdit()
        form_layout.addRow(QLabel("Ancestor:"), self.ancestor)
        completer = QCompleter()
        completer.setModel(self.data_context.individuals_model)
        completer.setCompletionRole(Qt.DisplayRole)
        completer.setCompletionColumn(IndividualsModelColumns.AUTOCOMPLETE)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setFilterMode(Qt.MatchContains)
        self.ancestor.setCompleter(completer)

        self.goal = QTextEdit()
        form_layout.addRow(QLabel("Goal:"), self.goal)

        form_group = QGroupBox("Plan")
        form_group.setLayout(form_layout)

        layout = QVBoxLayout()
        layout.addWidget(form_group)

        self.setLayout(layout)

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.data_context.data_model)
        self.mapper.addMapping(self.ancestor, TreeModelCols.TEXT)
        self.mapper.addMapping(self.goal, TreeModelCols.DESCRIPTION, b"plainText")
        self.mapper.toFirst()
