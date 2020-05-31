""" Bases for all other screens in the main window """

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QModelIndex
from grant.research import ResearchProject
from grant.windows.data_context import DataContext


class BaseScreen(QWidget):
    """ Forms the basis of all screen in the main window """

    def __init__(self, data_context: DataContext):
        super(BaseScreen, self).__init__()
        self.project = None
        self.data_context = data_context

    def update_project(self, project: ResearchProject):
        """ Sets the screen's reference to the overal project information """
        self.project = project


class SelectionScreen(BaseScreen):
    """ Basis of all selection screens on the left-hand side """

    item_selected = pyqtSignal(QModelIndex)

    # def __init__(self, model):
    #     super(SelectionScreen, self).__init__(model)

    def update_project(self, project: ResearchProject):
        """ Updates the project representation and reloads the screen """
        super(SelectionScreen, self).update_project(project)
        self.reload_screen()

    def reload_screen(self):
        """ Called when things change """

    def clear_selection(self):
        """ Called when the selection needs to be cleared """
        raise NotImplementedError(
            "clear_selection() must be implemented in sub-classes"
        )


class DetailScreen(BaseScreen):
    """ Basis of all detail screens on the right-hand side """

    def __init__(self, data_context):
        super(DetailScreen, self).__init__(data_context)

    def set_selected_item(self, item):
        """ Receive selected item from main window """
        if self.project is None:
            return

        if not hasattr(self, "mapper"):
            return

        self.mapper.setRootIndex(item.parent())
        self.mapper.setCurrentModelIndex(item)
