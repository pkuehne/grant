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
