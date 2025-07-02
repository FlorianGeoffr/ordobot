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
        self.list_models = ModelIA.list_models()
        self.setWindowTitle("Configuration des Modèles IA")
        self.setFixedSize(400, 200)
        layout = QVBoxLayout(self)
        self.combo_models = QComboBox(self)
        self.combo_models.addItems(self.list_models)
        self.combo_models.setCurrentText(ModelIA.get_model_name())
        self.combo_models.currentTextChanged.connect(self.update_description)
        layout.addWidget(QLabel("Sélectionnez le modèle IA :"))
        layout.addWidget(self.combo_models)
        self.description_model = QLineEdit(self)
        self.description_model.setReadOnly(True)
        self.update_description()
        layout.addWidget(QLabel("Description du modèle :"))
        layout.addWidget(self.description_model)

        button_save = QPushButton("Enregistrer", self)
        button_save.clicked.connect(self.save_config)
        layout.addWidget(button_save)
        self.setLayout(layout)

    def update_description(self):
        model = self.combo_models.currentText()
        description = ModelIA.get_description_model(model)
        self.description_model.setText(description)

    def save_config(self):
        model = self.combo_models.currentText()
        ModelIA.set_model(model)
        self.accept()
