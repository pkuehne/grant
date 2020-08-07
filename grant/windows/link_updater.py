""" Update linked items from Gedcom """

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from grant.models.sources_model import SourcesModelColumns
from grant.models.individuals_model import IndividualsModelColumns
from grant.models.tree_model import TreeModelCols
from grant.windows.data_context import DataContext


class LinkUpdater:
    """
    Updates the ResearchProject task/source values from the linked GEDCOM
    file, based on the relevant link field
    """

    def __init__(self, context: DataContext):
        self.data_context = context
        self.source_updates = []
        self.ancestor_updates = []

        self.setup_confirmation_dialog()

    def setup_confirmation_dialog(self):
        """ Sets up the break-link confirmation dialog """
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Warning)
        dialog.setWindowIcon(QIcon(":/icons/grant.ico"))
        dialog.setWindowTitle("Are you sure?")
        dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        self.confirmation_dialog = dialog

    def has_pending_updates(self) -> bool:
        """ Whether there are any updates waiting to be applied """
        pending_updates = len(self.source_updates) + len(self.ancestor_updates)
        return pending_updates != 0

    def calculate_updates(self):
        """
        Checks whether any names in the project can be updated from the linked gedcom file
        """

        plans: int = self.data_context.data_model.rowCount(QModelIndex())
        for plan_row in range(plans):
            plan_index = self.data_context.data_model.index(
                plan_row, TreeModelCols.LINK, QModelIndex()
            )
            self._process_plan_index(plan_index)
            tasks: int = self.data_context.data_model.rowCount(plan_index)
            for task_row in range(tasks):
                task_index = self.data_context.data_model.index(
                    task_row, TreeModelCols.LINK, plan_index
                )
                self._process_task_index(task_index)

    def _process_plan_index(self, plan_index: QModelIndex):
        """ blah """
        if plan_index.data() == "":
            return
        start_index = self.data_context.individuals_model.index(0, 0)

        matches = self.data_context.individuals_model.match(
            start_index, Qt.DisplayRole, plan_index.data()
        )
        if len(matches) != 1:
            print("Broken Link - " + f"Plan {plan_index.row()}: {len(matches)} matches")
            return
        gedcom_value = (
            matches[0].siblingAtColumn(IndividualsModelColumns.AUTOCOMPLETE).data()
        )
        plan_text = plan_index.siblingAtColumn(TreeModelCols.TEXT)
        if gedcom_value != plan_text.data():
            # print(f"Gedcom has changed: {plan_text} -> {gedcom_value}")
            self.ancestor_updates.append({"index": plan_text, "value": gedcom_value})

    def _process_task_index(self, task_index: QModelIndex):
        """ blah """
        if task_index.data() == "":
            return
        start_index = self.data_context.sources_model.index(0, 0)

        matches = self.data_context.sources_model.match(
            start_index, Qt.DisplayRole, task_index.data()
        )
        if len(matches) != 1:
            print("Broken Link - " + f"Task {task_index.row()}: {len(matches)} matches")
            return
        gedcom_value = (
            matches[0].siblingAtColumn(SourcesModelColumns.AUTOCOMPLETE).data()
        )
        task_text = task_index.siblingAtColumn(TreeModelCols.TEXT)
        if gedcom_value != task_text.data():
            # print(f"Gedcom has changed: {task_text} -> {gedcom_value}")
            self.source_updates.append({"index": task_text, "value": gedcom_value})

    def commit_updates(self):
        """ Commit the pending updates """
        num_ancestor_updates = len(self.ancestor_updates)
        num_source_updates = len(self.source_updates)

        ancestor_text = (
            f"• {num_ancestor_updates} ancestor name changes\n"
            if num_ancestor_updates
            else ""
        )
        source_text = (
            f"• {num_source_updates} source name changes\n"
            if num_source_updates
            else ""
        )

        text = (
            "Values in the linked GEDCOM file have changed. There are\n"
            + ancestor_text
            + source_text
            + "Do you want to update them with values from the GEDCOM file?"
        )
        self.confirmation_dialog.setText(text)
        button = self.confirmation_dialog.exec_()
        if button == QMessageBox.Cancel:
            return

        for update in self.ancestor_updates + self.source_updates:
            # print(f"Updating {update['index']} to {update['value']}")
            self.data_context.data_model.setData(update["index"], update["value"])
