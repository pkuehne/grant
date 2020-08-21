""" Tests for the PlanPrinter """

from unittest import mock
from PyQt5 import QtGui
from PyQt5.QtPrintSupport import QPrintDialog
from grant.windows.plan_printer import PlanPrinter
from grant.windows.plan_printer import _document_html
from grant import research


def test_default_page_setup():
    """ Check that the page is set up correctly when first created """
    # Given
    printer = PlanPrinter()

    # Then
    assert printer.printer.pageLayout().orientation() == QtGui.QPageLayout.Landscape


def test_document_html_includes_html_tags():
    """ The generated html for the document should include html tags """
    # Given

    # When
    html = _document_html([])

    # Then
    assert "<html>" in html
    assert "</html>" in html


def test_document_html_includes_each_ancestor():
    """ Each ancestor should have their name includes """
    # Given
    plan1 = research.ResearchPlan()
    plan1.ancestor = "Bob"
    plan2 = research.ResearchPlan()
    plan2.ancestor = "Dave"

    # When
    html = _document_html([plan1, plan2])

    # Then
    assert plan1.ancestor in html
    assert plan2.ancestor in html


def test_document_html_includes_each_task():
    """ Each ancestor should have their name includes """
    # Given
    plan1 = research.ResearchPlan()
    task1 = research.ResearchTask()
    task1.source = "Grantham"
    plan1.tasks.append(task1)
    plan2 = research.ResearchPlan()
    task2 = research.ResearchTask()
    task2.source = "Downton"
    plan2.tasks.append(task2)

    # When
    html = _document_html([plan1, plan2])

    # Then
    assert task1.source in html
    assert task2.source in html


def test_document_requires_setup_printer(monkeypatch):
    """ The document should be set to the pronter """
    # Given
    printer = PlanPrinter()
    document = mock.MagicMock()
    monkeypatch.setattr(printer.dialog, "exec_", lambda: QPrintDialog.Rejected)
    monkeypatch.setattr(QtGui, "QTextDocument", lambda: document)

    plan = research.ResearchPlan()
    plan.ancestor = "Bob"

    # When
    printer.print_plan(plan)

    # Then
    assert not document.setHtml.called


def test_document_is_sent_to_printer(monkeypatch):
    """ The document should be set to the pronter """
    # Given
    printer = PlanPrinter()
    document = mock.MagicMock()
    monkeypatch.setattr(printer.dialog, "exec_", lambda: QPrintDialog.Accepted)
    monkeypatch.setattr(QtGui, "QTextDocument", lambda: document)

    plan = research.ResearchPlan()
    plan.ancestor = "Bob"

    # When
    printer.print_plan(plan)

    # Then
    assert document.setHtml.called


def test_printing_project_includes_all_plans(monkeypatch):
    """ The document should be set to the pronter """
    # Given
    printer = PlanPrinter()
    document = mock.MagicMock()
    monkeypatch.setattr(printer.dialog, "exec_", lambda: QPrintDialog.Accepted)
    monkeypatch.setattr(QtGui, "QTextDocument", lambda: document)

    project = research.ResearchProject("")
    plan1 = research.ResearchPlan()
    plan1.ancestor = "Bob"
    plan2 = research.ResearchPlan()
    plan2.ancestor = "Dave"
    project.plans.append(plan1)
    project.plans.append(plan2)

    # When
    printer.print_project(project)

    # Then
    assert document.setHtml.called
    html = document.setHtml.call_args[0][0]
    assert plan1.ancestor in html
    assert plan2.ancestor in html
