#!/bin/bash

echo "🔧 Configuration rapide de l'environnement Git et formatage..."

echo
echo "📝 Configuration des alias Git..."
git config alias.st status
git config alias.co checkout
git config alias.br branch  
git config alias.ci commit
git config alias.cam "commit -am"
git config alias.lg "log --oneline --graph --decorate --all"
git config alias.unstage "reset HEAD --"

echo
echo "🔄 Configuration du rebase automatique..."
git config pull.rebase true
git config rebase.autoStash true
git config merge.ff only
git config branch.autosetupmerge always
git config branch.autosetuprebase always
git config rerere.enabled true

echo
echo "🎨 Formatage du code avec Black..."
python3 -m black . --line-length=88

echo
echo "✅ Configuration terminée!"
echo
echo "📋 Vous pouvez maintenant utiliser:"
echo "  git st          # Status"
echo "  git co <branch> # Checkout"
echo "  git cam \"msg\"   # Commit avec message"
echo "  git lg          # Log graphique"
echo
echo "🚀 Vous pouvez maintenant faire votre commit!"
