""" Container for selection and details screens """

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QHBoxLayout

from grant.windows.data_context import DataContext
from grant.windows.tree_selection_screen import TreeSelectionScreen
from grant.windows.filter_selection_screen import FilterSelectionScreen
from grant.windows.plan_details import PlanDetails
from grant.windows.task_details import TaskDetails
from grant.windows.base_screens import DetailScreen
from grant.research import ResearchProject


class MainScreen(QWidget):
    """ The main selection and display screen """

    def __init__(self, parent, data_context: DataContext):
        super().__init__(parent)
        self.data_context = data_context
        self.selection_stack = None
        self.detail_stack = None
        self.screens = {}

        self.setup_selection_screens()
        self.setup_details_screens()
        self.setup_layout()

    def setup_selection_screens(self):
        """ Set up the screens for selection """
        self.selection_stack = QStackedWidget()

        self.screens["tree"] = TreeSelectionScreen(self.data_context)
        self.selection_stack.addWidget(self.screens["tree"])

        self.screens["filter"] = FilterSelectionScreen(self.data_context)
        self.selection_stack.addWidget(self.screens["filter"])

        self.screens["tree"].item_selected.connect(self.selection_changed)
        self.screens["filter"].item_selected.connect(self.selection_changed)

    def setup_details_screens(self):
        """ Set up the screens for detail views """
        self.detail_stack = QStackedWidget()

        self.screens["blank"] = DetailScreen(self.data_context)
        self.detail_stack.addWidget(self.screens["blank"])
        self.screens["plan"] = PlanDetails(self.data_context)
        self.detail_stack.addWidget(self.screens["plan"])
        self.screens["task"] = TaskDetails(self.data_context)
        self.detail_stack.addWidget(self.screens["task"])

        self.detail_stack.setCurrentWidget(self.screens["blank"])

    def setup_layout(self):
        """ Setup the layout """
        layout = QHBoxLayout()
        layout.addWidget(self.selection_stack)
        layout.addWidget(self.detail_stack)
        self.setLayout(layout)

    def selection_changed(self, item):
        """ Called when the selection from a selection screen changes """
        node = item.internalPointer()
        if node.type == "gedcom":
            self.change_detail_screen("blank", item)
            return
        if node.type == "task":
            self.change_detail_screen("task", item)
            return
        if node.type == "plan":
            self.change_detail_screen("plan", item)
            return
        self.change_detail_screen("blank", item)

    def change_detail_screen(self, name: str, item):
        """ Sets the current detail screen """
        self.detail_stack.setCurrentWidget(self.screens[name])
        self.screens[name].set_selected_item(item)

    def change_selection_screen(self, name):
        """ Change the selection to the specified screen """
        self.selection_stack.setCurrentWidget(self.screens[name])
        self.screens[name].clear_selection()
        self.detail_stack.setCurrentWidget(self.screens["blank"])

    def set_project(self, project: ResearchProject):
        """ Updates all the screens with the new project information """
        self.data_context.data_model.set_project(project)
        for screen in self.screens.values():
            screen.update_project(project)
