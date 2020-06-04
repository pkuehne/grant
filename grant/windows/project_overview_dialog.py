""" Dialog showing an overview of the project """


from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from grant.windows.data_context import DataContext
from grant.research import ResearchProject


class ProjectOverviewDialog(QDialog):
    """ Edit a given Result """

    def __init__(self, context: DataContext, project: ResearchProject, parent=None):
        super(ProjectOverviewDialog, self).__init__(parent)
        self.context = context
        self.project = project

        self.setWindowIcon(QIcon(":/icons/grant.ico"))
        self.setWindowTitle("Project Overview")

        form_layout = QFormLayout()

        form_layout.addRow(QLabel("Filename:"), QLabel("Hello world"))

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.ok_button = QPushButton("OK")
        self.ok_button.pressed.connect(self.accept)
        button_layout.addWidget(self.ok_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    @classmethod
    def show(cls, parent):
        """ Wraps the creation of the dialog, particularly for unit testing """
        dialog = cls(parent)
        dialog.exec_()
