""" Contains the tree representation class for a ResearchProject """

from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from gene.research import ResearchProject, ResearchPlan, ResearchTask


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

    def delete_child(self, index):
        """ Delete index from children """
        if self.type == "plans":
            del self.data[index]
            del self.children[index]
        if self.type == "plan":
            del self.data.tasks[index]
            del self.children[index]

    def create_child(self):
        """ Creates a new child depending on the type """
        if self.type == "plans":
            plan = ResearchPlan()
            self.data.append(plan)
        if self.type == "plan":
            task = ResearchTask()
            self.data.tasks.append(task)
        self.children = self.get_children()

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
        return ""

    def set_text(self, value):
        """ Updates the text property of the node """
        if self.type == "plan":
            self.data.title = value
        if self.type == "task":
            self.data.title = value

    def get_description(self):
        """ Return a description for the given node """
        if self.type == "plan":
            return self.data.goal
        if self.type == "task":
            return self.data.description
        return ""

    def set_description(self, value):
        """ Updates the description property of the node """
        if self.type == "plan":
            self.data.goal = value
        if self.type == "task":
            self.data.description = value

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
                TreeNode("plans", self.project.plans, None, 2))
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

    def data(self, index, role):  # pylint: disable= no-self-use
        """ Return the data associated with the specific index for the role """
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role in [Qt.DisplayRole, Qt.EditRole]:
            if index.column() == 0:
                return node.get_text()
            if index.column() == 1:
                return node.get_description()
            return None
        if role == Qt.DecorationRole:
            return node.get_icon()
        return None

    def setData(self, index, value, _):  # pylint: disable=invalid-name
        """ Updates the nodes values based on an edit """
        if not index.isValid():
            return False
        node = index.internalPointer()

        if index.column() == 0:
            node.set_text(value)
        if index.column() == 1:
            node.set_description(value)

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
