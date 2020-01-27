""" Tests for the Plan Details screen """

from PyQt5.QtCore import Qt
from gene.windows import PlanDetails
from gene.research import ResearchProject, ResearchPlan


def test_load_project_sets_project(qtbot):
    """ load_project slot sets the class's project reference """
    # Given
    screen = PlanDetails()
    project = ResearchProject("")
    screen.project = None
    qtbot.addWidget(screen)

    # When
    screen.load_project(project)

    # Then
    assert screen.project == project


def test_select_plan_sets_title_and_goal(qtbot):
    """ Setting the plan, updates the title and goal widgets """
    # Given
    screen = PlanDetails()
    project = ResearchProject("")
    plan = ResearchPlan()
    plan.title = "Foo"
    plan.goal = "Bar"
    project.plans.append(plan)
    screen.load_project(project)
    screen.index = 10
    qtbot.addWidget(screen)

    # When
    screen.select_plan(0)

    # Then
    assert screen.title.text() == plan.title
    assert screen.goal.document().toPlainText() == plan.goal


def test_select_plan_does_nothing_if_no_project(qtbot):
    """ When no project is set, selecting plan does nothing """
    # Given
    screen = PlanDetails()
    screen.project = None
    screen.index = 0
    qtbot.addWidget(screen)

    # When
    screen.select_plan(10)

    # Then
    assert screen.index == 0


def test_typed_changes_are_saved(qtbot):
    """ Typing changes to title are saved """
    # Given
    screen = PlanDetails()
    project = ResearchProject("")
    plan = ResearchPlan()
    plan.title = "Foo"
    plan.goal = "Bar"
    project.plans.append(plan)
    screen.load_project(project)
    qtbot.addWidget(screen)

    # When
    with qtbot.waitSignal(screen.plan_changed, timeout=100) as _:
        qtbot.keyClicks(screen.title, "ABC")
        screen.title.editingFinished.emit()

    # Then
    assert screen.title.text() != "Foo"
    assert project.plans[0].title != "Foo"


def test_clicking_close_emits_a_signal(qtbot):
    """ Clicking on the close button fires the right signal """
    # Given
    screen = PlanDetails()

    # When
    with qtbot.waitSignal(screen.close_clicked, timeout=100) as _:
        qtbot.mouseClick(screen.close_button, Qt.LeftButton)

    # Then
