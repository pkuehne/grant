""" Manages the gedcom file link """

from typing import List
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox
from gedcom.parser import Parser
from gedcom.element.individual import Element, IndividualElement
from gedcom.tags import GEDCOM_TAG_SOURCE
from grant.models.individuals_model import Individual
from grant.models.sources_model import Source
from grant.windows.data_context import DataContext


class GedcomManager(QObject):
    """ Manager for the gedcom link """

    def __init__(self, data_context: DataContext, parent=None):
        super().__init__(parent)
        self.parser = Parser()
        self.individuals: List[Individual] = []
        self.sources: List[Source] = []
        self.data_context = data_context

    def load_link(self, file_path):
        """ Loads filename and parses file """
        if file_path is None or file_path == "":
            return
        try:
            self.parser.parse_file(file_path)
        except FileNotFoundError:
            QMessageBox.warning(
                self.parent(),
                "Invalid Gedcom File",
                "The gedcom file at '" + file_path + "' could not be found",
                QMessageBox.Ok,
            )
            return
        root_child_elements = self.parser.get_root_child_elements()

        for element in root_child_elements:
            if isinstance(element, IndividualElement):
                self.add_individual(element)
            if element.get_tag() == GEDCOM_TAG_SOURCE:
                self.add_source(element)
        self.data_context.individuals_model.update_list(self.individuals)
        self.data_context.sources_model.update_list(self.sources)

    def add_individual(self, element: IndividualElement):
        """ Adds an individual to the list """
        pointer = element.get_pointer()[1:-1]
        (first, last) = element.get_name()
        birth_year = element.get_birth_year()
        death_year = element.get_death_year()

        self.individuals.append(
            Individual(pointer, first, last, birth_year, death_year)
        )

    def add_source(self, source: Element):
        """ Adds a source to the list """
        pointer = source.get_pointer()[1:-1]
        title = ""
        author = ""
        publisher = ""
        abbreviation = ""
        for element in source.get_child_elements():
            if element.get_tag() == "TITL":
                title = element.get_value()
            if element.get_tag() == "AUTH":
                author = element.get_value()
            if element.get_tag() == "PUBL":
                publisher = element.get_value()
            if element.get_tag() == "ABBR":
                abbreviation = element.get_value()
        self.sources.append(Source(pointer, title, author, publisher, abbreviation))

    def clear_link(self):
        """ Unset everything """
        self.individuals.clear()
        self.sources.clear()
        self.data_context.individuals_model.update_list([])
        self.data_context.sources_model.update_list([])
