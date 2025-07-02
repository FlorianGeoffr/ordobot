from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import os
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("OrdoBot")
    app.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "assets", "icon.png")))
    app.setStyle("Fusion")

    main_window = QMainWindow()
    main_window.show()

    sys.exit(app.exec())