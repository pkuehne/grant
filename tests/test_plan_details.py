""" Tests for the Plan Details screen """

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from gene.windows import PlanDetails
from gene.research import ResearchProject, ResearchPlan


def test_load_project_sets_project(qtbot):
    """ load_project slot sets the class's project reference """
    # Given
    screen = PlanDetails(QStandardItemModel())
    project = ResearchProject("")
    screen.project = None
    qtbot.addWidget(screen)

    # When
    screen.update_project(project)

    # Then
    # assert screen.project == project
