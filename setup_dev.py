#!/usr/bin/env python3
"""
Script de configuration de l'environnement de développement pour OrdoBot
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description, check=True):
    """Exécute une commande et affiche le résultat"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, shell=True, check=check, capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"✅ {description} - OK")
            return True
        else:
            print(f"❌ {description} - Erreur: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erreur: {e}")
        return False


def setup_git_config():
    """Configure Git pour le projet"""
    print("\n📝 Configuration Git...")

    commands = [
        ("git config pull.rebase true", "Configuration pull.rebase"),
        ("git config rebase.autoStash true", "Configuration rebase.autoStash"),
        ("git config merge.ff only", "Configuration merge.ff"),
        (
            "git config branch.autosetupmerge always",
            "Configuration branch.autosetupmerge",
        ),
        (
            "git config branch.autosetuprebase always",
            "Configuration branch.autosetuprebase",
        ),
        ("git config rerere.enabled true", "Configuration rerere.enabled"),
        ("git config alias.st status", "Alias git st"),
        ("git config alias.co checkout", "Alias git co"),
        ("git config alias.br branch", "Alias git br"),
        ("git config alias.ci commit", "Alias git ci"),
        ("git config alias.cam 'commit -am'", "Alias git cam"),
        (
            "git config alias.lg 'log --oneline --graph --decorate --all'",
            "Alias git lg",
        ),
        ("git config alias.unstage 'reset HEAD --'", "Alias git unstage"),
    ]

    for command, description in commands:
        run_command(command, description, check=False)


def setup_pre_commit_hook():
    """Configure le hook pre-commit"""
    print("\n🪝 Configuration du hook pre-commit...")

    hooks_dir = Path(".git/hooks")
    hooks_dir.mkdir(exist_ok=True)

    pre_commit_content = """#!/bin/sh
# Pre-commit hook pour formatter et vérifier le code avant commit

echo "Running pre-commit checks..."

# Format code with black
echo "Formatting code with Black..."
python -m black . --line-length=88

# Add formatted files to staging
git add .

# Check with flake8
echo "Linting with flake8..."
python -m flake8 . --max-line-length=88 --extend-ignore=E203,W503

if [ $? -ne 0 ]; then
    echo "❌ Linting issues found. Please fix them before committing."
    exit 1
fi

echo "✅ All checks passed!"
exit 0
"""

    pre_commit_path = hooks_dir / "pre-commit"
    with open(pre_commit_path, "w", encoding="utf-8") as f:
        f.write(pre_commit_content)

    # Rendre le hook exécutable (Windows)
    if os.name != "nt":
        os.chmod(pre_commit_path, 0o755)

    print("✅ Hook pre-commit configuré")


def install_dependencies():
    """Installe les dépendances de développement"""
    print("\n📦 Installation des dépendances...")

    # Dépendances principales
    run_command("pip install -r requirements.txt", "Installation requirements.txt")

    # Dépendances de développement
    dev_packages = [
        "black>=23.0.0",
        "flake8>=6.0.0",
        "isort>=5.0.0",
    ]

    for package in dev_packages:
        run_command(f"pip install {package}", f"Installation {package}")


def main():
    """Fonction principale"""
    print("🚀 Configuration de l'environnement de développement OrdoBot\n")

    # Vérifier qu'on est dans le bon répertoire
    if not Path("main.py").exists():
        print(
            "❌ Erreur: Ce script doit être exécuté depuis le répertoire du "
            "projet OrdoBot"
        )
        sys.exit(1)

    # Configuration étape par étape
    install_dependencies()
    setup_git_config()
    setup_pre_commit_hook()

    print("\n✅ Configuration terminée!")
    print("\n📋 Commandes utiles:")
    print("  git st          # Status")
    print("  git co <branch> # Checkout")
    print("  git cam 'msg'   # Commit avec message")
    print("  git lg          # Log graphique")
    print("\n🎯 Le hook pre-commit formatera automatiquement votre code!")


if __name__ == "__main__":
    main()
    print("\n🎯 Le hook pre-commit formatera automatiquement votre code!")


if __name__ == "__main__":
    main()
