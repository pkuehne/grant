""" Detail View for a plan """

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QGroupBox
from PyQt5.QtWidgets import QDataWidgetMapper
from grant.windows.base_screens import DetailScreen
from grant.windows.result_widget import ResultWidget
from grant.windows.linkedlineedit_widget import LinkedLineEdit
from grant.models.sources_model import SourcesModelColumns
from grant.models.tree_model import TreeModelCols


class TaskDetails(DetailScreen):
    """ Displays all current Research Plans """

    def __init__(self, data_context):
        super().__init__(data_context)

        form_layout = QFormLayout()
        self.source = LinkedLineEdit(
            self.data_context.sources_model,
            SourcesModelColumns.AUTOCOMPLETE,
            SourcesModelColumns.POINTER,
        )
        self.source.link_updated.connect(self.link_updated)
        form_layout.addRow(QLabel("Source:"), self.source)

        self.description = QTextEdit()
        form_layout.addRow(QLabel("Description:"), self.description)

        self.result = ResultWidget()
        form_layout.addRow(QLabel("Results:"), self.result)

        form_group = QGroupBox("Task")
        form_group.setLayout(form_layout)

        layout = QVBoxLayout()
        layout.addWidget(form_group)

        # Don't add this, we just want to get/set the value
        self.link = QLineEdit()

        self.setLayout(layout)

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.data_context.data_model)
        self.mapper.addMapping(self.source, TreeModelCols.TEXT)
        self.mapper.addMapping(
            self.description, TreeModelCols.DESCRIPTION, b"plainText"
        )
        self.mapper.addMapping(self.result, TreeModelCols.RESULT)
        self.mapper.addMapping(self.link, TreeModelCols.LINK)
        self.result.result_changed.connect(self.mapper.submit)
        self.mapper.currentIndexChanged.connect(
            lambda _: self.source.set_link_visible(self.link.text() != "")
        )
        self.data_context.data_model.dataChanged.connect(
            lambda _, __: self.source.set_link_visible(self.link.text() != "")
        )
        self.mapper.toFirst()

    def link_updated(self, text: str):
        """ Called when the link needs updating from the LineEdit """
        self.link.setText(text)
        self.mapper.submit()
