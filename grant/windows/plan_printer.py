""" Prints ResearchPlans """

from typing import List
from PyQt5 import QtGui
from PyQt5.QtGui import QPageLayout
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtPrintSupport import QPrintDialog
from grant.research import ResearchPlan
from grant.research import ResearchProject
from grant.research import ResearchTask


def _style_html() -> str:
    """ The style to use in the header """
    return """
        body {
            width: 21cm;
            height: 29.7cm;
            margin: 2mm;
            }
        table,
        th,
        td {
            border: 1px solid black;
            border-collapse: collapse;
        }
        th,
        td {
            padding: 15px;
            vertical-align: center;
        }
        .task-date {
            text-align: center;
        }
        .task-result {
            text-align: center;
        }
        #task-table {
            width: 100%;
            margin: 20px 0px 0px 0px;
        }
        .page-break { page-break-before: always;}
    """


def _task_html(task: ResearchTask) -> str:
    """ Generates the HTML needed to print a task """
    return f"""
            <tbody>
              <tr>
                <td class="task-date"></td>
                <td>{task.source}</td>
                <td>{task.description}</td>
                <td class="task-result">Nil</td>
              </tr>
            </tbody>
        """


def _plan_html(plan: ResearchPlan) -> str:
    """ Generates the HTML necessary to print a plan """
    return f"""
        <h1>Research Log - {plan.ancestor}</h1>
        <hr />
        <h3>Research Goals:</h3>
        To find out when he lived, his parents and any potential wife he may have
        had.
        <table id="task-table">
            <thead>
            <tr>
                <th>Date of Search</th>
                <th>Source searched<br />(author, title, year, pages)</th>
                <th>
                    Description of search<br />(purpose of search, years/names searched)
                </th>
                <th>Outcome</th>
            </tr>
            </thead>
            {''.join(_task_html(task) for task in plan.tasks)}
        </table>
        <div class="page-break"></div>
    """


def _document_html(plans: List[ResearchPlan]) -> str:
    """ Generates the wrapper html for the printer """
    return f"""
        <html>
            <head>
                <style>
                    {_style_html()}
                </style>
            </head>
        <body>
            {''.join(_plan_html(plan) for plan in plans)}
        </body>
    </html>
    """


class PlanPrinter:
    """ Allows printing of ResearchPlan objects """

    def __init__(self):
        self.printer = QPrinter(QPrinter.HighResolution)
        self.printer.setPageOrientation(QPageLayout.Landscape)
        self.dialog = QPrintDialog(self.printer)

    def print_project(self, project: ResearchProject):
        """ Prints all plans in the project """
        self.print_plans(project.plans)

    def print_plan(self, plan: ResearchPlan):
        """ Print a single plan """
        self.print_plans([plan])

    def print_plans(self, plans: List[ResearchPlan]):
        """ print a list of plans """

        if self.dialog.exec_() != QPrintDialog.Accepted:
            return

        document = QtGui.QTextDocument()
        document.setHtml(_document_html(plans))
        document.print(self.printer)
