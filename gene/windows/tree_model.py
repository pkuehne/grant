""" Contains the tree representation class for a ResearchProject """

from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from gene.research import ResearchProject


class TreeNode:
    """ A wrapper class to normalize the parent/child relationship for node items """

    def __init__(self, node_type, data, parent, row):
        self.type = node_type
        self.data = data
        self.parent = parent
        self.row = row
        self.children = self.get_children()

    def get_children(self):
        """ Return the sub-items (plans/tasks/etc) for the given node """
        if self.type == "plans":
            return [TreeNode("plan", plan, self, index)
                    for index, plan in enumerate(self.data)]
        if self.type == "plan":
            return [TreeNode("task", task, self, index)
                    for index, task, in enumerate(self.data.tasks)]
        return []

    def get_text(self):
        """ Return a stringified representation for the given node """
        if self.type == "gedcom":
            return "No gedcom file linked" if self.data == "none" else self.data
        if self.type == "filename":
            return "Filename: " + self.data
        if self.type == "plans":
            return "Plans"
        if self.type == "plan":
            return self.data.title
        if self.type == "task":
            return self.data.title
        return self.data

    def get_icon(self):
        """ Returns a QIcon for this node """
        if self.type == "gedcom":
            return QIcon("icons/gedcom.ico")
        if self.type == "filename":
            return QIcon("icons/file.ico")
        if self.type == "plans":
            return QIcon("icons/plans.ico")
        if self.type == "plan":
            return QIcon("icons/plan.ico")
        if self.type == "task":
            return QIcon("icons/task.ico")
        return QIcon()

    def get_selection_representation(self):
        """ Return a way to identify the item selected """
        item = {}

        if self.type == "gedcom":
            item["gedcom"] = True
        if self.type == "plan":
            item["plan"] = self.row
        if self.type == "task":
            item["plan"] = self.parent.row
            item["task"] = self.row
        return item


class TreeModel(QAbstractItemModel):
    """ Represent the ResearchProject as a tree """

    def __init__(self):
        QAbstractItemModel.__init__(self)
        self.project = None
        self.root_nodes = []

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
                TreeNode("plans", self.project.plans, None, 2))
        self.endResetModel()

    def index(self, row, column, parent):
        """ Return index object for given item """
        if self.project is None:
            return QModelIndex()
        if not parent.isValid():
            return self.createIndex(row, column, self.root_nodes[row])
        node = parent.internalPointer()
        return self.createIndex(row, column, node.children[row])

    def parent(self, index):
        """ Return the parent index object for given item """
        if not index.isValid():
            print("return invalid for invalid index")
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

    def data(self, index, role):  # pylint: disable= no-self-use
        """ Return the data associated with the specific index for the role """
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role in [Qt.DisplayRole, Qt.EditRole]:
            return node.get_text()
        if role == Qt.DecorationRole:
            return node.get_icon()
        return None

    def setData(self, index, value, _):  # pylint: disable=invalid-name
        """ Updates the nodes values based on an edit """
        if not index.isValid():
            return False
        node = index.internalPointer()
        node.data.title = value

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
