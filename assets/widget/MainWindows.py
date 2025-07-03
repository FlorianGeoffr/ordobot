import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QTreeView,
    QFileSystemModel,
    QFileDialog,
    QDialog,
    QMessageBox,
    QTextBrowser,
)
from PySide6.QtCore import QDir
from PySide6.QtGui import QAction

from assets.FSUtils import get_dossier_struct
from assets.IAIntegration import IAIntegration
from assets.widget.ConfigDialog import ConfigDialog


class CGUDialog(QDialog):
    def __init__(self, parent=None):
        super(CGUDialog, self).__init__(parent)
        self.setWindowTitle("Conditions Générales d'Utilisation")
        self.setFixedSize(600, 400)
        layout = QVBoxLayout(self)
        text_browser = QTextBrowser(self)
        text_browser.setPlainText(
            "Conditions Générales d’Utilisation (CGU) – OrdoBot\n\n"
            "Objet\n"
            "OrdoBot est une application gratuite d’organisation automatique de dossiers et fichiers, "
            "basée sur l’intelligence artificielle.\n\n"
            "Usage autorisé\n"
            "L’application peut être utilisée librement par les particuliers et les professionnels, "
            "à condition que l’usage ne soit ni commercial, ni lucratif (pas de revente, de service "
            "payant basé sur OrdoBot, etc.).\n\n"
            "Propriété\n"
            "Le logiciel, son nom et son interface sont la propriété de ses créateurs. Toute reproduction "
            "ou modification sans accord est interdite.\n\n"
            "Responsabilité\n"
            'OrdoBot est fourni "en l’état", sans garantie. L’équipe ne peut être tenue responsable des '
            "pertes de données ou d’un usage inapproprié.\n\n"
            "Données personnelles\n"
            "OrdoBot fonctionne localement. Aucune donnée personnelle n’est collectée ou transmise.\n\n"
            "Loi applicable\n"
            "Les CGU sont régies par le droit français. En cas de litige, le tribunal compétent sera "
            "celui de Bourges."
        )
        layout.addWidget(text_browser)
        self.setLayout(layout)


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

        self.text_erea_prompt = QTextEdit(self)
        self.text_erea_prompt.setPlaceholderText("Entrez votre prompt ici...")
        self.text_erea_prompt.setMinimumHeight(100)

        layout_left.addWidget(button_select_folder)
        layout_left.addWidget(self.text_erea_prompt)

        button_generate = QPushButton("Générer l'arborescence", self)
        button_generate.setEnabled(True)
        button_generate.clicked.connect(self.generate_tree)
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

        action_cgu = QAction("CGU", self)
        action_cgu.triggered.connect(self.open_cgu_dialog)
        option_menu.addAction(action_cgu)

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

    def open_cgu_dialog(self):
        cgu_dialog = CGUDialog(self)
        cgu_dialog.exec()

    def generate_tree(self):
        actions, resume = IAIntegration().get_audit(
            self.text_erea_prompt.toPlainText(),
            get_dossier_struct(self.model.rootPath()),
        )
        for action in actions:
            print("Action:", action)
        messagesBox = QMessageBox()
        messagesBox.setWindowTitle("Résumé de l'audit")
        messagesBox.setText(resume)
        messagesBox.setInformativeText("Voulez-vous appliquer ces changements ?")
        messagesBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        messagesBox.setDefaultButton(QMessageBox.No)

        messagesBox.exec()
