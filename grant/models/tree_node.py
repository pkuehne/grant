""" Tree Node for use in TreeModel """

from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon


class TreeNode:
    """A wrapper class to normalize the parent/child relationship for node items"""

    def __init__(self, node_type, data, parent, row):
        self.type = node_type
        self.data = data
        self.parent = parent
        self.row = row
        self.children = self.get_children()

    def get_children(self):
        """Return the sub-items (plans/tasks/etc) for the given node"""
        if self.type == "plans":
            return [
                TreeNode("plan", plan, self, index)
                for index, plan in enumerate(self.data.plans)
            ]
        if self.type == "plan":
            return [
                TreeNode("task", task, self, index)
                for index, task, in enumerate(self.data.tasks)
            ]
        return []

    def delete_child(self, index):
        """Delete index from children"""
        if self.type == "plans":
            self.data.delete_plan(index)
            del self.children[index]
        if self.type == "plan":
            self.data.delete_task(index)
            del self.children[index]

    def create_child(self):
        """Creates a new child depending on the type"""
        if self.type == "plans":
            plan = self.data.add_plan()
            self.children.append(TreeNode("plan", plan, self, len(self.children)))
        if self.type == "plan":
            task = self.data.add_task()
            self.children.append(TreeNode("task", task, self, len(self.children)))

    def get_text(self):
        """Return a stringified representation for the given node"""
        if self.type == "gedcom":
            return "No gedcom file linked" if self.data == "" else self.data
        if self.type == "filename":
            return "Filename: " + self.data
        if self.type == "plans":
            return "Plans"
        if self.type == "plan":
            return self.data.ancestor
        if self.type == "task":
            return self.data.source
        return ""

    def set_text(self, value):
        """Updates the text property of the node"""
        if self.type == "plan":
            self.data.ancestor = value
        if self.type == "task":
            self.data.source = value

    def get_description(self):
        """Return a description for the given node"""
        if self.type == "plan":
            return self.data.goal
        if self.type == "task":
            return self.data.description
        return ""

    def set_description(self, value):
        """Updates the description property of the node"""
        if self.type == "plan":
            self.data.goal = value
        if self.type == "task":
            self.data.description = value

    def get_result(self):
        """Return the value for the result"""
        if self.type != "task":
            return ""
        return self.data.result

    def set_result(self, value):
        """Updates the result for a task"""
        if self.type == "task":
            self.data.result = value

    def get_ancestor(self):
        """Return the parent plan's ancestor value"""
        if self.type != "task":
            return ""
        return self.parent.data.ancestor

    def get_link(self):
        """Returns the node's gedcom link"""
        if self.type == "task":
            return self.data.source_link
        if self.type == "plan":
            return self.data.ancestor_link
        return ""

    def set_link(self, value):
        """Sets the node's gedcom link to value"""
        if self.type == "task":
            self.data.source_link = value
        if self.type == "plan":
            self.data.ancestor_link = value

    def get_icon(self):
        """Returns a QIcon for this node"""
        if self.type == "plan":
            return QIcon(":/icons/plan.ico")
        if self.type == "task":
            return QIcon(":/icons/task.ico")
        return QIcon()

    def get_font(self):
        """Returns the font to display the item in"""
        font = QFont()
        if self.is_complete():
            font.setStrikeOut(True)
        return font

    def is_complete(self):
        """Whether this plan/task is complete or not"""
        if self.type == "plans":
            return False
        if self.type == "task":
            return self.data.result is not None
        return all([node.is_complete() for node in self.children])
