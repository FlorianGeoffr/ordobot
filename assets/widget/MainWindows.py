from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class MainWindows(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindows, self).__init__(parent)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        button_select_folder = QPushButton("Choisir le dossier cible", self)
        button_select_folder.clicked.connect(self.select_folder)

        text_erea_prompt = QTextEdit(self)
        text_erea_prompt.setPlaceholderText("Entrez votre prompt ici...")
        text_erea_prompt.setMinimumHeight(100)

        layout.addWidget(button_select_folder)
        layout.addWidget(text_erea_prompt)
        self.setWindowTitle("OrdoBot")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            print(f"Selected folder: {folder}")
            # Here you can add code to handle the selected folder
        else:
            print("No folder selected")