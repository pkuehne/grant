""" Detail View for a plan """

from PyQt5.QtWidgets import QVBoxLayout, QFormLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QGroupBox
from PyQt5.QtWidgets import QDataWidgetMapper
from grant.windows.base_screens import DetailScreen
from grant.windows.linkedlineedit_widget import LinkedLineEdit
from grant.models.individuals_model import IndividualsModelColumns
from grant.models.tree_model import TreeModelCols


class PlanDetails(DetailScreen):
    """ Displays all current Research Plans """

    def __init__(self, data_context):
        super(PlanDetails, self).__init__(data_context)

        form_layout = QFormLayout()
        self.ancestor = LinkedLineEdit(
            self.data_context.individuals_model,
            IndividualsModelColumns.AUTOCOMPLETE,
            IndividualsModelColumns.POINTER,
        )
        self.ancestor.link_updated.connect(self.link_updated)
        form_layout.addRow(QLabel("Ancestor:"), self.ancestor)

        self.goal = QTextEdit()
        form_layout.addRow(QLabel("Goal:"), self.goal)

        form_group = QGroupBox("Plan")
        form_group.setLayout(form_layout)

        layout = QVBoxLayout()
        layout.addWidget(form_group)

        # Don't add this, we just want to get/set the value
        self.link = QLineEdit()

        self.setLayout(layout)

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.data_context.data_model)
        self.mapper.addMapping(self.ancestor, TreeModelCols.TEXT)
        self.mapper.addMapping(self.goal, TreeModelCols.DESCRIPTION, b"plainText")
        self.mapper.addMapping(self.link, TreeModelCols.LINK)
        self.mapper.currentIndexChanged.connect(
            lambda _: self.ancestor.set_link_visible(self.link.text() != "")
        )
        self.data_context.data_model.dataChanged.connect(
            lambda _, __: self.ancestor.set_link_visible(self.link.text() != "")
        )
        self.mapper.toFirst()

    def link_updated(self, text: str):
        """ Called when the link needs updating from the LineEdit """
        self.link.setText(text)
        self.mapper.submit()
