""" Contains the tree representation class for a ResearchProject """

from enum import IntEnum, unique
from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt
from grant.research import ResearchProject
from grant.models.tree_node import TreeNode


@unique
class TreeModelCols(IntEnum):
    """ Enum for the columns of the TreeModel """

    TEXT = 0
    DESCRIPTION = 1
    RESULT = 2
    ANCESTOR = 3
    LINK = 4


class TreeModel(QAbstractItemModel):
    """ Represent the ResearchProject as a tree """

    def __init__(self):
        QAbstractItemModel.__init__(self)
        self.project = None
        self.plans_node = None
        self.plans_index = QModelIndex()

    def set_project(self, project):
        """ Updates the internal project representation """
        self.beginResetModel()
        self.project: ResearchProject = project
        if self.project is not None:
            self.plans_node = TreeNode("plans", self.project, None, 2)
        self.endResetModel()

        self.plans_index = QModelIndex()

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
        if not index.isValid():
            node = self.plans_node
        else:
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
            node = self.plans_node
        else:
            node = parent.internalPointer()
        if row >= len(node.children):
            return QModelIndex()
        return self.createIndex(row, column, node.children[row])

    def parent(self, index):
        """ Return the parent index object for given item """
        if not index.isValid():
            return QModelIndex()
        node = index.internalPointer()
        if node.parent is self.plans_node:
            return QModelIndex()
        return self.createIndex(node.parent.row, 0, node.parent)

    def hasChildren(self, parent):  # pylint: disable=invalid-name
        """ Return whether this node has any children """
        if self.project is None:
            return False
        if not parent.isValid():
            return len(self.plans_node.children) != 0
        node = parent.internalPointer()
        return len(node.children) != 0

    def rowCount(self, parent):  # pylint: disable=invalid-name
        """ Return number of children for the given index object """
        if self.project is None:
            return 0
        if not parent.isValid():
            return len(self.plans_node.children)
        node = parent.internalPointer()
        return len(node.children)

    def columnCount(self, _):  # pylint: disable=invalid-name, no-self-use
        """ Number of columns to display """
        return len(list(TreeModelCols))

    def data(self, index, role):  # pylint: disable= no-self-use
        """ Return the data associated with the specific index for the role """
        if not index.isValid() or index.column() > self.columnCount(None):
            return None
        node = index.internalPointer()
        if role in [Qt.DisplayRole, Qt.EditRole]:
            return {
                TreeModelCols.TEXT: node.get_text(),
                TreeModelCols.DESCRIPTION: node.get_description(),
                TreeModelCols.RESULT: node.get_result(),
                TreeModelCols.ANCESTOR: node.get_ancestor(),
                TreeModelCols.LINK: node.get_link(),
            }[index.column()]
        if role == Qt.DecorationRole:
            return node.get_icon()
        if role == Qt.FontRole:
            return node.get_font()
        return None

    def setData(self, index, value, role=Qt.EditRole):  # pylint: disable=invalid-name
        """ Updates the nodes values based on an edit """
        if (
            not index.isValid()
            or index.column() > self.columnCount(None)
            or role != Qt.EditRole
        ):
            return False
        node = index.internalPointer()

        prev = ""
        if index.column() == TreeModelCols.TEXT:
            prev = node.get_text()
            node.set_text(value)
        if index.column() == TreeModelCols.DESCRIPTION:
            prev = node.get_description()
            node.set_description(value)
        if index.column() == TreeModelCols.RESULT:
            prev = node.get_result()
            node.set_result(value)
        if index.column() == TreeModelCols.LINK:
            prev = node.get_link()
            node.set_link(value)

        if prev != value:
            self.dataChanged.emit(index, index)
        return True

    def headerData(
        self, section, orientation, role
    ):  # pylint: disable=invalid-name, no-self-use
        """ Set the header information """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return {
                TreeModelCols.TEXT: "Research Project",
                TreeModelCols.ANCESTOR: "Ancestor",
            }.get(section, "")
        return None

    def flags(self, index):  # pylint: disable= no-self-use
        """ Returns the flags for the given index """
        if not index.isValid():
            return Qt.NoItemFlags
        flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        flags |= {TreeModelCols.ANCESTOR: 0}.get(index.column(), Qt.ItemIsEditable)
        return flags
