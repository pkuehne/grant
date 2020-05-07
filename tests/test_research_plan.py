""" Tests related to the ResearchPlan class """

from grant.research import ResearchPlan
from grant.research import ResearchTask


def test_unset_fields_are_defaulted():
    """ Check that when converting a plan, any fields not set in py are defaulted """
    # Given
    plan = ResearchPlan()
    plan_data = {}

    # When
    plan.from_py(plan_data)

    # Then
    assert plan.ancestor != ""


def test_add_task_creates_and_returns():
    """ add_task() should return the newly created task """
    # Given
    plan = ResearchPlan()

    # When
    retval = plan.add_task()

    # Then
    assert len(plan.tasks) == 1
    assert retval is not None


def test_delete_task_does_nothing_if_no_tasks():
    """ delete_task() does nothing if there are no tasks """
    # Given
    plan = ResearchPlan()

    # When
    plan.delete_task(1)

    # Then
    assert len(plan.tasks) == 0


def test_delete_task_deletes_the_specified_task():
    """ delete_task() does nothing if there are no tasks """
    # Given
    plan = ResearchPlan()
    task_one = ResearchTask()
    task_two = ResearchTask()
    task_three = ResearchTask()

    plan.tasks.append(task_one)
    plan.tasks.append(task_two)
    plan.tasks.append(task_three)

    # When
    plan.delete_task(1)

    # Then
    assert len(plan.tasks) == 2
    assert plan.tasks[0] == task_one
    assert plan.tasks[1] == task_three


def test_delete_task_does_nothing_if_index_out_of_bounds():
    """ delete_task() does nothing if the index is too large """
    # Given
    plan = ResearchPlan()
    task_one = ResearchTask()
    task_two = ResearchTask()
    task_three = ResearchTask()

    plan.tasks.append(task_one)
    plan.tasks.append(task_two)
    plan.tasks.append(task_three)

    # When
    plan.delete_task(5)

    # Then
    assert len(plan.tasks) == 3


def test_string_repr_includes_ancestor():
    """ The str() representation should include the ancestor """
    # Given
    plan = ResearchPlan()
    plan.ancestor = "ANCESTOR"

    # When
    string = str(plan)

    # Then
    assert plan.ancestor in string


def test_to_py_sets_fields():
    """ The to_py() function should create a python data structure of the class fields """
    # Given
    plan = ResearchPlan()
    plan.ancestor = "ANCESTOR"

    # When
    data = plan.to_py()

    # Then
    assert data["ancestor"] == plan.ancestor
    assert data["goal"] == plan.goal
    assert data["tasks"] == plan.tasks
    assert len(data.keys()) == 3  # To verify nothing else was added
