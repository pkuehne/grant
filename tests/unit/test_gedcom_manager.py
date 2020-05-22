""" Tests for the gedcom manager """

from unittest import mock
from PyQt5.QtWidgets import QMessageBox
from grant.windows.gedcom_manager import GedcomManager
from grant.models.individuals_model import Individual


def test_load_link_filename_cannot_be_none():
    """ When loading a file, the filename cannot be None """
    # Given
    manager = GedcomManager()

    # When
    manager.load_link(None)


def test_load_link_filename_cannot_be_empty():
    """ When loading a file, the filename cannot be None """
    # Given
    manager = GedcomManager()

    # When
    manager.load_link("")


def test_load_link_invalid_filename_shows_message(monkeypatch):
    """
    When a file is specified that doesn't exist
    an error dialog is shown
    """
    # Given
    manager = GedcomManager()
    monkeypatch.setattr(QMessageBox, "warning", mock.MagicMock())

    # When
    manager.load_link("foo")

    # Then
    QMessageBox.warning.assert_called()  # pylint: disable=no-member


def test_loading_file_adds_individuals():
    """ When loading a gedcom file, individuals should be added to the list """
    # Given
    manager = GedcomManager()

    # When
    manager.load_link("tests/unit/test.ged")

    # Then
    assert len(manager.individuals) == 2


def test_loading_file_creates_model():
    """ When loading a gedcom file, individuals should be added to the list """
    # Given
    manager = GedcomManager()

    # When
    manager.load_link("tests/unit/test.ged")

    # Then
    assert manager.individuals_model.rowCount() != 0


def test_loading_creates_individual():
    """ Individuals should have their values set correctly """
    # Given
    manager = GedcomManager()

    # When
    manager.load_link("tests/unit/test.ged")

    # Then
    assert manager.individuals[0].pointer == "I0000"
    assert manager.individuals[1].pointer == "I0001"
    assert manager.individuals[0].first_name == "Adam Brian Charles"
    assert manager.individuals[0].last_name == "Dawson"
    assert manager.individuals[0].birth_year == 1801
    assert manager.individuals[0].death_year == 1851


def test_clear_link_removes_individuals():
    """ When the link is removed, the individuals cache should be cleared too """
    # Given
    manager = GedcomManager()
    manager.individuals.append(Individual("I000", "Test", "User", 1900, 1999))

    # When
    manager.clear_link()

    # Then
    assert len(manager.individuals) == 0
