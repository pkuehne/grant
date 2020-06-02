""" tests for the sources model """

import pytest
from PyQt5.QtCore import QModelIndex
from grant.models.sources_model import SourcesModel
from grant.models.sources_model import Source
from grant.models.sources_model import SourcesModelColumns


@pytest.fixture
def three_sour_model():
    """ Fixture to create a basic model """
    sources = []
    sources.append(Source("I001", "Foo1", "Person", "Pub", "Abbr"))
    sources.append(Source("I002", "Foo2", "Person", "Pub", "Abbr"))
    sources.append(Source("I003", "Foo3", "Person", "Pub", "Abbr"))

    return SourcesModel(sources)


def test_column_count_is_nonzero():
    """ Even for an empty model, there should be columns defined """
    # Given

    # When
    model = SourcesModel()

    # Then
    assert model.columnCount() > 0
    assert model.rowCount() == 0


def test_setting_list_sets_row_count(
    three_sour_model,
):  # pylint: disable=redefined-outer-name
    """ The number of items in the list should be the row count """
    # Then
    assert three_sour_model.rowCount() != 0


def test_column_count_not_recursive(
    three_sour_model,
):  # pylint: disable=redefined-outer-name
    """ Column count for an item should be zero """
    # Then
    assert three_sour_model.columnCount(three_sour_model.index(0, 0)) == 0


def test_row_count_not_recursive(
    three_sour_model,
):  # pylint: disable=redefined-outer-name
    """ Row count for an item should be zero """
    # Then
    assert three_sour_model.rowCount(three_sour_model.index(0, 0)) == 0


def test_data_returns_none_for_invalid_index(
    three_sour_model,
):  # pylint: disable=redefined-outer-name
    """ When an invalid index is passed to data(), None should be returned """
    # When
    retval = three_sour_model.data(QModelIndex())

    # Then
    assert retval is None


def test_data_returns_pointer_held_in_column(
    three_sour_model,
):  # pylint: disable=redefined-outer-name
    """ A given column should hold the pointer """
    # Given
    index = three_sour_model.index(0, 0)

    # When
    pointer = three_sour_model.data(index)

    # Then
    assert pointer == "I001"


def test_data_returns_values_in_source_record():
    """ Check the first name """
    # Given
    sources = []
    source = Source("I001", "Test", "Person", "Pub", "Abbr")
    sources.append(source)

    model = SourcesModel(sources)

    # When
    pointer = model.data(model.index(0, SourcesModelColumns.POINTER))
    title = model.data(model.index(0, SourcesModelColumns.TITLE))
    author = model.data(model.index(0, SourcesModelColumns.AUTHOR))
    publisher = model.data(model.index(0, SourcesModelColumns.PUBLISHER))
    abbreviation = model.data(model.index(0, SourcesModelColumns.ABBREVIATION))
    autocomplete = model.data(model.index(0, SourcesModelColumns.AUTOCOMPLETE))
    # Then
    assert model.columnCount() == 6
    assert pointer == source.pointer
    assert title == source.title
    assert author == source.author
    assert publisher == source.publisher
    assert abbreviation == source.abbreviation
    assert autocomplete != ""


def test_autocomplete_name_includes_relevant_data():
    """ Check the first name """
    # Given
    sources = []
    source = Source("I001", "Test", "Person", "Pub", "Abbr")
    sources.append(source)

    model = SourcesModel(sources)
    index = model.index(0, SourcesModelColumns.AUTOCOMPLETE)

    # When
    descriptive_name = model.data(index)

    # Then
    assert source.pointer not in descriptive_name
    assert source.title in descriptive_name
    assert source.author in descriptive_name


def test_autocomplete_name_no_comma_if_no_author():
    """ Check the first name """
    # Given
    sources = []
    source = Source("I001", "Test", "", "Pub", "Abbr")
    sources.append(source)

    model = SourcesModel(sources)
    index = model.index(0, SourcesModelColumns.AUTOCOMPLETE)

    # When
    descriptive_name = model.data(index)

    # Then
    assert "," not in descriptive_name
    assert descriptive_name == source.title


def test_update_list_changes_data(qtbot):
    """ Check the first name """
    # Given
    model = SourcesModel()
    assert model.rowCount() == 0

    sources = []
    source = Source("I001", "Test", "Person", "Pub", "Abbr")
    sources.append(source)

    # When
    with qtbot.waitSignals([model.modelAboutToBeReset, model.modelReset]):
        model.update_list(sources)

    # Then
    assert model.rowCount() == 1
