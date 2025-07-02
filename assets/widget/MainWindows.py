from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QTreeView,
    QFileSystemModel,
    QAction,
    QFileDialog,
    QDialog,
)
from PySide6.QtCore import QDir

from assets.widget.ConfigDialog import ConfigDialog


class MainWindows(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindows, self).__init__(parent)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        layout_left = QVBoxLayout()
        layout.addLayout(layout_left)
        layout_right = QVBoxLayout()
        layout.addLayout(layout_right)

        button_select_folder = QPushButton("Choisir le dossier cible", self)
        button_select_folder.clicked.connect(self.select_folder)

        text_erea_prompt = QTextEdit(self)
        text_erea_prompt.setPlaceholderText("Entrez votre prompt ici...")
        text_erea_prompt.setMinimumHeight(100)

        layout_left.addWidget(button_select_folder)
        layout_left.addWidget(text_erea_prompt)

        button_generate = QPushButton("Générer l'arborescence", self)
        button_generate.setEnabled(False)
        layout_left.addWidget(button_generate)
        layout_left.addStretch()

        button_apply_to_system = QPushButton("Appliquer au système", self)
        button_apply_to_system.setEnabled(False)
        layout_left.addWidget(button_apply_to_system)

        self.tree_file = QTreeView(self)
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.tree_file.setModel(self.model)
        self.tree_file.setRootIndex(self.model.index(QDir.rootPath()))
        self.setWindowTitle("OrdoBot")

        layout_right.addWidget(self.tree_file)

        menu = self.menuBar()
        visualisation_menu = menu.addMenu("Visualisation")
        action_expand_all = QAction("Développer tout", self)
        action_expand_all.triggered.connect(self.tree_file.expandAll)
        visualisation_menu.addAction(action_expand_all)
        action_collapse_all = QAction("Réduire tout", self)
        action_collapse_all.triggered.connect(self.tree_file.collapseAll)
        visualisation_menu.addAction(action_collapse_all)
        # select show file
        action_show_files = QAction("Afficher les fichiers", self)
        action_show_files.setCheckable(True)
        action_show_files.setChecked(True)
        action_show_files.triggered.connect(
            lambda: self.model.setFilter(
                QDir.NoDotAndDotDot | QDir.Files | QDir.Dirs
                if action_show_files.isChecked()
                else QDir.NoDotAndDotDot | QDir.Dirs
            )
        )

        option_menu = menu.addMenu("Options")
        selection_model = QAction("Selection du modèle d'ia", self)
        selection_model.triggered.connect(self.open_option_dialog)
        option_menu.addAction(selection_model)

        visualisation_menu.addAction(action_show_files)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            print(f"Selected folder: {folder}")
            self.model.setRootPath(folder)
            self.tree_file.setRootIndex(self.model.index(folder))
        else:
            print("No folder selected")

    def open_option_dialog(self):
        dial = ConfigDialog()
        if dial.exec() == QDialog.Accepted:
            print("Configuration saved")
        else:
            print("Configuration cancelled")
