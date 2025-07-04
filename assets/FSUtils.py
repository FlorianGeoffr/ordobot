import os


def get_dossier_struct(path: str, base_path=None) -> dict:
    if base_path is None:
        base_path = path  # Garde la racine d'origine

    dossier = {}

    try:
        for entry in os.scandir(path):

            if entry.is_dir(follow_symlinks=False):
                dossier[entry.name] = get_dossier_struct(entry.path, base_path)
            else:
                dossier[entry.name] = None  # Ou résumé si besoin
    except PermissionError:
        pass  # Sécurité en cas d'accès refusé

    return dossier
