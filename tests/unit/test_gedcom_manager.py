""" Tests for the gedcom manager """

from unittest import mock
from PyQt5.QtWidgets import QMessageBox
from grant.windows.gedcom_manager import GedcomManager
from grant.windows.data_context import DataContext
from grant.models.individuals_model import Individual
from grant.models.sources_model import Source


def test_load_link_filename_cannot_be_none():
    """ When loading a file, the filename cannot be None """
    # Given
    manager = GedcomManager(DataContext())

    # When
    manager.load_link(None)


def test_load_link_filename_cannot_be_empty():
    """ When loading a file, the filename cannot be None """
    # Given
    manager = GedcomManager(DataContext())

    # When
    manager.load_link("")


def test_load_link_invalid_filename_shows_message(monkeypatch):
    """
    When a file is specified that doesn't exist
    an error dialog is shown
    """
    # Given
    manager = GedcomManager(DataContext())
    monkeypatch.setattr(QMessageBox, "warning", mock.MagicMock())

    # When
    manager.load_link("foo")

    # Then
    QMessageBox.warning.assert_called()  # pylint: disable=no-member


def test_loading_file_creates_models():
    """ When loading a gedcom file, models should be populated """
    # Given
    manager = GedcomManager(DataContext())

    # When
    manager.load_link("tests/unit/test.ged")

    # Then
    assert manager.data_context.individuals_model.rowCount() != 0
    assert manager.data_context.sources_model.rowCount() != 0


def test_loading_creates_individuals():
    """ Individuals should have their values set correctly """
    # Given
    manager = GedcomManager(DataContext())

    # When
    manager.load_link("tests/unit/test.ged")

    # Then
    assert len(manager.individuals) == 2
    assert manager.individuals[0].pointer == "I0000"
    assert manager.individuals[1].pointer == "I0001"
    assert manager.individuals[0].first_name == "Adam Brian Charles"
    assert manager.individuals[0].last_name == "Dawson"
    assert manager.individuals[0].birth_year == 1801
    assert manager.individuals[0].death_year == 1851


def test_loading_creates_sources():
    """ Sources should have their values set correctly """
    # Given
    manager = GedcomManager(DataContext())

    # When
    manager.load_link("tests/unit/test.ged")

    # Then
    assert len(manager.sources) == 2
    assert manager.sources[0].pointer == "S0000"
    assert manager.sources[1].pointer == "S0001"
    assert manager.sources[0].title == "Grantham Church Books 1705-1767"
    assert manager.sources[0].author == "Grantham Diocese"
    assert manager.sources[0].publisher == "Ancestry.com"
    assert manager.sources[0].abbreviation == "GCB17"


def test_clear_link_removes_caches():
    """ When the link is removed, the caches should be cleared too """
    # Given
    manager = GedcomManager(DataContext())
    manager.individuals.append(Individual("I000", "Test", "User", 1900, 1999))
    manager.sources.append(Source("S000", "Test", "User", "S/O", "ABB"))

    # When
    manager.clear_link()

    # Then
    assert len(manager.individuals) == 0
    assert len(manager.sources) == 0


def test_refresh_link_reloads_file():
    """ When the link is removed, the caches should be cleared too """
    # Given
    manager = GedcomManager(DataContext())
    manager.individuals.append(Individual("IND01", "Test", "User", 1900, 1999))
    manager.sources.append(Source("SOU01", "Test", "User", "S/O", "ABB"))

    # When
    manager.refresh_link("tests/unit/test.ged")

    # Then
    assert len(manager.individuals) == 2
    assert manager.individuals[0].pointer == "I0000"
    assert len(manager.sources) == 2
    assert manager.sources[0].pointer == "S0000"
