"""
Main file
"""
import sys
import yaml
from PyQt5.QtWidgets import QApplication
from gene.windows import MainWindow
from gene.research import ResearchProject

YAML_DATA = """
---
version: 1.0
project: 
    title: My test research project
    gedcom: none
    plans: 
        - title: A research Plan
          goal: To represent a research plan fully
          tasks: 
            - title: Task 1
              status: active
            - title: Task 2
              status: active
"""


def main(argv):
    """ The main """
    app = QApplication(argv)
    app.setStyle("Fusion")

    loaded = yaml.safe_load(YAML_DATA)
    project = ResearchProject()
    project.from_py(loaded["project"])

    window = MainWindow()

    # Show window and run
    window.show()
    app.exec_()


if __name__ == "__main__":
    main(sys.argv)
