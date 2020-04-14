""" A custom widget to display a ResearchResult """

from PyQt5.QtCore import pyqtProperty
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from grant.research import ResearchResult
from .result_dialog import ResultDialog


class ResultWidget(QWidget):
    """ A widget to display results """

    result_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._result = None

        result_box = QHBoxLayout()
        result_box.setContentsMargins(0, 0, 0, 0)

        self.textbox = QLineEdit(self)
        self.textbox.setReadOnly(True)
        self.more_action = QAction(QIcon(":/icons/more.ico"), "more")
        self.more_action.triggered.connect(self.show_result_dialog)
        self.textbox.addAction(self.more_action, self.textbox.TrailingPosition)
        result_box.addWidget(self.textbox)

        self.result_nil = QPushButton("Nil")
        self.result_nil.pressed.connect(lambda: self.record_result(False))
        result_box.addWidget(self.result_nil)
        self.result_success = QPushButton("Success")
        self.result_success.pressed.connect(lambda: self.record_result(True))
        result_box.addWidget(self.result_success)

        self.setLayout(result_box)

    @pyqtProperty(QObject, user=True, notify=result_changed)
    def result(self):
        """ Result property getter """
        return self._result

    @result.setter
    def result(self, value):
        """ Result property setter """
        self._result = value
        self.textbox.setText(str(self._result))
        self.textbox.setVisible(self._result is not None)
        self.result_nil.setVisible(self._result is None)
        self.result_success.setVisible(self._result is None)

    def record_result(self, success: bool):
        """ Records a result """
        self._result = ResearchResult(success)
        self.show_result_dialog()

    def show_result_dialog(self):
        """ Opens the result dialog """
        dialog = ResultDialog(self._result)
        dialog.summary.setFocus()
        if dialog.exec():
            self.result = dialog.result
            self.result_changed.emit()
