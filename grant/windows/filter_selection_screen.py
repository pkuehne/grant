""" Class for Tree Selection Screen """

# from PyQt5.QtGui import QStandardItemModel
# from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QVBoxLayout
from grant.windows.base_screens import SelectionScreen


class FilterSelectionScreen(SelectionScreen):
    """ Shows all plans and tasks in a tree view """

    def __init__(self, model):
        super(FilterSelectionScreen, self).__init__(model)

        self.table_view = QTableView()
        self.table_view.setModel(self.data_model)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.verticalHeader().hide()
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.selectionModel().selectionChanged.connect(self.selection_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.table_view)

        self.setLayout(layout)

    def reload_screen(self):
        """ Loads the screen """

    def selection_changed(self, selected, _):
        """ Handle changed selection """

    def clear_selection(self):
        """ Called when screen is being switched to """
        self.table_view.selectionModel().clearSelection()
