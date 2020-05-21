""" Tests for the gedcom manager """

from grant.windows.gedcom_manager import GedcomManager


def test_loading_file_adds_individuals():
    """ When loading a gedcom file, individuals should be added to the list """
    # Given
    manager = GedcomManager()

    # When
    manager.load_link("tests/unit/test.ged")

    # Then
    assert len(manager.individuals) == 2


def test_individuals_include_names():
    """ Individuals should have their name included """
    # Given
    manager = GedcomManager()

    # When
    manager.load_link("tests/unit/test.ged")

    # Then
    assert "Adam Brian Charles Dawson" in list(manager.individuals.values())[0]


def test_individuals_include_birth_year_if_set():
    """ Birth year should be included if it is set """
    # Given
    manager = GedcomManager()

    # When
    manager.load_link("tests/unit/test.ged")

    # Then
    assert "1801" in list(manager.individuals.values())[0]


def test_individuals_include_death_year_if_set():
    """ Death year should be included if it is set """
    # Given
    manager = GedcomManager()

    # When
    manager.load_link("tests/unit/test.ged")

    # Then
    assert "1851" in list(manager.individuals.values())[0]


def test_individuals_include_pointer():
    """ Death year should be included if it is set """
    # Given
    manager = GedcomManager()

    # When
    manager.load_link("tests/unit/test.ged")

    # Then
    assert "I0000" in list(manager.individuals.values())[0]
    assert "@" not in list(manager.individuals.values())[0]
    assert "I0001" in list(manager.individuals.values())[1]
    assert "@" not in list(manager.individuals.values())[1]


def test_clear_link_removes_individuals():
    """ When the link is removed, the individuals cache should be cleared too """
    # Given
    manager = GedcomManager()
    manager.individuals["I0000"] = "Test Person (1234-1256)"

    # When
    manager.clear_link()

    # Then
    assert len(manager.individuals) == 0
