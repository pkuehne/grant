""" Class for Tree Selection Screen """

# from PyQt5.QtGui import QStandardItemModel
# from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QComboBox
from grant.models.tasks_model import TasksModel
from grant.models.table_model import TableModel
from .base_screens import SelectionScreen


class FilterSelectionScreen(SelectionScreen):
    """ Shows all plans and tasks in a tree view """

    def __init__(self, data_context):
        super(FilterSelectionScreen, self).__init__(data_context)

        self.table_model = TableModel()
        self.table_model.setSourceModel(self.data_context.data_model)
        self.tasks_model = TasksModel()
        self.tasks_model.setSourceModel(self.table_model)

        filter_widgets = QFormLayout()
        self.text_filter = QLineEdit()
        self.text_filter.textChanged.connect(self.tasks_model.task_matcher.text_filter)
        filter_widgets.addRow(QLabel("Text:"), self.text_filter)
        result_model = QStringListModel(["", "open", "success", "nil"])
        self.result_filter = QComboBox()
        self.result_filter.setModel(result_model)
        self.result_filter.currentTextChanged.connect(
            self.tasks_model.task_matcher.result_filter
        )
        filter_widgets.addRow(QLabel("Result:"), self.result_filter)

        self.table_view = QTableView()
        self.table_view.setModel(self.tasks_model)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.verticalHeader().hide()
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.selectionModel().selectionChanged.connect(
            self.selection_changed
        )
        self.table_view.hideColumn(1)
        self.table_view.hideColumn(2)

        layout = QVBoxLayout()
        layout.addLayout(filter_widgets)
        layout.addWidget(self.table_view)

        self.setLayout(layout)

    def selection_changed(self, selected, _):
        """ Handle changed selection """
        if len(selected.indexes()) < 1:
            return
        index = selected.indexes()[0]
        flat_index = self.tasks_model.mapToSource(index)
        tree_index = self.table_model.mapToSource(flat_index)
        self.item_selected.emit(tree_index)

    def clear_selection(self):
        """ Called when screen is being switched to """
        self.table_view.selectionModel().clearSelection()
