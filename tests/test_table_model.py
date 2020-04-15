""" Tests for the TasksModel """

from grant.models.tree_model import TreeModel
from grant.models.table_model import TableModel


def test_basic_checks(qtmodeltester):
    """ Check the model for basic issues """
    # Given
    tree = TreeModel()
    model = TableModel()
    model.setSourceModel(tree)

    # Then
    qtmodeltester.check(model)
