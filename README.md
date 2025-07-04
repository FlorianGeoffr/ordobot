# 🎯 Guide de démarrage rapide - OrdoBot

## ⚡ Démarrage en 3 étapes

### 1. Configuration (une seule fois)
```bash
# Dans PowerShell, dans le dossier du projet :
.\setup_git.bat
```

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Lancement
```bash
python main.py
```

## 🔑 Obtenir une clé API OpenAI

Pour utiliser les fonctionnalités d'intelligence artificielle de l'application, vous devez disposer d'une clé API OpenAI. Voici les étapes pour l'obtenir :

### Étape 1 : Créer un compte OpenAI
1. Rendez-vous sur [https://platform.openai.com/signup/](https://platform.openai.com/signup/).
2. Créez un compte ou connectez-vous si vous en avez déjà un.

### Étape 2 : Générer une clé API
1. Une fois connecté, accédez à [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys).
2. Cliquez sur **Create new secret key** pour générer une nouvelle clé API.
3. Copiez la clé générée et conservez-la en lieu sûr (vous ne pourrez pas la voir à nouveau).

### Étape 3 : Configurer la clé API dans OrdoBot
1. Lancez l'application OrdoBot.
2. Dans la barre de menu, cliquez sur **Configuration > IA > Sélectionner modèle et clé API...**.
3. Collez votre clé API dans le champ prévu à cet effet.
4. Cliquez sur **Tester** pour vérifier la validité de la clé.
5. Enregistrez la configuration.

---

**⚠️ Important :**  
- Ne partagez jamais votre clé API avec d'autres personnes. Elle donne accès à votre compte OpenAI.  
- L'utilisation de l'API OpenAI peut entraîner des frais. Consultez les [tarifs OpenAI](https://platform.openai.com/pricing/) pour plus

## 🔥 Workflow quotidien

```bash
# 1. Créer une branche
git co -b feat/ma-fonctionnalite

# 2. Développer (dans VS Code)
# - Modifiez vos fichiers
# - Le formatage se fait automatiquement

# 3. Commit (formatage automatique)
git cam "feat(ui): ajout de ma fonctionnalité"

# 4. Push
git push origin feat/ma-fonctionnalite
```

## 🛠️ Commandes Git configurées

| Court | Long | Usage |
|-------|------|-------|
| `git st` | `git status` | Voir l'état |
| `git co` | `git checkout` | Changer de branche |
| `git cam "msg"` | `git commit -am "msg"` | Commit rapide |
| `git lg` | `git log --graph` | Historique graphique |

## 📋 Tâches VS Code

**Ctrl+Shift+P** → "Tasks: Run Task" :
- **Run OrdoBot** : Lance l'app
- **Format Code** : Formate le code
- **Install Dependencies** : Installe les dépendances

## 🎨 Développement

1. **Ouvrez VS Code** dans le dossier du projet
2. **F5** pour débugger l'application
3. **Ctrl+S** formate automatiquement à la sauvegarde
4. **Extensions suggérées** s'installent automatiquement

## 📄 Conditions Générales d'Utilisation (CGU)

Vous pouvez consulter les Conditions Générales d'Utilisation directement depuis l'application en cliquant sur **Options > CGU** dans la barre de menu.

## 🚨 En cas de problème

### Alias Git ne marchent pas ?
```bash
.\setup_git.bat
```

### Erreur de formatage ?
```bash
python -m black . --line-length=88
```

### App ne se lance pas ?
```bash
pip install -r requirements.txt
python main.py
```

---
**🎯 Vous êtes prêt ! Commencez par lancer `python main.py`**
