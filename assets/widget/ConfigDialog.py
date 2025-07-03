from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QLabel,
    QLineEdit,
    QPushButton,
)

from assets.config import Config


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)

        # Utiliser Class Config pour gérer les préférences
        self.config = Config()

        # Liste des modèles disponibles
        self.list_models = [
            "gpt-4.1-mini",
            "gpt-4.1",
            "gpt-4o-mini",
            "gpt-4o",
        ]

        self.setWindowTitle("Configuration IA")
        self.setFixedSize(450, 280)
        layout = QVBoxLayout(self)

        # ComboBox pour les modèles
        self.combo_models = QComboBox(self)
        self.combo_models.addItems(self.list_models)

        # Récupérer le modèle actuel depuis Config
        current_model = self.config.get("ai_model", "gpt-3.5-turbo")
        if current_model in self.list_models:
            self.combo_models.setCurrentText(current_model)

        self.combo_models.currentTextChanged.connect(self.update_description)
        layout.addWidget(QLabel("Sélectionnez le modèle IA :"))
        layout.addWidget(self.combo_models)

        # Description du modèle
        self.description_model = QLineEdit(self)
        self.description_model.setReadOnly(True)
        self.update_description()
        layout.addWidget(QLabel("Description du modèle :"))
        layout.addWidget(self.description_model)

        # Clé API avec bouton d'affichage
        layout.addWidget(QLabel("Clé API :"))
        api_layout = QHBoxLayout()

        self.text_api = QLineEdit(self)
        self.text_api.setPlaceholderText("Clé API")
        # Utiliser chatgpt_api_key comme dans IAIntegration
        self.text_api.setText(self.config.get("chatgpt_api_key", ""))
        self.text_api.setEchoMode(QLineEdit.Password)

        # Bouton pour afficher/masquer la clé
        self.button_show_api = QPushButton("👁️", self)
        self.button_show_api.clicked.connect(self.toggle_api_visibility)
        self.button_show_api.setFixedWidth(40)

        # Bouton pour tester la clé API
        self.button_test_api = QPushButton("Tester", self)
        self.button_test_api.clicked.connect(self.test_api)
        self.button_test_api.setFixedWidth(60)

        api_layout.addWidget(self.text_api)
        api_layout.addWidget(self.button_show_api)
        api_layout.addWidget(self.button_test_api)
        layout.addLayout(api_layout)

        # Label pour le statut du test
        self.label_status = QLabel("")
        layout.addWidget(self.label_status)

        # Boutons de contrôle
        buttons_layout = QHBoxLayout()

        button_save = QPushButton("Enregistrer", self)
        button_save.clicked.connect(self.save_config)
        buttons_layout.addWidget(button_save)

        button_cancel = QPushButton("Annuler", self)
        button_cancel.clicked.connect(self.reject)
        buttons_layout.addWidget(button_cancel)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def toggle_api_visibility(self):
        """Affiche/masque la clé API"""
        if self.text_api.echoMode() == QLineEdit.Password:
            self.text_api.setEchoMode(QLineEdit.Normal)
            self.button_show_api.setText("🙈")
        else:
            self.text_api.setEchoMode(QLineEdit.Password)
            self.button_show_api.setText("👁️")

    def test_api(self):
        """Test simple de la clé API"""
        api_key = self.text_api.text().strip()
        if not api_key:
            self.label_status.setText("Veuillez entrer une clé API")
            self.label_status.setStyleSheet("color: orange;")
            return

        # Test basique (vérification du format)
        if len(api_key) > 20 and api_key.startswith(("sk-", "xai-")):
            self.label_status.setText("Format de clé API valide")
            self.label_status.setStyleSheet("color: green;")
        else:
            self.label_status.setText("Format de clé API invalide")
            self.label_status.setStyleSheet("color: red;")

    def get_description_model(self, model):
        """Retourne la description d'un modèle"""
        descriptions = {
            "gpt-4.1 nano": "Modèle léger et rapide, idéal pour les tâches simples.",
            "gpt-4.1 turbo": "Modèle performant pour des réponses rapides et précises.",
            "gpt-4 mini": "Modèle compact avec une bonne balance entre performance et coût.",
        }
        return descriptions.get(model, "Description non disponible")

    def update_description(self):
        """Met à jour la description du modèle sélectionné"""
        model = self.combo_models.currentText()
        description = self.get_description_model(model)
        self.description_model.setText(description)

    def save_config(self):
        """Sauvegarde la configuration IA"""
        try:
            # Sauvegarder les paramètres IA
            self.config.set("ai_model", self.combo_models.currentText())
            # Utiliser chatgpt_api_key comme dans IAIntegration
            self.config.set("chatgpt_api_key", self.text_api.text().strip())

            # Ajouter des métadonnées
            from datetime import datetime

            self.config.set("last_config_update", datetime.now().isoformat())

            print("Configuration IA sauvegardée avec succès")
            print(f"Modèle: {self.combo_models.currentText()}")
            print(
                f"Clé API: {'Configurée' if self.text_api.text().strip() else 'Non configurée'}"
            )

            # Afficher le chemin de sauvegarde
            info = self.config.get_os_info()
            print(f"Sauvé dans: {info['config_file']}")

            self.accept()

        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            self.label_status.setText(f"Erreur: {e}")
            self.label_status.setStyleSheet("color: red;")
