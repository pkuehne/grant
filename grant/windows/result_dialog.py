""" A window to edit the ResearchResult of a ResearchTask """

import datetime
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtCore import QStringListModel, QDate
from grant.research import ResearchResult


class ResultDialog(QDialog):
    """Edit a given Result"""

    dialog_reference = None

    def __init__(self, result: ResearchResult, parent=None):
        super(ResultDialog, self).__init__(parent)
        self.result = result

        self.setWindowTitle("Task Result")

        form_layout = QFormLayout()

        self.status = QComboBox()
        status_model = QStringListModel(["<remove>", "success", "nil"])
        self.status.setModel(status_model)
        form_layout.addRow(QLabel("Result:"), self.status)
        self.completed = QDateEdit()
        form_layout.addRow(QLabel("Date:"), self.completed)
        self.summary = QTextEdit()
        form_layout.addRow(QLabel("Summary:"), self.summary)
        self.document = QLineEdit()
        form_layout.addRow(QLabel("Document:"), self.document)

        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.pressed.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        self.ok_button = QPushButton("OK")
        self.ok_button.pressed.connect(self.ok_pressed)
        button_layout.addWidget(self.ok_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        if self.result is not None:
            self.completed.setDate(self.result.date)
            self.status.setCurrentText("nil" if self.result.is_nil() else "success")
            self.summary.setText(self.result.summary)
            self.document.setText(self.result.document)
        else:
            self.completed.setDate(QDate.currentDate())
            self.status.setCurrentText("<remove>")

    def ok_pressed(self):
        """Triggered when the OK button is pressed"""
        if self.status.currentText() == "<remove>":
            self.result = None
        else:
            success = self.status.currentText() == "success"
            if self.result is None:
                self.result = ResearchResult(success)
            self.result.summary = self.summary.toPlainText()
            self.result.document = self.document.text()
            self.result.nil = success is False
            self.result.date = datetime.date(
                self.completed.date().year(),
                self.completed.date().month(),
                self.completed.date().day(),
            )

        self.accept()

    @classmethod
    def get_result(cls, result, parent):
        """Wraps the creation of the dialog, particularly for unit testing"""
        ResultDialog.dialog_reference = cls(result, parent)
        ResultDialog.dialog_reference.summary.setFocus()
        ResultDialog.dialog_reference.exec_()
        result = ResultDialog.dialog_reference.result
        ResultDialog.dialog_reference = None
        return result
