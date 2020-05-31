""" tests for the individuals model """

import pytest
from PyQt5.QtCore import QModelIndex
from grant.models.individuals_model import IndividualsModel
from grant.models.individuals_model import Individual
from grant.models.individuals_model import IndividualsModelColumns


@pytest.fixture
def three_indi_model():
    """ Fixture to create a basic model """
    individuals = []
    individuals.append(Individual("I001", "Foo1", "Person", 1901, 1951))
    individuals.append(Individual("I002", "Foo2", "Person", 1902, 1952))
    individuals.append(Individual("I003", "Foo3", "Person", 1903, 1953))

    return IndividualsModel(individuals)


def test_column_count_is_nonzero():
    """ Even for an empty model, there should be columns defined """
    # Given

    # When
    model = IndividualsModel()

    # Then
    assert model.columnCount() > 0
    assert model.rowCount() == 0


def test_setting_list_sets_row_count(
    three_indi_model,
):  # pylint: disable=redefined-outer-name
    """ The number of items in the list should be the row count """
    # Then
    assert three_indi_model.rowCount() != 0


def test_column_count_not_recursive(
    three_indi_model,
):  # pylint: disable=redefined-outer-name
    """ Column count for an item should be zero """
    # Then
    assert three_indi_model.columnCount(three_indi_model.index(0, 0)) == 0


def test_row_count_not_recursive(
    three_indi_model,
):  # pylint: disable=redefined-outer-name
    """ Row count for an item should be zero """
    # Then
    assert three_indi_model.rowCount(three_indi_model.index(0, 0)) == 0


def test_data_returns_none_for_invalid_index(
    three_indi_model,
):  # pylint: disable=redefined-outer-name
    """ When an invalid index is passed to data(), None should be returned """
    # When
    retval = three_indi_model.data(QModelIndex())

    # Then
    assert retval is None


def test_data_returns_pointer_held_in_column(
    three_indi_model,
):  # pylint: disable=redefined-outer-name
    """ A given column should hold the pointer """
    # Given
    index = three_indi_model.index(0, 0)

    # When
    pointer = three_indi_model.data(index)

    # Then
    assert pointer == "I001"


def test_data_returns_values_in_individual_record():
    """ Check the first name """
    # Given
    individuals = []
    indi = Individual("I001", "Test", "Person", 1901, 1951)
    individuals.append(indi)

    model = IndividualsModel(individuals)

    # When
    pointer = model.data(model.index(0, IndividualsModelColumns.POINTER))
    first = model.data(model.index(0, IndividualsModelColumns.FIRST_NAME))
    last = model.data(model.index(0, IndividualsModelColumns.LAST_NAME))
    birth = model.data(model.index(0, IndividualsModelColumns.BIRTH_YEAR))
    death = model.data(model.index(0, IndividualsModelColumns.DEATH_YEAR))
    autocomplete = model.data(model.index(0, IndividualsModelColumns.AUTOCOMPLETE))
    # Then
    assert model.columnCount() == 6
    assert pointer == indi.pointer
    assert first == indi.first_name
    assert last == indi.last_name
    assert birth == indi.birth_year
    assert death == indi.death_year
    assert autocomplete != ""


def test_autocomplete_name_includes_relevant_data():
    """ Check the first name """
    # Given
    individuals = []
    indi = Individual("I001", "Test", "Person", 1901, 1951)
    individuals.append(indi)

    model = IndividualsModel(individuals)
    index = model.index(0, IndividualsModelColumns.AUTOCOMPLETE)

    # When
    descriptive_name = model.data(index)

    # Then
    assert indi.pointer not in descriptive_name
    assert indi.first_name in descriptive_name
    assert indi.last_name in descriptive_name
    assert str(indi.birth_year) in descriptive_name
    assert str(indi.death_year) in descriptive_name


def test_update_list_changes_data(qtbot):
    """ Check the first name """
    # Given
    model = IndividualsModel()
    assert model.rowCount() == 0

    individuals = []
    indi = Individual("I001", "Test", "Person", 1901, 1951)
    individuals.append(indi)

    # When
    with qtbot.waitSignals([model.modelAboutToBeReset, model.modelReset]):
        model.update_list(individuals)

    # Then
    assert model.rowCount() == 1
