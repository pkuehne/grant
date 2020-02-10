""" Tests for the TasksModel """

from grant.windows.table_model import TableModel


def test_create():
    """ a """
    # Given
    model = TableModel()

    # Then
    assert model is not None
