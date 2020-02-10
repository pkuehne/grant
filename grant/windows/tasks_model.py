""" Provides a proxy model to pick only the leaf tasks from the Tree Model """

from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtCore import QModelIndex


class TasksModel(QSortFilterProxyModel):
    """ Filters the input TreeModel to a table model of only the tasks """

    def filterAcceptsRow(self, row, parent):  # pylint: disable=invalid-name
        """ Whether this row is part of the filtered view """

        index = self.sourceModel().index(row, 0, parent)
        if not index.isValid():
            return True

        node = index.internalPointer()

        return node.type == "task"
