""" Test for the Tree Model """

from PyQt5.QtCore import QModelIndex

from gene.windows.tree_model import TreeNode
from gene.windows.tree_model import TreeModel
from gene.research import ResearchProject, ResearchPlan, ResearchTask


def test_empty_icon_returned_for_unknown_node_type():
    """ Return an empty QIcon if the type is invalid """
    # Given
    node = TreeNode("foo", None, None, 0)

    # When
    icon = node.get_icon()

    # Then
    assert icon.isNull()


def test_new_model_is_empty_by_default():
    """ Empty model should not have a project set and no nodes """
    # Given
    model = TreeModel()

    # Then
    assert model.project is None
    assert model.root_nodes == []


def test_set_project_calls_begin_end_reset(qtbot):
    """ beginReset and endReset should be emitted """
    # Given
    model = TreeModel()
    project = ResearchProject("")

    # When
    with qtbot.waitSignals([model.modelAboutToBeReset, model.modelReset]):
        model.set_project(project)


def test_set_project_calls_begin_end_reset_when_project_is_none(qtbot):
    """ Ensure that model is reset even when unsetting the project """
    # Given
    model = TreeModel()

    # When
    with qtbot.waitSignals([model.modelAboutToBeReset, model.modelReset]):
        model.set_project(None)


def test_set_project_clears_existing_nodes():
    """ Setting valid project should clear existing nodes """
    # Given
    model = TreeModel()
    project = ResearchProject("")

    # When
    model.set_project(project)
    model.set_project(project)

    # Then
    assert sum(1 for n in model.root_nodes if n.type == "gedcom") == 1
    assert sum(1 for n in model.root_nodes if n.type == "filename") == 1


def test_index_returns_empty_for_invalid_row():
    """ The start and end row removal signals should be emitted """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    project.plans.append(plan)

    model.set_project(project)
    plans_index = model.index(2, 0, QModelIndex())

    # When
    plan_index = model.index(10, 0, plans_index)

    # Then
    assert plan_index.isValid() is False


def test_index_returns_index_for_valid_row():
    """ The start and end row removal signals should be emitted """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    project.plans.append(plan)

    model.set_project(project)
    plans_index = model.index(2, 0, QModelIndex())

    # When
    plan_index = model.index(0, 0, plans_index)

    # Then
    assert plan_index.isValid() is True


def test_delete_calls_signals(qtbot):
    """ The start and end row removal signals should be emitted """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    project.plans.append(plan)

    model.set_project(project)
    plans_index = model.index(2, 0, QModelIndex())
    plan_index = model.index(0, 0, plans_index)

    # When
    with qtbot.waitSignals([model.rowsAboutToBeRemoved, model.rowsRemoved]):
        model.delete_node(plan_index)


def test_delete_does_not_call_signals_for_invalid_index(qtbot):
    """ The start and end row removal signals should not be emitted if the index is invalid"""
    # Given
    model = TreeModel()
    node = TreeNode("foo", None, None, 0)
    model.root_nodes.append(node)

    # When
    with qtbot.assertNotEmitted(model.rowsAboutToBeRemoved):
        with qtbot.assertNotEmitted(model.rowsRemoved):
            model.delete_node(QModelIndex())


def test_delete_removes_task():
    """ Delete removes task from underlying data structure """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    task = ResearchTask()
    plan.tasks.append(task)
    project.plans.append(plan)

    model.set_project(project)
    plans_index = model.index(2, 0, QModelIndex())
    plan_index = model.index(0, 0, plans_index)
    task_index = model.index(0, 0, plan_index)

    # When
    model.delete_node(task_index)

    # Then
    assert len(project.plans) == 1
    assert len(plan.tasks) == 0


def test_delete_removes_plan():
    """ Delete removes plan from underlying data structure """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    task = ResearchTask()
    plan.tasks.append(task)
    project.plans.append(plan)

    model.set_project(project)
    plans_index = model.index(2, 0, QModelIndex())
    plan_index = model.index(0, 0, plans_index)

    # When
    model.delete_node(plan_index)

    # Then
    assert len(project.plans) == 0


def test_add_creates_plan():
    """ Add should create a new plan in the underlying data structure """
    # Given
    model = TreeModel()
    project = ResearchProject("")

    model.set_project(project)
    plans_index = model.index(2, 0, QModelIndex())

    # When
    model.add_node(plans_index)

    # Then
    assert len(project.plans) == 1


def test_add_creates_task():
    """ Add should create a new task in the underlying data structure """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    project.plans.append(plan)

    model.set_project(project)
    plans_index = model.index(2, 0, QModelIndex())
    plan_index = model.index(0, 0, plans_index)

    # When
    model.add_node(plan_index)

    # Then
    assert len(project.plans) == 1
    assert len(plan.tasks) == 1


def test_set_data_doesnot_fire_signal_if_no_change(qtbot):
    """ When setting data, the dataChanged signal should only be emitted on actual changes """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    project.plans.append(plan)

    model.set_project(project)
    plans_index = model.index(2, 0, QModelIndex())
    plan_index = model.index(0, 0, plans_index)

    # When
    with qtbot.assertNotEmitted(model.dataChanged):
        model.setData(plan_index, plan.title, None)
