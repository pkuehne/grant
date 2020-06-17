""" The Research-related classes """
from datetime import datetime
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QTextDocument


def convert_html(text: str) -> str:
    """ Converts potential HTML into plain text """
    document = QTextDocument()
    document.setHtml(text)
    return document.toPlainText().rstrip().lstrip()


class ResearchResult(QObject):
    """ Result of a Task """

    def __init__(self, success: bool):
        super().__init__()
        self.date = datetime.now()
        self.document = ""
        self.summary = ""
        self.nil = not success

    def is_nil(self):
        """ Negative result? """
        return self.nil is True

    def from_py(self, data):
        """ converts from pythonic to class """
        if data is None:
            return
        self.date = data.get("date", None)
        self.document = data.get("document", "")
        self.summary = data.get("summary", "")
        self.nil = data.get("nil", True)

    def to_py(self):
        """ Converts from class to pythonic """
        data = {}
        data["date"] = self.date
        data["document"] = self.document
        data["summary"] = self.summary
        data["nil"] = self.nil
        return data

    def __str__(self):
        """ String representation """
        data = ""
        if self.is_nil():
            data = "nil"
        else:
            data = "success"

        data += " - " + self.summary if self.summary != "" else ""
        return data


class ResearchTask:
    """ A single task """

    def __init__(self):
        self.source = ""
        self.description = ""
        self.result = None

    def __str__(self):
        return "Research Task: " + self.description

    def from_py(self, data):
        """ Converts from pythonic to class """
        self.source = data.get("source", "")
        self.description = convert_html(data.get("description", ""))
        result = data.get("result", None)
        if result is not None:
            self.result = ResearchResult(False)
            self.result.from_py(result)

    def to_py(self):
        """ Converts from class to pythonic """
        data = {}
        data["source"] = self.source
        data["description"] = self.description
        data["result"] = None if self.result is None else self.result.to_py()
        return data

    def is_open(self):
        """ Whether the task is still open """
        return self.result is None


class ResearchPlan:
    """ A collection of tasks with a common goal """

    default_ancestor = "My Ancestor"

    def __init__(self):
        self.ancestor = self.default_ancestor
        self.goal = "Describe your goals for this plan..."
        self.tasks = []

    def __str__(self):
        retval = "Research Plan: " + self.ancestor
        return retval

    def from_py(self, data):
        """ Converts from pythonic to class """
        self.ancestor = data.get("ancestor", None)
        self.goal = convert_html(data.get("goal", ""))
        for task_data in data.get("tasks", []):
            task = ResearchTask()
            task.from_py(task_data)
            self.tasks.append(task)

    def to_py(self):
        """ Converts from class to pythonic """
        data = {}
        data["ancestor"] = self.ancestor
        data["goal"] = self.goal
        data["tasks"] = []
        for task in self.tasks:
            data["tasks"].append(task.to_py())
        return data

    def add_task(self):
        """ Create a new task and return it """
        task = ResearchTask()
        self.tasks.append(task)
        return task

    def delete_task(self, index):
        """ Deletes the task at the given index """
        if index > len(self.tasks) or len(self.tasks) == 0:
            return
        del self.tasks[index]


class ResearchProject:
    """ All the research plans for a gedcom """

    def __init__(self, filename):
        self.version = "1.0"
        self.gedcom = ""
        self.filename = filename
        self.plans = []

    def __str__(self):
        return self.filename

    def from_py(self, data):
        """ Converts from pythonic datastructures to class """
        self.version = data["version"]
        self.gedcom = data.get("gedcom", "")
        if self.gedcom == "none":
            self.gedcom = ""  # backwards compatibility check
        for plan_data in data["plans"]:
            plan = ResearchPlan()
            plan.from_py(plan_data)
            self.plans.append(plan)

    def to_py(self):
        """ Converts to pythonic representation """
        data = {}
        data["version"] = self.version
        data["gedcom"] = self.gedcom
        data["plans"] = []
        for plan in self.plans:
            data["plans"].append(plan.to_py())
        return data

    def has_gedcom(self):
        """ Whether a gedcom file is associated with this project """
        return self.gedcom != ""

    def add_plan(self):
        """ Creates and returns a new plan """
        plan = ResearchPlan()
        self.plans.append(plan)
        return plan

    def delete_plan(self, index):
        """ Delete plan at index """
        if index > len(self.plans) or len(self.plans) == 0:
            return
        del self.plans[index]
