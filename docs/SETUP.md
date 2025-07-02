# Guide d'utilisation complet - OrdoBot

## 🚀 Configuration initiale (à faire une seule fois)

### Étape 1 : Configuration automatique
Ouvrez PowerShell dans le dossier du projet et exécutez :

```batch
.\setup_git.bat
```

**Ce script va :**
- ✅ Configurer tous les alias Git (`git st`, `git co`, etc.)
- ✅ Activer le rebase automatique
- ✅ Formater votre code avec Black
- ✅ Vous permettre de faire des commits propres

### Étape 2 : Installation des dépendances
```bash
pip install -r requirements.txt
```

### Étape 3 : Vérification
Testez que tout fonctionne :
```bash
git st              # Devrait afficher le status
python main.py      # Devrait lancer l'application
```

## � Utilisation quotidienne

### Workflow de développement

1. **Créer une nouvelle branche** :
   ```bash
   git co -b feat/ma-nouvelle-fonctionnalite
   ```

2. **Développer votre code** :
   - Modifiez les fichiers dans VS Code
   - Le formatage se fait automatiquement à la sauvegarde
   - Testez avec `python main.py`

3. **Commiter vos changements** :
   ```bash
   git cam "feat(ui): ajout du bouton de génération"
   ```
   ℹ️ Le hook pre-commit formatera automatiquement votre code !

4. **Mettre à jour depuis develop** :
   ```bash
   git pull origin develop
   ```
   ℹ️ Le rebase se fait automatiquement !

5. **Push vers GitHub** :
   ```bash
   git push origin feat/ma-nouvelle-fonctionnalite
   ```

### Commandes Git utiles configurées

| Commande | Équivalent | Description |
|----------|------------|-------------|
| `git st` | `git status` | Voir l'état des fichiers |
| `git co <branch>` | `git checkout <branch>` | Changer de branche |
| `git br` | `git branch` | Lister les branches |
| `git ci` | `git commit` | Commit simple |
| `git cam "msg"` | `git commit -am "msg"` | Commit avec message |
| `git lg` | `git log --graph` | Log graphique |
| `git unstage` | `git reset HEAD --` | Désindexer des fichiers |

## 🛠️ Utilisation avec VS Code

### Tâches configurées
Appuyez sur **Ctrl+Shift+P** puis tapez "Tasks: Run Task" :

- **"Run OrdoBot"** : Lance l'application
- **"Install Dependencies"** : Installe les dépendances
- **"Format Code (Black)"** : Formate tout le code
- **"Lint Code (Flake8)"** : Vérifie la qualité du code

### Debug
- **F5** : Lance l'application en mode debug
- Points d'arrêt : Cliquez à gauche des numéros de ligne

### Extensions installées automatiquement
Lors de l'ouverture, VS Code suggérera d'installer :
- Python
- Black Formatter
- Flake8
- GitLens
- EditorConfig

## 🎯 Structure du projet

```
ordobot/
├── main.py                    # Point d'entrée de l'application
├── assets/
│   ├── config.py             # Configuration globale
│   ├── modelIA.py            # Gestion des modèles IA
│   ├── IAIntegration.py      # Intégration IA
│   └── widget/
│       ├── MainWindows.py    # Fenêtre principale
│       └── ConfigDialog.py   # Dialog de configuration
├── docs/                     # Documentation
├── .vscode/                  # Configuration VS Code
├── .git/hooks/               # Hooks Git automatiques
└── requirements.txt          # Dépendances Python
```

## 🔧 Dépannage

### Problème : "git st" ne fonctionne pas
**Solution :** Relancez le script de configuration :
```bash
.\setup_git.bat
```

### Problème : Erreur de formatage avec Black
**Solution :** Formatez manuellement :
```bash
python -m black . --line-length=88
git add .
git commit -m "fix: formatage du code"
```

### Problème : L'application ne se lance pas
**Solutions :**
1. Vérifiez les dépendances : `pip install -r requirements.txt`
2. Vérifiez Python : `python --version` (doit être 3.11+)
3. Lancez depuis VS Code avec F5 pour voir les erreurs

## 🎨 Personnalisation

### Modifier la configuration Git
Éditez le fichier `.gitconfig` ou utilisez :
```bash
git config alias.mon_alias "ma commande"
```

### Modifier le formatage
Éditez le fichier `pyproject.toml` :
```toml
[tool.black]
line-length = 88  # Changez cette valeur
```

### Ajouter des tâches VS Code
Éditez `.vscode/tasks.json` pour ajouter vos propres tâches.

## 📝 Convention de commits

Utilisez ces préfixes selon vos modifications :
- `feat(scope): description` - Nouvelle fonctionnalité
- `fix(scope): description` - Correction de bug
- `refactor(scope): description` - Refactoring
- `docs(scope): description` - Documentation
- `chore(scope): description` - Maintenance

**Exemple :**
```bash
git cam "feat(ui): ajout de la sélection de modèle IA"
```

## 🚀 Prêt à développer !

Vous êtes maintenant prêt à développer efficacement sur OrdoBot ! 

**Pour commencer :**
1. Lancez `python main.py` pour voir l'application
2. Créez une branche avec `git co -b feat/mon-feature`
3. Modifiez le code dans VS Code
4. Commitez avec `git cam "feat: ma modification"`

Bon développement ! 🎯
