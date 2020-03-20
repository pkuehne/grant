""" Class for Tree Selection Screen """

# from PyQt5.QtGui import QStandardItemModel
# from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QVBoxLayout
from grant.windows.base_screens import SelectionScreen
from grant.windows.tasks_model import TasksModel
from grant.windows.table_model import TableModel


class FilterSelectionScreen(SelectionScreen):
    """ Shows all plans and tasks in a tree view """

    def __init__(self, model):
        super(FilterSelectionScreen, self).__init__(model)

        # filter_box = QVBoxLayout()

        self.table_model = TableModel()
        self.table_model.setSourceModel(self.data_model)
        self.tasks_model = TasksModel()
        self.tasks_model.setSourceModel(self.table_model)

        self.table_view = QTableView()
        self.table_view.setModel(self.tasks_model)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.verticalHeader().hide()
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.selectionModel().selectionChanged.connect(self.selection_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.table_view)

        self.setLayout(layout)

    def selection_changed(self, selected, _):
        """ Handle changed selection """
        if len(selected.indexes()) != 1:
            return
        index = selected.indexes()[0]
        flat_index = self.tasks_model.mapToSource(index)
        tree_index = self.table_model.mapToSource(flat_index)
        self.item_selected.emit(tree_index)

    def clear_selection(self):
        """ Called when screen is being switched to """
        self.table_view.selectionModel().clearSelection()
