""" Test for the Tree Model """

from gene.windows.tree_model import TreeNode
from gene.windows.tree_model import TreeModel
from gene.research import ResearchProject


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
