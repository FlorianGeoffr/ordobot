from pathlib import Path


def lister_contenu(path_str: str, mode: str = "tous") -> list[Path]:
    """
    Liste le contenu d'un dossier selon le mode spécifié.

    :param path_str: Chemin du dossier
    :param mode: "fichiers", "dossiers" ou "tous"
    :return: Liste d'objets Path
    """
    path = Path(path_str).expanduser().resolve()
    if not path.exists() or not path.is_dir():
        raise ValueError(f"❌ Le chemin '{path}' est invalide ou n'est pas un dossier.")

    elements = sorted(path.iterdir(), key=lambda x: x.name.lower())

    if mode == "fichiers":
        return [e for e in elements if e.is_file()]
    elif mode == "dossiers":
        return [e for e in elements if e.is_dir()]
    elif mode == "tous":
        return elements
    else:
        raise ValueError("Mode invalide. Utilise 'fichiers', 'dossiers' ou 'tous'.")


def renommer_dossier(parent_path: str, index: int, nouveau_nom: str):
    """
    Renomme un sous-dossier à partir de son index dans la liste.

    :param parent_path: Chemin du dossier parent
    :param index: Index du dossier à renommer (dans la liste des dossiers)
    :param nouveau_nom: Nouveau nom du dossier
    """
    dossiers = lister_contenu(parent_path, mode="dossiers")
    if not (0 <= index < len(dossiers)):
        raise IndexError("Index invalide.")

    ancien = dossiers[index]
    nouveau = ancien.parent / nouveau_nom
    ancien.rename(nouveau)
    return nouveau


def supprimer_dossier(parent_path: str, index: int):
    """
    Supprime un sous-dossier vide par index.

    :param parent_path: Chemin du dossier parent
    :param index: Index du dossier à supprimer (dans la liste des dossiers)
    """
    dossiers = lister_contenu(parent_path, mode="dossiers")
    if not (0 <= index < len(dossiers)):
        raise IndexError("Index invalide.")

    cible = dossiers[index]
    cible.rmdir()  # échoue si non vide
    return cible.name


def ajouter_dossier(nom_dossier: str, parent_path: str):
    """
    Crée un nouveau dossier dans le dossier parent.

    :param nom_dossier: Nom du nouveau dossier
    :param parent_path: Chemin du dossier parent
    """
    parent = Path(parent_path).expanduser().resolve()
    if not parent.exists() or not parent.is_dir():
        raise ValueError("❌ Dossier parent invalide.")

    nouveau = parent / nom_dossier
    if nouveau.exists():
        raise FileExistsError(f"⚠️ Le dossier '{nom_dossier}' existe déjà.")

    nouveau.mkdir()
    return nouveau
