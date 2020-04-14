""" Contains the tree representation class for a ResearchProject """

from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt
from grant.research import ResearchProject
from grant.models.tree_node import TreeNode


class TreeModel(QAbstractItemModel):
    """ Represent the ResearchProject as a tree """

    def __init__(self):
        QAbstractItemModel.__init__(self)
        self.project = None
        self.root_nodes = []
        self.gedcom_index = QModelIndex()
        self.filename_index = QModelIndex()
        self.plans_index = QModelIndex()

    def set_project(self, project):
        """ Updates the internal project representation """
        self.beginResetModel()
        self.project: ResearchProject = project
        if self.project is not None:
            self.root_nodes.clear()
            self.root_nodes.append(
                TreeNode("gedcom", self.project.gedcom, None, 0))
            self.root_nodes.append(
                TreeNode("filename", self.project.filename, None, 1))
            self.root_nodes.append(
                TreeNode("plans", self.project, None, 2))
        self.endResetModel()

        self.gedcom_index = self.index(0, 0, QModelIndex())
        self.filename_index = self.index(1, 0, QModelIndex())
        self.plans_index = self.index(2, 0, QModelIndex())

    def delete_node(self, index):
        """ Deletes the node at the given index """
        if not index.isValid():
            return
        self.beginRemoveRows(index.parent(), index.row(), index.row())
        node = index.internalPointer()
        parent = node.parent

        parent.delete_child(index.row())

        self.endRemoveRows()

    def add_node(self, index):
        """ Adds a new node at the given index """
        node = index.internalPointer()

        self.layoutAboutToBeChanged.emit()
        self.beginInsertRows(index, len(node.children), len(node.children) + 1)

        node.create_child()

        self.endInsertRows()
        self.layoutChanged.emit()

    def index(self, row, column, parent):
        """ Return index object for given item """
        if self.project is None:
            return QModelIndex()
        if not parent.isValid():
            return self.createIndex(row, column, self.root_nodes[row])
        node = parent.internalPointer()
        if row >= len(node.children):
            return QModelIndex()
        return self.createIndex(row, column, node.children[row])

    def parent(self, index):
        """ Return the parent index object for given item """
        if not index.isValid():
            return QModelIndex()
        node = index.internalPointer()
        if node.parent is None:
            return QModelIndex()
        return self.createIndex(node.parent.row, 0, node.parent)

    def hasChildren(self, parent):  # pylint: disable=invalid-name
        """ Return whether this node has any children """
        if not parent.isValid():
            return len(self.root_nodes) != 0
        node = parent.internalPointer()
        return len(node.children) != 0

    def rowCount(self, parent):  # pylint: disable=invalid-name
        """ Return number of children for the given index object """
        if not parent.isValid():
            return len(self.root_nodes)
        node = parent.internalPointer()
        return len(node.children)

    def columnCount(self, _):  # pylint: disable=invalid-name, no-self-use
        """ Number of columns to display """
        return 1

    def data_column(self, node, column):
        """ Returns the data that this node should show in the given column """
        if column == 0:
            return node.get_text()
        if column == 1:
            return node.get_description()
        if column == 2:
            return node.get_result()
        return None

    def data(self, index, role):  # pylint: disable= no-self-use
        """ Return the data associated with the specific index for the role """
        if not index.isValid() or index.column() > 2:
            return None
        node = index.internalPointer()
        if role in [Qt.DisplayRole, Qt.EditRole]:
            return self.data_column(node, index.column())
        if role == Qt.DecorationRole:
            return node.get_icon()
        if role == Qt.FontRole:
            return node.get_font()
        return None

    def setData(self, index, value, _):  # pylint: disable=invalid-name
        """ Updates the nodes values based on an edit """
        if not index.isValid() or index.column() > 2:
            return False
        node = index.internalPointer()

        prev = ""
        if index.column() == 0:
            prev = node.get_text()
            node.set_text(value)
        if index.column() == 1:
            prev = node.get_description()
            node.set_description(value)
        if index.column() == 2:
            # prev = node.get_status()
            # node.set_status(value)
            pass

        if prev != value:
            self.dataChanged.emit(index, index)
        return True

    def headerData(self, section, orientation, role):  # pylint: disable=invalid-name, no-self-use
        """ Set the header information """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole \
                and section == 0:
            return "Research Project"
        return None

    def flags(self, index):  # pylint: disable= no-self-use
        """ Returns the flags for the given index """
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled

    def update_result(self, index, result):
        """ Sets the result for a given task """
        if not index.isValid() or index.column() > 2:
            return False
        node: TreeNode = index.internalPointer()

        if not node.type == "task":
            return False

        node.data.result = result
        self.dataChanged.emit(index, index)
