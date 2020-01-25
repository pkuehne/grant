""" Contains the MainWindow implementation """

from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout


class MainWindow(QMainWindow):
    """ The Main Window where we start """

    def __init__(self):
        super().__init__()

        self.root = QWidget(self)
        self.setCentralWidget(self.root)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("title"))
        layout.addWidget(QLabel("goal"))

        self.setWindowTitle("Gene - Genealogical Research Assistant")
        self.root.setLayout(layout)
