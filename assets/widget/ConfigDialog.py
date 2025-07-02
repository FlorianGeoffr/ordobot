from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QComboBox,
    QLabel,
    QLineEdit,
    QPushButton,
)

from assets.modelIA import ModelIA


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)
        self.list_modeles = ModelIA.list_models()
        self.setWindowTitle("Configuration des Modèles IA")
        self.setFixedSize(400, 200)
        layout = QVBoxLayout(self)
        self.combo_modeles = QComboBox(self)
        self.combo_modeles.addItems(self.list_modeles)
        self.combo_modeles.setCurrentText(ModelIA.get_model_name())
        self.combo_modeles.currentTextChanged.connect(self.update_description)
        layout.addWidget(QLabel("Sélectionnez le modèle IA :"))
        layout.addWidget(self.combo_modeles)
        self.description_modele = QLineEdit(self)
        self.description_modele.setReadOnly(True)
        self.update_description()
        layout.addWidget(QLabel("Description du modèle :"))
        layout.addWidget(self.description_modele)

        button_save = QPushButton("Enregistrer", self)
        button_save.clicked.connect(self.save_config)
        layout.addWidget(button_save)
        self.setLayout(layout)

    def update_description(self):
        modele = self.combo_modeles.currentText()
        description = ModelIA.get_description_model(modele)
        self.description_modele.setText(description)

    def save_config(self):
        modele = self.combo_modeles.currentText()
        ModelIA.set_model(modele)
        self.accept()
