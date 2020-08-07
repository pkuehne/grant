""" Test for the Tree Model """

import pytest
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from grant.models.tree_model import TreeModel, TreeModelCols
from grant.research import ResearchProject, ResearchPlan, ResearchTask, ResearchResult


def test_model_checker(qtmodeltester):
    """ Checks the model for basic issues """
    # Given
    model = TreeModel()

    qtmodeltester.check(model)


def test_only_column_count_returns_correct_number():
    """ Checks that the column count is correct """
    # Given
    model = TreeModel()

    # Then
    assert model.columnCount(QModelIndex()) == len(list(TreeModelCols))


def test_new_model_is_empty_by_default(qtmodeltester):
    """ Empty model should not have a project set and no nodes """
    # Given
    model = TreeModel()

    # Then
    qtmodeltester.check(model)
    assert model.project is None
    assert model.plans_node is None


@pytest.mark.parametrize("project", [ResearchProject(""), None])
def test_set_project_calls_begin_end_reset(project, qtbot, qtmodeltester):
    """ beginReset and endReset should be emitted """
    # Given
    model = TreeModel()

    # When
    with qtbot.waitSignals([model.modelAboutToBeReset, model.modelReset]):
        model.set_project(project)

    # Then
    qtmodeltester.check(model)


def test_set_project_clears_existing_nodes():
    """ Setting valid project should clear existing nodes """
    # Given
    model = TreeModel()
    project = ResearchProject("")

    # When
    model.set_project(project)
    model.set_project(project)

    # Then
    assert len(model.plans_node.children) == 0


def test_index_returns_empty_for_invalid_row():
    """ The start and end row removal signals should be emitted """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    project.plans.append(plan)

    model.set_project(project)

    # When
    plan_index = model.index(10, 0, model.plans_index)

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

    # When
    plan_index = model.index(0, 0, model.plans_index)

    # Then
    assert plan_index.isValid() is True


def test_has_children_handles_no_project_set():
    """ When no project is set, hasChildren should return False """
    # Given
    model = TreeModel()

    # Then
    assert model.hasChildren(QModelIndex()) is False


def test_has_children_handles_parent_index():
    """ When no project is set, hasChildren should return False """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    project.add_plan().add_task()
    model.set_project(project)

    # Then
    assert model.hasChildren(QModelIndex()) is True


def test_has_children_handles_plan_index():
    """ When no project is set, hasChildren should return False """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    project.add_plan().add_task()
    model.set_project(project)

    # Then
    assert model.hasChildren(model.index(0, 0, model.plans_index)) is True


def test_delete_does_nothing_on_invalid_index(qtbot):
    """ Delete removes task from underlying data structure """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    project.add_plan().add_task()
    model.set_project(project)

    # When
    with qtbot.assertNotEmitted(model.rowsAboutToBeRemoved):
        with qtbot.assertNotEmitted(model.rowsRemoved):
            model.delete_node(QModelIndex())

    # Then
    assert len(project.plans) == 1
    assert len(project.plans[0].tasks) == 1


def test_delete_calls_signals(qtbot):
    """ The start and end row removal signals should be emitted """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    project.plans.append(plan)

    model.set_project(project)
    plan_index = model.index(0, 0, model.plans_index)

    # When
    with qtbot.waitSignals([model.rowsAboutToBeRemoved, model.rowsRemoved]):
        model.delete_node(plan_index)


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
    plan_index = model.index(0, 0, model.plans_index)
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
    plan_index = model.index(0, 0, model.plans_index)

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

    # When
    model.add_node(model.plans_index)

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
    plan_index = model.index(0, 0, model.plans_index)

    # When
    model.add_node(plan_index)

    # Then
    assert len(project.plans) == 1
    assert len(plan.tasks) == 1


def test_setdata_doesnot_fire_signal_if_no_change(qtbot):
    """ When setting data, the dataChanged signal should only be emitted on actual changes """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    project.plans.append(plan)

    model.set_project(project)
    plan_index = model.index(0, 0, model.plans_index)

    # When
    with qtbot.assertNotEmitted(model.dataChanged):
        retval = model.setData(plan_index, plan.ancestor)

    assert retval is True


def test_setdata_fires_signal_on_change(qtbot):
    """ When setting data, the dataChanged signal is emitted on changes """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    project.plans.append(plan)

    model.set_project(project)
    plan_index = model.index(0, 0, model.plans_index)

    # When
    with qtbot.waitSignal(model.dataChanged):
        retval = model.setData(plan_index, "Foo")

    assert retval is True


def test_setdata_returns_false_on_invalid_index():
    """ When setting data, false is returned for invalid index """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    project.plans.append(plan)

    model.set_project(project)

    # When
    retval = model.setData(QModelIndex(), "Foo")

    assert retval is False


def test_setdata_returns_false_on_invalid_column():
    """ When setting data, false is returned for invalid column """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    project.plans.append(plan)

    model.set_project(project)
    plan_index = model.index(0, model.columnCount(None) + 1, model.plans_index)

    # When
    retval = model.setData(plan_index, "Foo")

    assert retval is False


def test_setdata_updates_description():
    """ setData() works on the description """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    project.plans.append(plan)

    model.set_project(project)
    plan_index = model.index(0, 1, model.plans_index)

    # When
    retval = model.setData(plan_index, "Foo")

    assert retval is True
    assert model.data(plan_index, Qt.DisplayRole) == "Foo"


def test_setdata_updates_result():
    """ setData() works on the result """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    project.plans.append(plan)
    project.plans[0].add_task()

    model.set_project(project)
    plan_index = model.index(0, 0, model.plans_index)
    task_index = model.index(0, 2, plan_index)

    result = ResearchResult(True)
    result.description = "Test"

    # When
    retval = model.setData(task_index, result)

    assert retval is True
    assert model.data(task_index, Qt.DisplayRole) == result


def test_setdata_updates_link():
    """ setData() works on the link """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    project.plans.append(plan)
    project.plans[0].add_task()

    model.set_project(project)
    plan_index = model.index(0, 0, model.plans_index)
    task_index = model.index(0, TreeModelCols.LINK, plan_index)

    # When
    retval = model.setData(task_index, 1234)

    assert retval is True
    assert model.data(task_index, Qt.DisplayRole) == 1234


def test_data_returns_none_for_invalid_index():
    """ When getting data, nothing is returned for invalid index """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    project.plans.append(plan)

    model.set_project(project)

    # When
    retval = model.data(QModelIndex(), Qt.DisplayRole)

    # Then
    assert retval is None


def test_data_returns_string_for_valid_index():
    """ When getting data, ancestor is returned for valid index """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    plan.ancestor = "Foo"
    project.plans.append(plan)

    model.set_project(project)
    plan_index = model.index(0, 0, model.plans_index)

    # When
    retval = model.data(plan_index, Qt.DisplayRole)

    # Then
    assert retval is plan.ancestor


def test_data_returns_none_for_invalid_column():
    """ When getting data, invalid column returns None """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    plan.ancestor = "Foo"
    project.plans.append(plan)

    model.set_project(project)
    plan_index = model.index(0, len(list(TreeModelCols)) + 1, model.plans_index)

    # When
    retval = model.data(plan_index, Qt.DisplayRole)

    # Then
    assert retval is None


def test_data_returns_qicon_for_decoration_role():
    """ When getting data, decoration role returns an icon """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    plan.ancestor = "Foo"
    project.plans.append(plan)

    model.set_project(project)
    plan_index = model.index(0, 0, model.plans_index)

    # When
    retval = model.data(plan_index, Qt.DecorationRole)

    # Then
    assert isinstance(retval, QIcon)


def test_data_returns_none_for_invalid_role():
    """ When getting data, invalid role returns None """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    plan.ancestor = "Foo"
    project.plans.append(plan)

    model.set_project(project)
    plan_index = model.index(0, 0, model.plans_index)

    # When
    retval = model.data(plan_index, Qt.UserRole)

    # Then
    assert retval is None


def test_get_font_returns_strikeout_for_task_with_result():
    """ A task with a nil result should show up as strike-out """
    # Given
    model = TreeModel()
    project = ResearchProject("")
    plan = ResearchPlan()
    task = ResearchTask()
    task.result = ResearchResult(False)
    plan.tasks.append(task)
    project.plans.append(plan)

    model.set_project(project)

    plan_index = model.index(0, 0, model.plans_index)
    task_index = model.index(0, 0, plan_index)

    # When
    font = model.data(task_index, Qt.FontRole)

    # Then
    assert font.strikeOut() is True


def test_header_data_set_for_valid_orientation():
    """ Check that the header data is correctly returned """
    # Given
    model = TreeModel()

    # Then
    assert model.headerData(0, Qt.Horizontal, Qt.DisplayRole) != ""


def test_header_data_none_for_invalid_orientation():
    """ Check that the header data is correctly returned """
    # Given
    model = TreeModel()

    # Then
    assert model.headerData(0, Qt.Vertical, Qt.DisplayRole) != ""


def test_flags_set_for_line_items():
    """ Check flags are set correctly for plans and tasks """
    # Given
    model = TreeModel()

    project = ResearchProject("")
    project.add_plan().add_task()
    model.set_project(project)

    # When
    plan_index = model.index(0, 0, model.plans_index)
    task_index = model.index(0, 0, plan_index)

    # Then
    plan_flags = int(model.flags(plan_index))
    task_flags = int(model.flags(task_index))

    assert plan_flags & Qt.ItemIsSelectable == Qt.ItemIsSelectable
    assert plan_flags & Qt.ItemIsEditable == Qt.ItemIsEditable
    assert plan_flags & Qt.ItemIsEnabled == Qt.ItemIsEnabled
    assert task_flags & Qt.ItemIsSelectable == Qt.ItemIsSelectable
    assert task_flags & Qt.ItemIsEditable == Qt.ItemIsEditable
    assert task_flags & Qt.ItemIsEnabled == Qt.ItemIsEnabled


def test_flags_no_flags_for_invalid_index():
    """ Check that no flags are returned for invalid index """
    # Given
    model = TreeModel()

    # project = ResearchProject("")
    # project.add_plan().add_task()

    # When
    plan_index = model.index(0, 0, model.plans_index)
    task_index = model.index(0, 0, plan_index)

    # Then
    assert model.flags(plan_index) == Qt.NoItemFlags
    assert model.flags(task_index) == Qt.NoItemFlags


def test_flags_not_editable_for_ancestor_column():
    """ The ancestor column should not be editable """
    model = TreeModel()

    project = ResearchProject("")
    project.add_plan().add_task()
    model.set_project(project)

    # When
    plan_index = model.index(0, TreeModelCols.ANCESTOR, model.plans_index)
    task_index = model.index(0, TreeModelCols.ANCESTOR, plan_index)

    # Then
    assert model.flags(plan_index) & Qt.ItemIsEditable != Qt.ItemIsEditable
    assert model.flags(task_index) & Qt.ItemIsEditable != Qt.ItemIsEditable
