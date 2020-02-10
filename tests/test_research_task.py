""" Tests for the ResearchTask class """

from grant.research import ResearchTask


def test_unset_fields_are_defaulted():
    """ Check that when converting a task, any fields not set in py are defaulted """
    # Given
    task = ResearchTask()
    task_data = {}

    # When
    task.from_py(task_data)

    # Then
    assert task.title != ""
    assert task.status != ""
