""" Bases for all other screens in the main window """

from PyQt5.QtWidgets import QWidget
from gene.research import ResearchProject


class BaseScreen(QWidget):
    """ Forms the basis of all screen in the main window """

    def __init__(self):
        super(BaseScreen, self).__init__()
        self.project = None

    def update_project(self, project: ResearchProject):
        """ Sets the screen's reference to the overal project information """
        self.project = project


class SelectionScreen(BaseScreen):
    """ Basis of all selection screens on the left-hand side """

    def update_project(self, project: ResearchProject):
        """ Updates the project representation and reloads the screen """
        super(SelectionScreen, self).update_project(project)
        self.reload_screen()

    def reload_screen(self):
        """ Called when things change """
        pass


class DetailSecreen(BaseScreen):
    """ Basis of all detail screens on the right-hand side """
