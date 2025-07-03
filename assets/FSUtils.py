from assets.IAIntegration import FSAction
import os
EXCLUSIONS = [
    # Versionnage
    ".git",
    ".git/objects",
    ".git/lfs",
    ".git/modules",
    ".git/logs",
    ".git/refs",
    ".git/info",
    ".git/hooks",
    ".svn",
    ".hg",
    ".bzr",

    # Node.js / Frontend
    "node_modules",
    "bower_components",
    "jspm_packages",
    "dist",
    "build",
    "public/build",
    ".next",
    ".nuxt",
    ".parcel-cache",
    "webpack-cache",
    ".yarn/cache",
    ".yarn/unplugged",
    "out",
    "tmp",
    "temp",
    ".turbo",

    # Python
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".mypy_cache",
    ".pytest_cache",
    ".tox",
    "pip-wheel-metadata",
    ".ipynb_checkpoints",

    # Java / JVM
    "target",
    "bin",
    "obj",
    ".gradle",
    ".idea/libraries",
    "build/classes",
    "build/reports",

    # C / C++ / Rust
    "out",
    "build",
    "target",
    ".ccls-cache",
    "Cargo.lock",

    # IDE & Configs
    ".idea",
    ".vscode",
    ".history",
    ".settings",
    ".metadata",
    "workspace-storage",

    # Docker / Container
    "docker_tmp",
    ".docker",
    "release",
    "release/app",

    # CI/CD et logs
    "coverage",
    ".coverage",
    "htmlcov",
    "logs",
    "reports",
    "artifacts",
    ".nyc_output",

    # Systèmes & OS
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini",
    "__MACOSX",
    ".Trash",
    "lost+found",
    ".fseventsd",
    ".Spotlight-V100",
    ".TemporaryItems",
    ".DocumentRevisions-V100",
    ".AppleDouble",
    ".AppleDB",
    ".AppleDesktop",

    # Médias et Cloud volumineux
    "Photos Library.photoslibrary",
    "iPhoto Library",
    "Camera Roll",
    "Saved Pictures",
    "Music",
    "Videos",
    "Movies",
    "Downloads",
    "iCloud Drive",
    "Google Drive",
    "OneDrive",
    "Dropbox",
    "Nextcloud",

    # Archives temporaires
    "__MACOSX",
    ".unison",

    # Cache divers
    "cache",
    ".cache",
    ".npm",
    ".npm-cache",
    ".eslintcache",
    ".jest-cache",
    ".pnp",
    ".pnp.js",
    ".caches",

    # Machine Learning / Data
    "checkpoints",
    "runs",
    "wandb",
    "data",
    "datasets",
    "models",
    "weights",
    ".dvc",

    # Tests / Debug
    ".pytest_cache",
    "test-output",
    "tests/logs",

    # Packages lourds compressés
    "*.zip",
    "*.tar",
    "*.tar.gz",
    "*.tgz",
    "*.rar",
    "*.7z",

    # Backup et fichiers temporaires
    "*.bak",
    "*.tmp",
    "*.swp",
    "*.swo",
    "*~",

    # Cache Windows spécifique
    "System Volume Information",
    "$RECYCLE.BIN",

    # Mac TimeMachine
    ".MobileBackups",

    # Virtualisation & Emulation
    "VirtualBox VMs",
    "*.vmdk",
    "*.vdi",
    "*.iso",
    "*.qcow2",

    # Divers gros exports
    "screenshots",
    "exports",
    "captures",
    "recordings",
]


def est_exclu(rel_path):
    for exclu in EXCLUSIONS:
        if rel_path == exclu or rel_path.startswith(exclu + os.sep):
            return True
    return False


def get_dossier_struct(path: str, base_path=None) -> dict:
    if base_path is None:
        base_path = path  # Garde la racine d'origine

    dossier = {}

    try:
        for entry in os.scandir(path):
            rel_path = os.path.relpath(entry.path, base_path)

            if est_exclu(os.path.basename(rel_path)):
                # On inscrit le dossier, mais on ne rentre pas dedans
                if entry.is_dir(follow_symlinks=False):
                    dossier[entry.name] = "[contenu exclu]"
                continue

            if entry.is_dir(follow_symlinks=False):
                dossier[entry.name] = get_dossier_struct(entry.path, base_path)
            else:
                dossier[entry.name] = None  # Ou résumé si besoin
    except PermissionError:
        pass  # Sécurité en cas d'accès refusé

    return dossier
