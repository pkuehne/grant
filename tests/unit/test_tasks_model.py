""" Tests for the TasksModel """

from grant.models.tasks_model import TasksModel


def test_create():
    """ a """
    # Given
    model = TasksModel()

    # Then
    assert model is not None
