""" The Research-related classes """


class TaskLog:
    """ Audit log for a task """

    def __init__(self):
        self.action = ""
        self.date = ""
        self.text = ""


class ResearchTask:
    """ A single task """
    default_task_title = "New Task"
    default_status = "active"

    def __init__(self):
        self.title = self.default_task_title
        self.description = "Add a more detailed description of the task"
        self.status = self.default_status
        self.logs = []

    def __str__(self):
        return "Research Task: " + self.title

    def from_py(self, data):
        """ Converts from pythonic to class """
        self.title = data.get("title", self.default_task_title)
        self.description = data.get("description", "")
        self.status = data.get("status", self.default_status)

    def to_py(self):
        """ Converts from class to pythonic """
        data = {}
        data["title"] = self.title
        data["description"] = self.description
        data["status"] = self.status
        return data


class ResearchPlan:
    """ A collection of tasks with a common goal """
    default_title = "New Plan"

    def __init__(self):
        self.title = self.default_title
        self.goal = "Describe your goals for this plan..."
        self.tasks = []

    def __str__(self):
        retval = "Research Plan: " + self.title
        for task in self.tasks:
            retval = retval + "\n\t\t" + str(task)
        return retval

    def from_py(self, data):
        """ Converts from pythonic to class """
        self.title = data.get("title", self.default_title)
        self.goal = data.get("goal", "")
        for task_data in data.get("tasks", []):
            task = ResearchTask()
            task.from_py(task_data)
            self.tasks.append(task)

    def to_py(self):
        """ Converts from class to pythonic """
        data = {}
        data["title"] = self.title
        data["goal"] = self.goal
        data["tasks"] = []
        for task in self.tasks:
            data["tasks"].append(task.to_py())
        return data


class ResearchProject:
    """ All the research plans for a gedcom """

    def __init__(self, filename):
        self.version = "1.0"
        self.gedcom = "none"
        self.filename = filename
        self.plans = []

    def __str__(self):
        return self.filename

    def from_py(self, data):
        """ Converts from pythonic datastructures to class """
        self.version = data["version"]
        self.gedcom = data["gedcom"]
        for plan_data in data["plans"]:
            plan = ResearchPlan()
            plan.from_py(plan_data)
            self.plans.append(plan)
        print(self)

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
        return self.gedcom != "none"
