""" Provides a proxy model to flatten the Tree Model """

from PyQt5.QtCore import QAbstractProxyModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt


class TableModel(QAbstractProxyModel):
    """ Retructures the TreeModel into a flat table, keeping all data the same """

    def __init__(self):
        super(TableModel, self).__init__()
        self.row_map = {}
        self.index_map = {}

    def build_map(self, model, parent, row):
        """ Constructs and internal mapping of rows and indices """
        if row == 0:
            self.row_map = {}
            self.index_map = {}
        rows = model.rowCount(parent)
        for child_row in range(rows):
            index = model.index(child_row, 0, parent)
            print('row', row, 'item', model.data(index, Qt.DisplayRole))
            self.row_map[index] = row
            self.index_map[row] = index
            row = row + 1
            if model.hasChildren(index):
                row = self.build_map(model, index, row)
        return row

    def sourceDataChanged(self, topLeft, bottomRight):  # pylint: disable=invalid-name
        """ remap source indices and emit dataChanged signal """
        self.dataChanged.emit(self.mapFromSource(topLeft),
                              self.mapFromSource(bottomRight))

    def setSourceModel(self, model):  # pylint: disable=invalid-name
        """ Build row/index map when source model is set """
        QAbstractProxyModel.setSourceModel(self, model)
        self.build_map(model, QModelIndex(), 0)
        model.dataChanged.connect(self.sourceDataChanged)

    def mapFromSource(self, index):  # pylint: disable=invalid-name
        """ map given index from Tree to Flat """
        if index not in self.row_map:
            return QModelIndex()
        #print('mapping to row', self.row_map[index], flush = True)
        return self.createIndex(self.row_map[index], index.column(), index.internalPointer())

    def mapToSource(self, index):  # pylint: disable=invalid-name
        """ map given index from flat table to tree """
        if not index.isValid() or index.row() not in self.index_map:
            return QModelIndex()
        #print('mapping from row', index.row(), flush = True)
        return self.index_map[index.row()]

    def columnCount(self, index):  # pylint: disable=invalid-name
        """ Return column count of source model for this index """
        return QAbstractProxyModel.sourceModel(self)\
            .columnCount(self.mapToSource(index))

    def rowCount(self, index):  # pylint: disable=invalid-name
        """ Return row count of source model at this index """
        #print('rows:', len(self.row_map), flush=True)
        return len(self.row_map) if not index.isValid() else 0

    def index(self, row, column, parent):
        """ Return index into the flat table """
        #print('index for:', row, column, flush=True)
        if parent.isValid() or not self.index_map:
            return QModelIndex()
        return self.createIndex(row, column, self.index_map[row].internalPointer())

    def parent(self, _):  # pylint: disable=no-self-use
        """ Return invalid index, since there are no parents """
        return QModelIndex()
