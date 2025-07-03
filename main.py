import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from assets.widget.MainWindows import MainWindows

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("OrdoBot")
    app.setWindowIcon(
        QIcon(os.path.join(os.path.dirname(__file__), "assets", "icon.png"))
    )
    app.setStyle("Fusion")

    main_window = MainWindows()
    main_window.show()

    sys.exit(app.exec())
