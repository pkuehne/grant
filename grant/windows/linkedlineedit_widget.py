""" A QLineEdit which can be linked to a gedcom autocomplete """

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMessageBox


class LinkedLineEdit(QLineEdit):
    """ QLineEdit with a linked Gedcom reference """

    link_updated = pyqtSignal(str)

    def __init__(self, model, text_column, pointer_column, parent=None):
        super().__init__(parent)
        self.model = model
        self.pointer_column = pointer_column
        self.text_column = text_column

        self.setup_confirmation_dialog()
        self.setup_action()
        self.setup_completer()

    def setup_action(self):
        """ Sets up the unlink action """
        unlink_tooltip = (
            "This field is linked to an entry in your GEDCOM file "
            + "and will update as your GEDCOM changes. "
            + "Click to break this link."
        )
        self.link_action = QAction(QIcon(":/icons/link.ico"), unlink_tooltip)
        self.link_action.triggered.connect(self.unlink_name)
        self.addAction(self.link_action, self.TrailingPosition)

    def setup_confirmation_dialog(self):
        """ Sets up the break-link confirmation dialog """
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Warning)
        dialog.setWindowIcon(QIcon(":/icons/grant.ico"))
        dialog.setText("This will break the link to your GEDCOM file.")
        dialog.setWindowTitle("Are you sure?")
        dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.confirmation_dialog = dialog

    def setup_completer(self):
        """ Sets up the autocomplete on the ancestor """
        completer = QCompleter()
        completer.setModel(self.model)
        completer.setCompletionRole(Qt.DisplayRole)
        completer.setCompletionColumn(self.text_column)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setFilterMode(Qt.MatchContains)
        # pylint: disable=unsubscriptable-object
        signal = completer.activated[QModelIndex]
        signal.connect(self.autocomplete_activated)
        self.setCompleter(completer)

    def set_link_visible(self, visible: bool):
        """ The index of the selected plan has changed """
        self.link_action.setVisible(visible)
        self.setReadOnly(visible)

    def autocomplete_activated(self, index: QModelIndex):
        """ Called when the autocomplete is activated """
        pointer = index.siblingAtColumn(self.pointer_column).data()
        self.link_updated.emit(pointer)

    def unlink_name(self):
        """ Unlinks the name again """
        button = self.confirmation_dialog.exec_()
        if button == QMessageBox.Cancel:
            return
        self.link_updated.emit("")
