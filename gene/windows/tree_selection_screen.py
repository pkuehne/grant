""" Class for Tree Selection Screen """

from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QVBoxLayout
from gene.windows.base_screens import SelectionScreen
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
            return "Gedcom: " + self.data
        if self.type == "filename":
            return "Filename: " + self.data
        if self.type == "plans":
            return "Plans"
        if self.type == "plan":
            return self.data.title
        if self.type == "task":
            return self.data.title
        return self.data

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

    def hasChildren(self, parent):
        """ Return whether this node has any children """
        if not parent.isValid():
            return len(self.root_nodes) != 0
        node = parent.internalPointer()
        return len(node.children) != 0

    def rowCount(self, parent):
        """ Return number of children for the given index object """
        if not parent.isValid():
            return len(self.root_nodes)
        node = parent.internalPointer()
        return len(node.children)

    def columnCount(self, _):
        """ Number of columns to display """
        return 1

    def data(self, index, role):
        """ Return the data associated with the specific index for the role """
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None

        node = index.internalPointer()
        return node.get_text()

    def headerData(self, section, orientation, role):
        """ Set the header information """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole \
                and section == 0:
            return "Research Project"
        return None


class TreeSelectionScreen(SelectionScreen):
    """ Shows all plans and tasks in a tree view """

    def __init__(self):
        super(TreeSelectionScreen, self).__init__()

        self.plan_model = TreeModel()
        self.plan_table = QTreeView()
        self.plan_table.setModel(self.plan_model)
        self.plan_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.plan_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.plan_table.selectionModel().selectionChanged.connect(self.selection_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.plan_table)

        self.setLayout(layout)

    def reload_screen(self):
        """ Loads the screen """
        self.plan_model.set_project(self.project)

    def selection_changed(self, selected, _):
        """ Handle changed selection """
        if len(selected.indexes()) != 1:
            return
        node = selected.indexes()[0].internalPointer()
        self.item_selected.emit(node.get_selection_representation())
