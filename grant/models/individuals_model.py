""" Model holding the Gedcom individuals """

from typing import List
from enum import IntEnum, unique
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt


@unique
class IndividualsModelColumns(IntEnum):
    """ Enum for the Model columns """

    POINTER = 0
    FIRST_NAME = 1
    LAST_NAME = 2
    BIRTH_YEAR = 3
    DEATH_YEAR = 4
    AUTOCOMPLETE = 5


class Individual:
    """ Bridge representation of an Individual """

    def __init__(
        self,
        pointer: str,
        first_name: str,
        last_name: str,
        birth_year: int,
        death_year: int,
    ):
        self.pointer = pointer
        self.first_name = first_name
        self.last_name = last_name
        self.birth_year = birth_year
        self.death_year = death_year

    def autocomplete_name(self):
        """ The name to appear in autocomplete lists """
        full_name = f"{self.first_name} {self.last_name}"
        life_span = f"({self.birth_year}-{self.death_year})"
        return f"{full_name} {life_span}"


class IndividualsModel(QAbstractTableModel):
    """ Model representation of Gedcom Individuals """

    def __init__(self, individuals: List[Individual] = None):
        super().__init__()
        self.individuals: List[Individual] = individuals if individuals else []

    def update_list(self, individuals: List[Individual]):
        """ Updates the internal representation """
        self.beginResetModel()
        self.individuals = individuals
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):  # pylint: disable=invalid-name
        """ Number of individuals """
        if parent.isValid():
            return 0
        return len(self.individuals)

    def columnCount(
        self, parent=QModelIndex()
    ):  # pylint: disable=invalid-name, no-self-use
        """ Columns in the model """
        if parent.isValid():
            return 0
        return len(list(IndividualsModelColumns))

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        """ Get individual for a row/column """
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        individual = self.individuals[index.row()]

        if index.column() == IndividualsModelColumns.POINTER:
            return individual.pointer
        if index.column() == IndividualsModelColumns.FIRST_NAME:
            return individual.first_name
        if index.column() == IndividualsModelColumns.LAST_NAME:
            return individual.last_name
        if index.column() == IndividualsModelColumns.BIRTH_YEAR:
            return individual.birth_year
        if index.column() == IndividualsModelColumns.DEATH_YEAR:
            return individual.death_year
        if index.column() == IndividualsModelColumns.AUTOCOMPLETE:
            return individual.autocomplete_name()
