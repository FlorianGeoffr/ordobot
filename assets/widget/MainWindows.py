from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class MainWindows(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindows, self).__init__(parent)
        self.setWindowTitle("OrdoBot")
        self.setGeometry(QRect(0, 0, 350, 500))
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.setStyleSheet("QMainWindow { background-color: #2E2E2E; }")

        # Set up the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Add a label to the layout
        label = QLabel("Welcome to OrdoBot!", self)
        label.setStyleSheet("color: white; font-size: 20px;")
        layout.addWidget(label)