""" Detail View for a plan """

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QGroupBox
from PyQt5.QtWidgets import QDataWidgetMapper
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from grant.windows.base_screens import DetailScreen
from grant.windows.result_widget import ResultWidget
from grant.models.sources_model import SourcesModelColumns
from grant.models.tree_model import TreeModelCols


class TaskDetails(DetailScreen):
    """ Displays all current Research Plans """

    def __init__(self, data_context):
        super().__init__(data_context)

        unlink_tooltip = (
            "This source is linked to an entry in your GEDCOM "
            + "and will update as the source name in your gedcom changes. "
            + "Click to break this link."
        )
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
        # pylint: disable=unsubscriptable-object
        signal = completer.activated[QModelIndex]
        signal.connect(self.autocomplete_activated)
        self.source.setCompleter(completer)
        self.link_action = QAction(QIcon(":/icons/link.ico"), unlink_tooltip)
        self.link_action.triggered.connect(self.unlink_name)
        self.source.addAction(self.link_action, self.source.TrailingPosition)

        self.description = QTextEdit()
        form_layout.addRow(QLabel("Description:"), self.description)

        self.result = ResultWidget()
        form_layout.addRow(QLabel("Results:"), self.result)

        form_group = QGroupBox("Task")
        form_group.setLayout(form_layout)

        layout = QVBoxLayout()
        layout.addWidget(form_group)

        self.link = QLineEdit()
        # Don't add this, we just want to get/set the value
        self.setup_confirmation_dialog()

        self.setLayout(layout)

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.data_context.data_model)
        self.mapper.addMapping(self.source, TreeModelCols.TEXT)
        self.mapper.addMapping(
            self.description, TreeModelCols.DESCRIPTION, b"plainText"
        )
        self.mapper.addMapping(self.result, TreeModelCols.RESULT)
        self.mapper.addMapping(self.link, TreeModelCols.LINK)
        self.result.result_changed.connect(self.mapper.submit)
        self.mapper.currentIndexChanged.connect(self.index_changed)
        self.data_context.data_model.dataChanged.connect(
            lambda index, _: self.index_changed(index)
        )
        self.mapper.toFirst()

    def setup_confirmation_dialog(self):
        """ Sets up the break-link confirmation dialog """
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Warning)
        dialog.setWindowIcon(QIcon(":/icons/grant.ico"))
        dialog.setText("This will break the link to your GEDCOM file.")
        dialog.setWindowTitle("Are you sure?")
        dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.confirmation_dialog = dialog

    def index_changed(self, _):
        """ The index of the selected plan has changed """
        self.link_action.setVisible(self.link.text() != "")

    def autocomplete_activated(self, index: QModelIndex):
        """ Called when the autocomplete is activated """
        self.link.setText(index.siblingAtColumn(SourcesModelColumns.POINTER).data())
        self.mapper.submit()

    def unlink_name(self):
        """ Unlinks the name again """
        button = self.confirmation_dialog.exec_()
        if button == QMessageBox.Cancel:
            return
        self.link.setText("")
        self.mapper.submit()
