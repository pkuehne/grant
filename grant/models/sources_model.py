""" Model holding the Gedcom sources """

from typing import List
from enum import IntEnum, unique
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt


@unique
class SourcesModelColumns(IntEnum):
    """ Enum for the Model columns """

    POINTER = 0
    TITLE = 1
    AUTHOR = 2
    PUBLISHER = 3
    ABBREVIATION = 4
    AUTOCOMPLETE = 5


class Source:
    """ Bridge representation of a Source """

    def __init__(
        self, pointer: str, title: str, author: str, publisher: str, abbreviation: str,
    ):
        self.pointer = pointer
        self.title = title
        self.author = author
        self.publisher = publisher
        self.abbreviation = abbreviation

    def autocomplete_name(self):
        """ The name to appear in autocomplete lists """
        author = f"{self.author}, " if self.author != "" else ""
        return f"{author}{self.title}"


class SourcesModel(QAbstractTableModel):
    """ Model representation of Gedcom Sources """

    def __init__(self, sources: List[Source] = None):
        super().__init__()
        self.sources: List[Source] = sources if sources else []

    def update_list(self, sources: List[Source]):
        """ Updates the internal representation """
        self.beginResetModel()
        self.sources = sources
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):  # pylint: disable=invalid-name
        """ Number of sources """
        if parent.isValid():
            return 0
        return len(self.sources)

    def columnCount(
        self, parent=QModelIndex()
    ):  # pylint: disable=invalid-name, no-self-use
        """ Columns in the model """
        if parent.isValid():
            return 0
        return len(list(SourcesModelColumns))

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        """ Get source data for a row/column """
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        source = self.sources[index.row()]

        return {
            SourcesModelColumns.POINTER: source.pointer,
            SourcesModelColumns.TITLE: source.title,
            SourcesModelColumns.AUTHOR: source.author,
            SourcesModelColumns.PUBLISHER: source.publisher,
            SourcesModelColumns.ABBREVIATION: source.abbreviation,
            SourcesModelColumns.AUTOCOMPLETE: source.autocomplete_name(),
        }[index.column()]
