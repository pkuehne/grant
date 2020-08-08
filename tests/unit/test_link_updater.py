""" Tests for the LinkUpdater class """

# from unittest import mock
import pytest
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QMessageBox
from grant.windows.link_updater import LinkUpdater
from grant.windows.data_context import DataContext
from grant.research import ResearchProject, ResearchPlan, ResearchTask
from grant.models.tree_model import TreeModel, TreeModelCols
from grant.models.individuals_model import IndividualsModel, Individual
from grant.models.sources_model import SourcesModel, Source


def test_has_pending_updates():
    """ If there are pending updates, this function should return true """
    # Given
    updater = LinkUpdater(DataContext())

    assert updater.has_pending_updates() is False

    # When
    updater.ancestor_updates = ["foo"]

    # Then
    assert updater.has_pending_updates() is True


def test_pending_updates_are_cleared():
    """
    If there are any previous pending changes, they are cleared before
    updates are calculated
    """

    # Given
    tree_model = TreeModel()
    tree_model.set_project(ResearchProject(""))

    individuals_model = IndividualsModel([])
    sources_model = SourcesModel([])

    context = DataContext(
        data_model=tree_model,
        individuals_model=individuals_model,
        sources_model=sources_model,
    )
    updater = LinkUpdater(context)
    updater.source_updates = ["Foo", "Bar"]
    updater.ancestor_fixes = ["Baz", "Fiz"]

    # When
    updater.calculate_updates()

    # Then
    assert updater.has_pending_updates() is False


def test_plan_links_are_checked():
    """
    Check the following:
    * Unchanged links are respected
    * Broken links are identified
    * Updated links are identified
    """

    # Given
    project = ResearchProject("")
    individuals = []
    sources = []

    indi_linked = Individual("I1234", "Link", "Indi", 1000, 2000)
    individuals.append(indi_linked)
    plan_linked = ResearchPlan()
    plan_linked.ancestor = indi_linked.autocomplete_name()
    plan_linked.ancestor_link = indi_linked.pointer
    project.plans.append(plan_linked)

    plan_broken = ResearchPlan()
    plan_broken.ancestor = "Broken Ancestor 1234/5678"
    plan_broken.ancestor_link = "FooBar"
    project.plans.append(plan_broken)

    indi_altered = Individual("I9876", "Altered", "Indi", 1000, 2000)
    individuals.append(indi_altered)
    plan_altered = ResearchPlan()
    plan_altered.ancestor = "Altered Ancestor 1000/2000"
    plan_altered.ancestor_link = indi_altered.pointer
    project.plans.append(plan_altered)

    tree_model = TreeModel()
    tree_model.set_project(project)

    individuals_model = IndividualsModel(individuals)
    sources_model = SourcesModel(sources)

    context = DataContext(
        data_model=tree_model,
        individuals_model=individuals_model,
        sources_model=sources_model,
    )
    updater = LinkUpdater(context)

    # When
    updater.calculate_updates()

    # Then
    assert updater.has_pending_updates() is True
    assert len(updater.ancestor_updates) == 1
    assert len(updater.source_updates) == 0


def test_task_links_are_checked():
    """
    Check the following:
    * Unchanged links are respected
    * Broken links are identified
    * Updated links are identified
    """

    # Given
    project = ResearchProject("")
    individuals = []
    sources = []

    plan = ResearchPlan()

    source_linked = Source("S123", "Linked", "Author", "Pub", "abbr")
    sources.append(source_linked)
    task_linked = ResearchTask()
    task_linked.source = source_linked.autocomplete_name()
    task_linked.source_link = source_linked.pointer
    plan.tasks.append(task_linked)

    task_broken = ResearchTask()
    task_broken.source = "Broken Source"
    task_broken.source_link = "FooBar"
    plan.tasks.append(task_broken)

    source_altered = Source("S987", "Altered", "Author", "Pub", "abbr")
    sources.append(source_altered)
    task_altered = ResearchTask()
    task_altered.source = "Altered Source"
    task_altered.source_link = source_altered.pointer
    plan.tasks.append(task_altered)

    project.plans.append(plan)

    tree_model = TreeModel()
    tree_model.set_project(project)

    individuals_model = IndividualsModel(individuals)
    sources_model = SourcesModel(sources)

    context = DataContext(
        data_model=tree_model,
        individuals_model=individuals_model,
        sources_model=sources_model,
    )
    updater = LinkUpdater(context)

    # When
    updater.calculate_updates()

    # Then
    assert updater.has_pending_updates() is True
    assert len(updater.ancestor_updates) == 0
    assert len(updater.source_updates) == 1


@pytest.fixture(name="link_updater")
def fixture_link_updater():
    """ Fixture to create an updater with uncommitted updates """
    tree_model = TreeModel()
    individuals_model = IndividualsModel([])
    sources_model = SourcesModel([])

    old_value = "Altered Ancestor"
    new_value = "Foo"

    project = ResearchProject("")
    plan_altered = ResearchPlan()
    plan_altered.ancestor = old_value
    plan_altered.ancestor_link = "I001"
    project.plans.append(plan_altered)
    tree_model.set_project(project)

    context = DataContext(
        data_model=tree_model,
        individuals_model=individuals_model,
        sources_model=sources_model,
    )

    updater = LinkUpdater(context)
    plan_index = tree_model.index(0, TreeModelCols.TEXT, QModelIndex())
    updater.ancestor_updates = [{"index": plan_index, "value": new_value}]

    return (updater, old_value, new_value, tree_model, plan_index)


def test_commit_aborts_without_confirmation(link_updater, qtbot, monkeypatch):
    """ commit does not update if the user does not confirm """

    # Given

    (updater, old_value, _, tree_model, plan_index) = link_updater
    monkeypatch.setattr(
        updater.confirmation_dialog, "exec_", lambda: QMessageBox.Cancel
    )

    # When
    with qtbot.assertNotEmitted(tree_model.dataChanged):
        updater.commit_updates()

    # Then
    assert plan_index.data() == old_value


def test_commit_updates_model_with_confirmation(link_updater, qtbot, monkeypatch):
    """ Committing the changes, updates the TreeModel """

    # Given
    (updater, _, new_value, tree_model, plan_index) = link_updater
    monkeypatch.setattr(updater.confirmation_dialog, "exec_", lambda: QMessageBox.Ok)

    # When
    with qtbot.waitSignal(tree_model.dataChanged):
        updater.commit_updates()

    # Then
    assert plan_index.data() == new_value
