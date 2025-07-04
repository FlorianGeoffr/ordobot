import os
import shutil

from PySide6.QtCore import QAbstractItemModel, QModelIndex, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFileSystemModel

import tempfile


class DiffFileSystemModel(QFileSystemModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dict_diff = {}

    def data(self, index, role):
        chemin = self.filePath(index)
        relatif = os.path.relpath(chemin, self.rootPath())

        if role == Qt.ForegroundRole:
            etat = self.dict_diff.get(relatif)
            if etat == "ajouté":
                return QColor("green")
            if etat == "supprimé":
                return QColor("red")

        return super().data(index, role)

    def set_diff(self, diff_dict):
        """
        Met à jour le dictionnaire des différences et notifie le modèle.
        :param diff_dict: Dictionnaire des différences avec les chemins relatifs comme clés.
        """
        self.dict_diff = diff_dict
        self.layoutChanged.emit()  # Notifie le modèle que la structure a changé


def comparer_structure(dossier1, dossier2):
    diffs = {}
    noms_1 = set(os.listdir(dossier1)) if os.path.exists(dossier1) else set()
    noms_2 = set(os.listdir(dossier2)) if os.path.exists(dossier2) else set()

    for nom in sorted(noms_1 | noms_2):
        chemin1 = os.path.join(dossier1, nom)
        chemin2 = os.path.join(dossier2, nom)

        if nom in noms_1 and nom not in noms_2:
            diffs[nom] = "supprimé"
        elif nom not in noms_1 and nom in noms_2:
            diffs[nom] = "ajouté"
        else:
            if os.path.isdir(chemin1) and os.path.isdir(chemin2):
                sous_diffs = comparer_structure(chemin1, chemin2)
                for k, v in sous_diffs.items():
                    diffs[f"{nom}/{k}"] = v
            # Sinon, on considère qu'un fichier de même nom existe → pas besoin d'aller plus loin

    return diffs


def get_virtual_fs(base, actions) -> str:
    temp_folder = tempfile.mkdtemp()

    # application de la struc base dans le dossier temporaire
    def apply_structure(base, path: str):
        for name, content in base.items():
            new_path = path + "/" + name
            if isinstance(content, dict):
                os.makedirs(new_path, exist_ok=True)
                apply_structure(content, new_path)
            else:
                with open(new_path, "w") as f:
                    pass

    apply_structure(base, temp_folder)

    # application des actions
    for action in actions:
        if action.type == "rm":
            path = temp_folder + "/" + action.args[0]
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
        elif action.type == "mk":
            os.makedirs(temp_folder + "/" + action.args[0], exist_ok=True)
        elif action.type == "mv":
            src = temp_folder + "/" + action.args[0]
            dst = temp_folder + "/" + action.args[1]
            if os.path.exists(src):
                shutil.move(src, dst)
        elif action.type == "mvc":
            # copy file in src to dst (but not the folder)
            src = temp_folder + "/" + action.args[0]
            dst = temp_folder + "/" + action.args[1]
            if os.path.exists(src):
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
    return temp_folder
