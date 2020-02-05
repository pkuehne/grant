""" Widget to show Research Tasks """

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtWidgets import QTableView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSignal
from gene.research import ResearchPlan, ResearchTask


class TaskOverview(QWidget):
    """ Displays all current Research Tasks """

    task_edited = pyqtSignal(int)
    task_deleted = pyqtSignal()
    task_added = pyqtSignal(int)

    def __init__(self):
        super(TaskOverview, self).__init__()
        self.plan: ResearchPlan = None
        self.task_model = QStandardItemModel()
        self.task_model.setHorizontalHeaderLabels(["Task", "Status"])
        self.task_table = QTableView()
        self.task_table.setModel(self.task_model)
        self.task_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.task_table.verticalHeader().hide()
        self.task_table.doubleClicked.connect(self.edit_task)
        self.task_table.selectionModel().selectionChanged.connect(self.selection_changed)

        self.add_button = QPushButton()
        self.add_button.setText("Add")
        self.add_button.setDisabled(True)
        self.add_button.pressed.connect(self.add_task)
        self.edit_button = QPushButton()
        self.edit_button.setText("Edit")
        self.edit_button.setDisabled(True)
        self.edit_button.pressed.connect(lambda: self.edit_task(
            self.task_table.selectionModel().selectedIndexes()[0]))
        self.delete_button = QPushButton()
        self.delete_button.setText("Delete")
        self.delete_button.setDisabled(True)
        self.delete_button.pressed.connect(lambda: self.delete_task(
            self.task_table.selectionModel().selectedIndexes()[0]))

        button_box = QVBoxLayout()
        button_box.addWidget(self.add_button)
        button_box.addWidget(self.edit_button)
        button_box.addWidget(self.delete_button)
        button_box.addStretch()

        layout = QHBoxLayout()
        layout.addWidget(self.task_table)
        layout.addLayout(button_box)

        self.setLayout(layout)

    def load_plan(self, plan: ResearchPlan):
        """ Slot for when research plan changes """
        self.plan = plan
        self.load_tasks()

    def load_tasks(self):
        """ Populates the task table with all tasks """
        self.add_button.setDisabled(self.plan is None)
        if self.plan is None:
            return

        self.task_model.setRowCount(0)
        for task in self.plan.tasks:
            row = []
            row.append(QStandardItem(task.title))
            row.append(QStandardItem(task.status))
            self.task_model.appendRow(row)

    def edit_task(self, index):
        """ Double-click on row, open up task """
        # print(self.task_model.data(index.siblingAtColumn(0)))
        self.task_edited.emit(index.row())

    def add_task(self):
        """ Add a new task """
        self.plan.tasks.append(ResearchTask())
        self.load_tasks()
        self.task_added.emit(len(self.plan.tasks)-1)

    def delete_task(self, index):
        """ Delete the selected task """
        del self.plan.tasks[index.row()]
        self.task_table.selectionModel().clearSelection()
        self.load_tasks()
        self.task_deleted.emit()

    def selection_changed(self, selected, _):
        """ Handle changed selection """
        self.edit_button.setEnabled(selected.count())
        self.delete_button.setEnabled(selected.count())
