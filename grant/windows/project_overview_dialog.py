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

        self.setWindowIcon(QIcon(":/icons/grant.ico"))
        self.setWindowTitle("Project Overview")

        form_layout = QFormLayout()

        all_tasks = [task for plan in project.plans for task in plan.tasks]
        form_layout.addRow(QLabel("Project File:"), QLabel(project.filename))
        form_layout.addRow(QLabel("Total Plans:"), QLabel(str(len(project.plans))))
        form_layout.addRow(
            QLabel("Total Tasks:"), QLabel(str(len(all_tasks))),
        )
        form_layout.addRow(
            QLabel("Open Tasks:"),
            QLabel(str(len([t for t in all_tasks if t.is_open()]))),
        )
        form_layout.addRow(QLabel(""), QLabel(""))
        form_layout.addRow(QLabel("Gedcom Link:"), QLabel(project.gedcom))
        form_layout.addRow(
            QLabel("Linked Individuals:"),
            QLabel(str(context.individuals_model.rowCount())),
        )
        form_layout.addRow(
            QLabel("Linked Sources:"), QLabel(str(context.sources_model.rowCount())),
        )

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.ok_button = QPushButton("OK")
        self.ok_button.pressed.connect(self.accept)
        button_layout.addWidget(self.ok_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    @classmethod
    def show(cls, context: DataContext, project: ResearchProject, parent):
        """ Wraps the creation of the dialog, particularly for unit testing """
        dialog = cls(context, project, parent)
        dialog.exec_()
