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
from assets.config import Config
from assets.theme import theme_manager


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

        # Initialiser config et appliquer le thème sauvegardé
        self.config = Config()
        theme_manager.apply_theme()

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

        # Création des menus
        self.create_menus()

    def create_menus(self):
        """Crée tous les menus de l'application"""
        menu = self.menuBar()

        # Menu Visualisation
        self.create_visualisation_menu(menu)

        # Menu Configuration (regroupe IA, Thème, Langue)
        self.create_configuration_menu(menu)

    def create_visualisation_menu(self, menu):
        """Crée le menu Visualisation"""
        visualisation_menu = menu.addMenu("Visualisation")

        action_expand_all = QAction("Développer tout", self)
        action_expand_all.triggered.connect(self.tree_file.expandAll)
        visualisation_menu.addAction(action_expand_all)

        action_collapse_all = QAction("Réduire tout", self)
        action_collapse_all.triggered.connect(self.tree_file.collapseAll)
        visualisation_menu.addAction(action_collapse_all)

        visualisation_menu.addSeparator()

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
        visualisation_menu.addAction(action_show_files)

    def create_configuration_menu(self, menu):
        """Crée le menu Configuration avec ses sous-menus"""
        config_menu = menu.addMenu("Configuration")

        # Sous-menu IA
        ia_submenu = config_menu.addMenu("IA")

        # Action pour ouvrir ConfigDialog
        action_config_ia = QAction("Sélectionner modèle et clé API...", self)
        action_config_ia.triggered.connect(self.open_ia_config)
        ia_submenu.addAction(action_config_ia)

        ia_submenu.addSeparator()

        # Affichage du modèle actuel
        current_model = self.config.get("ai_model", "Non configuré")
        action_current_model = QAction(f"Modèle actuel: {current_model}", self)
        action_current_model.setEnabled(False)
        ia_submenu.addAction(action_current_model)
        self.action_current_model = action_current_model

        # Sous-menu Thème
        theme_submenu = config_menu.addMenu("Thème")

        themes = [("dark", "Sombre"), ("light", "Clair")]
        current_theme = theme_manager.get_current_theme()

        self.theme_actions = {}
        for theme_key, theme_label in themes:
            action = QAction(theme_label, self)
            action.setCheckable(True)
            action.setChecked(theme_key == current_theme)
            action.triggered.connect(lambda checked, t=theme_key: self.set_theme(t))
            theme_submenu.addAction(action)
            self.theme_actions[theme_key] = action

        # Sous-menu Langue
        language_submenu = config_menu.addMenu("Langue")

        languages = ["French", "English", "Spanish"]
        current_language = self.config.get("language", "French")

        self.language_actions = {}
        for language in languages:
            action = QAction(language, self)
            action.setCheckable(True)
            action.setChecked(language == current_language)
            action.triggered.connect(lambda checked, l=language: self.set_language(l))
            language_submenu.addAction(action)
            self.language_actions[language] = action

        # Ajouter l'action CGU
        action_cgu = QAction("CGU", self)
        action_cgu.triggered.connect(self.open_cgu_dialog)
        config_menu.addAction(action_cgu)

    def set_theme(self, theme):
        """Change le thème et met à jour les menus"""
        theme_manager.set_theme(theme)
        print(f"Thème changé vers: {theme}")

        # Mettre à jour les coches
        for theme_key, action in self.theme_actions.items():
            action.setChecked(theme_key == theme)

    def set_language(self, language):
        """Change la langue et met à jour les menus"""
        self.config.set("language", language)
        print(f"Langue changée vers: {language}")

        # Mettre à jour les coches
        for lang_key, action in self.language_actions.items():
            action.setChecked(lang_key == language)

    def open_ia_config(self):
        """Ouvre la configuration IA"""
        dial = ConfigDialog(self)
        if dial.exec() == QDialog.Accepted:
            print("Configuration IA sauvegardée")
            # Mettre à jour l'affichage du modèle actuel
            current_model = self.config.get("ai_model", "Non configuré")
            self.action_current_model.setText(f"Modèle actuel: {current_model}")
        else:
            print("Configuration IA annulée")

    def select_folder(self):
        """Sélectionne un dossier"""
        folder = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier")
        if folder:
            print(f"Dossier sélectionné: {folder}")
            self.model.setRootPath(folder)
            self.tree_file.setRootIndex(self.model.index(folder))
        else:
            print("Aucun dossier sélectionné")

    def open_option_dialog(self):
        """Méthode de compatibilité - redirige vers config IA"""
        dial = ConfigDialog()
        if dial.exec() == QDialog.Accepted:
            print("Configuration saved")
        else:
            print("Configuration cancelled")

    def open_cgu_dialog(self):
        cgu_dialog = CGUDialog(self)
        cgu_dialog.exec()

    def generate_tree(self):
        """Génère l'arborescence avec l'IA"""
        try:
            # Vérifier si la configuration IA est prête
            api_key = self.config.get("chatgpt_api_key", "")
            if not api_key:
                QMessageBox.warning(
                    self,
                    "Configuration manquante",
                    "Veuillez configurer votre clé API dans Configuration > IA > Sélectionner modèle et clé API...",
                )
                return

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

        except ValueError as e:
            # Erreur de configuration IA
            QMessageBox.critical(
                self,
                "Erreur de configuration",
                f"Erreur IA: {str(e)}\n\nVeuillez configurer votre clé API dans Configuration > IA.",
            )
        except Exception as e:
            # Autres erreurs
            QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite: {str(e)}")
