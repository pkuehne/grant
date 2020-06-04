"""
Main file
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from grant.windows import MainWindow
import resources  # pylint: disable=unused-import


def main(argv):
    """ The main """
    app = QApplication(argv)
    app.setStyle("Fusion")
    QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton)

    window = MainWindow()

    window.show()
    app.exec_()


if __name__ == "__main__":
    main(sys.argv)
