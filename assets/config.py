import json
import os
from pathlib import Path
from PySide6.scripts.project_lib import Singleton


class Config(metaclass=Singleton):
    def __init__(self):
        # Dossier de base (ordobot)
        self.config_base_dir = Path(__file__).parent.parent

        # Créer le dossier spécifique selon l'OS
        if os.name == "nt":  # Windows
            self.config_dir = self.config_base_dir / "windows"
        elif os.uname().sysname == "Darwin":  # macOS
            self.config_dir = self.config_base_dir / "mac"
        else:  # Linux et autres Unix
            self.config_dir = self.config_base_dir / "linux"

        self.config_file = self.config_dir / "config.json"
        self._data = {}
        self._load_config()

    def _load_config(self):
        """Charge la configuration depuis le fichier JSON spécifique à l'OS"""
        try:
            if self.config_file.exists():
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            else:
                self._data = {}
        except (json.JSONDecodeError, FileNotFoundError):
            self._data = {}

    def _save_config(self):
        """Sauvegarde la configuration dans le fichier JSON spécifique à l'OS"""
        try:
            # Créer le dossier OS spécifique s'il n'existe pas
            self.config_dir.mkdir(exist_ok=True)
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur sauvegarde config: {e}")

    # set préférences utilisateur
    def set(self, key, value):
        """Définit une valeur de configuration dans le dossier OS spécifique"""
        self._data[key] = value
        self._save_config()

    # get préférences utilisateur
    def get(self, key, default=None):
        """Récupère une valeur de configuration depuis le dossier OS spécifique"""
        return self._data.get(key, default)

    # update les préférences utilisateur
    def update(self, key, value):
        """Met à jour une valeur de configuration dans le dossier OS spécifique"""
        if key in self._data:
            self._data[key] = value
            self._save_config()
        else:
            print(f"Clé '{key}' non trouvée dans la configuration.")

    def delete(self, key):
        """Supprime une valeur de configuration dans le dossier OS spécifique"""
        if key in self._data:
            del self._data[key]
            self._save_config()
        else:
            print(f"Clé '{key}' non trouvée dans la configuration.")

    # get infos sur l'OS et les chemins utilisés
    def get_os_info(self):
        """Retourne des informations sur l'OS et les chemins utilisés"""
        return {
            "os_name": os.name,
            "platform": os.uname().sysname if hasattr(os, "uname") else "Windows",
            "config_dir": str(self.config_dir),
            "config_file": str(self.config_file),
            "config_dir_exists": self.config_dir.exists(),
            "config_file_exists": self.config_file.exists(),
        }


# ======= Exemple utilisation =======
# Set infos
# cd /Users/denisdmu/Documents/ordobot && python3 -c "
# from assets.config import Config
# config = Config()
# print(' Saving preferences...')
# config.set('favorite_color', 'blue')
# config.set('city', 'Paris')
# config.set('language', 'English')
# config.set('theme', 'dark')
# print('Preferences saved!')
# info = config.get_os_info()
# print(f' Config saved in: {info[\"config_dir\"]}')
# "

# Get infos
# cd /Users/denisdmu/Documents/ordobot && python3 -c "
# from assets.config import Config
# config = Config()
# print(' Getting preferences...')
# print(f'Favorite color: {config.get(\"favorite_color\")}')
# print(f'City: {config.get(\"city\")}')
# print(f'Language: {config.get(\"language\")}')
# print(f'Theme: {config.get(\"theme\")}')
# print(f'Unknown key: {config.get(\"unknown_key\", \"default_value\")}')
# info = config.get_os_info()
# print(f' OS Info: {info[\"platform\"]} - Config in: {info[\"config_dir\"]}')
# "

# Update infos
# cd /Users/denisdmu/Documents/ordobot && python3 -c "
# from assets.config import Config
# config = Config()
# print(' Testing update method...')

# # D'abord vérifier les valeurs actuelles
# print('Before update:')
# print(f'  City: {config.get(\"city\")}')
# print(f'  Theme: {config.get(\"theme\")}')

# # Mettre à jour des clés existantes
# config.update('city', 'London')
# config.update('theme', 'light')

# # Essayer de mettre à jour une clé inexistante
# config.update('nonexistent_key', 'some_value')

# print('After update:')
# print(f'  City: {config.get(\"city\")}')
# print(f'  Theme: {config.get(\"theme\")}')
# print(' Update test completed!')
# "

# Delete infos
# cd /Users/denisdmu/Documents/ordobot && python3 -c "
# from assets.config import Config
# config = Config()
# print(' Testing delete method...')
# # D'abord vérifier les valeurs actuelles
# print('Before delete:')
# print(f'  City: {config.get(\"city\")}')
# print(f'  Theme: {config.get(\"theme\")}')
# # Supprimer des clés existantes
# config.delete('city')
# config.delete('theme')
# # Essayer de supprimer une clé inexistante
# config.delete('nonexistent_key')
# print('After delete:')
# print(f'  City: {config.get(\"city\")}')
# print(f'  Theme: {config.get(\"theme\")}')
# print(' Delete test completed!')
# "