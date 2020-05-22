""" Manages the gedcom file link """

from typing import List
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox
from gedcom.parser import Parser
from gedcom.element.individual import IndividualElement
from grant.models.individuals_model import (
    IndividualsModel,
    Individual,
)


class GedcomManager(QObject):
    """ Manager for the gedcom link """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parser = Parser()
        self.individuals: List[Individual] = []
        self.individuals_model = IndividualsModel([])

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
        self.individuals_model = IndividualsModel(self.individuals)

    def add_individual(self, element: IndividualElement):
        """ Adds an individual to the list """
        pointer = element.get_pointer()[1:-1]
        (first, last) = element.get_name()
        birth_year = element.get_birth_year()
        death_year = element.get_death_year()

        self.individuals.append(
            Individual(pointer, first, last, birth_year, death_year)
        )

    def clear_link(self):
        """ Unset everything """
        self.individuals.clear()
        self.individuals_model = IndividualsModel([])
