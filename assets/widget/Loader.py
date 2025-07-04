from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *


class Loader(QDialog):
    def __init__(self, parent=None):
        super(Loader, self).__init__(parent)
        self.setWindowTitle("Chargement")
        self.setFixedSize(300, 100)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        layout = QVBoxLayout(self)
        self.label = QLabel("Chargement en cours...", self)
        layout.addWidget(self.label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)  # Indeterminate mode
        layout.addWidget(self.progress_bar)

        self.setStyleSheet("background-color: #f0f0f0; color: #333;")
        self.setModal(True)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.show()

    def update_message(self, message: str):
        """
        Update the loading message displayed in the dialog.
        :param message: The new message to display.
        """
        self.label.setText(message)
        self.label.adjustSize()

    def close_dialog(self):
        """
        Close the loading dialog.
        This method can be called to close the dialog when loading is complete.
        :return:
        """
        self.close()
        self.deleteLater()

    def closeEvent(self, event):
        pass
