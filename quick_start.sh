#!/bin/bash

# Script de démarrage rapide pour gitBis
# Usage: ./quick_start.sh

set -e  # Arrêter en cas d'erreur

echo "🚀 DÉMARRAGE RAPIDE GITBIS"
echo "=========================="

# Vérifier Python
echo "📋 Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python $PYTHON_VERSION détecté"

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip3 install -r requirements.txt

# Rendre les scripts exécutables
echo "🔧 Configuration des permissions..."
chmod +x gitBis.py
chmod +x setup.py
chmod +x run_tests.py

# Test rapide
echo "🧪 Test rapide..."
python3 gitBis.py init
python3 gitBis.py --help

echo ""
echo "🎉 Installation terminée !"
echo ""
echo "📚 Commandes utiles :"
echo "  python3 gitBis.py init            # Initialiser un dépôt"
echo "  python3 gitBis.py add fichier.txt # Ajouter un fichier"
echo "  python3 gitBis.py commit -m 'msg' # Créer un commit"
echo "  python3 gitBis.py log             # Voir l'historique"
echo "  python3 run_tests.py              # Lancer les tests"
echo "  python3 test_gitBis.py            # Tests d'intégration"
echo ""
echo "💡 Pour créer un alias :"
echo "  echo 'alias gitBis=\"python3 gitBis.py\"' >> ~/.zshrc"
echo "  source ~/.zshrc" 