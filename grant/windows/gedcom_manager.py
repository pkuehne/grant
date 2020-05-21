""" Manages the gedcom file link """

from gedcom.parser import Parser
from gedcom.element.individual import IndividualElement


class GedcomManager:
    """ Manager for the gedcom link """

    def __init__(self):
        self.parser = Parser()
        self.individuals = {}

    def load_link(self, file_path):
        """ Loads filename and parses file """
        self.parser.parse_file(file_path)
        root_child_elements = self.parser.get_root_child_elements()

        for element in root_child_elements:
            if isinstance(element, IndividualElement):
                self.add_individual(element)

    def add_individual(self, element: IndividualElement):
        """ Adds an individual to the list """
        pointer = element.get_pointer()[1:-1]
        (first, last) = element.get_name()
        full_name = first + " " + last

        birth_year = element.get_birth_year()
        death_year = element.get_death_year()
        alive_range = str(birth_year) + "-" + str(death_year)

        self.individuals[pointer] = (
            pointer + ": " + full_name + " (" + alive_range + ")"
        )

    def clear_link(self):
        """ Unset everything """
        self.individuals.clear()
