""" Holds all data models for the application """

from dataclasses import dataclass
from grant.models.tree_model import TreeModel
from grant.models.individuals_model import IndividualsModel
from grant.models.sources_model import SourcesModel


@dataclass
class DataContext:
    """ Holder of all data models """

    data_model: TreeModel
    individuals_model: IndividualsModel

    def __init__(self, data_model=None, individuals_model=None, sources_model=None):
        self.data_model = TreeModel() if data_model is None else data_model
        self.individuals_model = (
            IndividualsModel([]) if individuals_model is None else individuals_model
        )
        self.sources_model = (
            SourcesModel([]) if sources_model is None else sources_model
        )
