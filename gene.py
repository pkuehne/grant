"""
Main file
"""
import sys
from PyQt5.QtWidgets import QApplication
from grant.windows import MainWindow
import resources  # pylint: disable=unused-import


def main(argv):
    """ The main """
    app = QApplication(argv)
    app.setStyle("Fusion")

    window = MainWindow()

    window.show()
    app.exec_()


if __name__ == "__main__":
    main(sys.argv)
