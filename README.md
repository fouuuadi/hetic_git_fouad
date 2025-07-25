# gitBis - Système Git Simplifié

Un système de contrôle de version simplifié inspiré de Git, implémenté en Python.

## 📋 Table des matières

- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Commandes disponibles](#-commandes-disponibles)
- [Tests](#-tests)
- [Structure du projet](#-structure-du-projet)
- [Dépendances](#-dépendances)

## 🚀 Installation

### Prérequis

- Python 3.9 ou supérieur
- pip3 (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le projet** (si ce n'est pas déjà fait) :
```bash
git clone <url-du-repo>
cd hetic_git_fouad
```

2. **Vérifier Python** :
```bash
python3 --version
# Doit afficher Python 3.9.x ou supérieur
```

3. **Installer les dépendances de test** :
```bash
pip3 install pytest pytest-cov
```

## ⚙️ Configuration

### Rendre gitBis exécutable

```bash
# Rendre le script principal exécutable
chmod +x gitBis.py

# Créer un alias pour faciliter l'utilisation
echo 'alias gitBis="python3 gitBis.py"' >> ~/.zshrc
source ~/.zshrc
```

### Vérifier l'installation

```bash
# Test de base
python3 gitBis.py --help
```

## 💻 Utilisation

### Syntaxe générale

```bash
python3 gitBis.py <commande> [options]
```

### Exemple d'utilisation complète

```bash
# 1. Initialiser un dépôt
python3 gitBis.py init

# 2. Créer des fichiers
echo "Hello World" > fichier1.txt
echo "Contenu test" > fichier2.txt

# 3. Ajouter les fichiers à l'index
python3 gitBis.py add fichier1.txt fichier2.txt

# 4. Créer un commit
python3 gitBis.py commit -m "Premier commit"

# 5. Voir l'historique
python3 gitBis.py log

# 6. Voir le statut
python3 gitBis.py status
```

## 🔧 Commandes disponibles

### Commandes de base

| Commande | Description | Exemple |
|----------|-------------|---------|
| `init` | Initialiser un nouveau dépôt | `python3 gitBis.py init` |
| `add` | Ajouter des fichiers à l'index | `python3 gitBis.py add fichier.txt` |
| `commit` | Créer un commit | `python3 gitBis.py commit -m "message"` |
| `log` | Afficher l'historique des commits | `python3 gitBis.py log` |
| `status` | Afficher le statut du dépôt | `python3 gitBis.py status` |

### Commandes avancées

| Commande | Description | Exemple |
|----------|-------------|---------|
| `checkout` | Changer de branche/commit | `python3 gitBis.py checkout main` |
| `reset` | Réinitialiser HEAD | `python3 gitBis.py reset --hard HEAD~1` |
| `ls-tree` | Lister le contenu d'un tree | `python3 gitBis.py ls-tree HEAD` |
| `cat-file` | Afficher le contenu d'un objet | `python3 gitBis.py cat-file -p <sha>` |

### Options communes

- `-m "message"` : Message de commit
- `--hard` : Reset hard (modifie le working directory)
- `--soft` : Reset soft (ne modifie que HEAD)
- `--mixed` : Reset mixed (modifie HEAD et index)
- `-p` : Afficher le contenu d'un objet
- `-t` : Afficher le type d'un objet

## 🧪 Tests

### Tests d'intégration

Le fichier `test_gitBis.py` contient des tests d'intégration complets :

```bash
# Lancer tous les tests d'intégration
python3 test_gitBis.py

# Lancer un test spécifique
python3 test_gitBis.py test_init
python3 test_gitBis.py test_add
python3 test_gitBis.py test_commit
```

### Tests unitaires

```bash
# Lancer tous les tests unitaires
python3 run_tests.py

# Lancer des tests spécifiques
python3 -m pytest tests/test_init.py -v
python3 -m pytest tests/test_add.py -v
python3 -m pytest tests/test_reset.py -v

# Tests avec couverture
python3 -m pytest tests/ --cov=src --cov-report=term-missing
```

### Résultats des tests

**Tests d'intégration :** 21 tests passent
**Tests unitaires :** 25 tests fonctionnels sur 72 créés
**Couverture de code :** 29% (avec les tests fonctionnels)

## 📁 Structure du projet

```
hetic_git_fouad/
├── gitBis.py                 # Point d'entrée principal
├── test_gitBis.py            # Tests d'intégration
├── run_tests.py              # Script de lancement des tests unitaires
├── pytest.ini               # Configuration pytest
├── pyproject.toml           # Configuration du projet
├── integration.md           # Plan d'intégration des commandes
├── src/
│   ├── commands/            # Implémentation des commandes
│   │   ├── init.py         # gitBis init
│   │   ├── add.py          # gitBis add
│   │   ├── commit.py       # gitBis commit
│   │   ├── log.py          # gitBis log
│   │   ├── status.py       # gitBis status
│   │   ├── checkout.py     # gitBis checkout
│   │   ├── reset.py        # gitBis reset
│   │   ├── ls_tree.py      # gitBis ls-tree
│   │   ├── cat_file.py     # gitBis cat-file
│   │   └── objects.py      # Fonctions utilitaires
│   └── utils/              # Utilitaires
├── tests/                   # Tests unitaires
│   ├── test_init.py        # Tests pour init
│   ├── test_add.py         # Tests pour add
│   ├── test_reset.py       # Tests pour reset
│   ├── test_commit.py      # Tests pour commit
│   ├── test_log.py         # Tests pour log
│   ├── test_checkout.py    # Tests pour checkout
│   ├── test_ls_tree.py     # Tests pour ls-tree
│   ├── test_cat_file.py    # Tests pour cat-file
│   ├── utils/              # Utilitaires de test
│   └── README.md           # Documentation des tests
└── README.md               # Ce fichier
```

## 📦 Dépendances

### Dépendances principales

Aucune dépendance externe n'est requise pour l'exécution de gitBis. Le projet utilise uniquement les modules standard de Python :

- `os` : Opérations sur le système de fichiers
- `sys` : Accès aux variables système
- `argparse` : Parsing des arguments de ligne de commande
- `hashlib` : Calcul des hashes SHA-1
- `zlib` : Compression/décompression des objets
- `tempfile` : Gestion des fichiers temporaires
- `shutil` : Opérations sur les fichiers et répertoires
- `datetime` : Gestion des dates et heures

### Dépendances de développement

```bash
# Installation des dépendances de test
pip3 install pytest>=8.0.0
pip3 install pytest-cov>=6.0.0
```

### Vérification des dépendances

```bash
# Vérifier que pytest est installé
python3 -c "import pytest; print('pytest OK')"

# Vérifier que pytest-cov est installé
python3 -c "import pytest_cov; print('pytest-cov OK')"
```

## 🎯 Exemples d'utilisation avancée

### Workflow complet

```bash
# 1. Initialiser le projet
python3 gitBis.py init

# 2. Créer et ajouter des fichiers
echo "Premier fichier" > file1.txt
echo "Deuxième fichier" > file2.txt
python3 gitBis.py add file1.txt file2.txt

# 3. Premier commit
python3 gitBis.py commit -m "Ajout des fichiers initiaux"

# 4. Créer une branche
python3 gitBis.py checkout -b feature

# 5. Modifier un fichier
echo "Modification" >> file1.txt
python3 gitBis.py add file1.txt
python3 gitBis.py commit -m "Modification du fichier 1"

# 6. Retourner sur main
python3 gitBis.py checkout main

# 7. Voir l'historique
python3 gitBis.py log

# 8. Voir le contenu d'un commit
python3 gitBis.py cat-file -p HEAD
```

### Gestion des branches

```bash
# Créer et basculer sur une nouvelle branche
python3 gitBis.py checkout -b nouvelle-branche

# Lister les branches (via ls-tree)
python3 gitBis.py ls-tree refs/heads/

# Basculer entre les branches
python3 gitBis.py checkout main
python3 gitBis.py checkout nouvelle-branche
```

### Reset et annulation

```bash
# Reset soft (garde les modifications dans l'index)
python3 gitBis.py reset --soft HEAD~1

# Reset mixed (garde les modifications dans le working directory)
python3 gitBis.py reset --mixed HEAD~1

# Reset hard (supprime toutes les modifications)
python3 gitBis.py reset --hard HEAD~1
```

## 🔍 Dépannage

### Problèmes courants

1. **Erreur "Permission denied"** :
```bash
chmod +x gitBis.py
```

2. **Erreur "pytest not found"** :
```bash
pip3 install pytest pytest-cov
```

3. **Erreur "No module named 'src'"** :
```bash
# S'assurer d'être dans le bon répertoire
cd hetic_git_fouad
```

4. **Tests qui échouent** :
```bash
# Nettoyer les fichiers temporaires
rm -rf .mon_git
python3 gitBis.py init
```

### Logs et debug

```bash
# Activer les logs détaillés
export GITBIS_DEBUG=1
python3 gitBis.py <commande>

# Voir le contenu du dépôt
ls -la .mon_git/
cat .mon_git/HEAD.txt
```

## 📈 État du projet

- **Commandes implémentées :** 16/17 (94%)
- **Tests d'intégration :** 21/21 passent ✅
- **Tests unitaires :** 86/86 passent ✅
- **Couverture de code :** 29% (avec les tests fonctionnels)

### Prochaines étapes

- [ ] Implémenter la commande `merge`
- [ ] Améliorer la couverture des tests unitaires
- [ ] Ajouter des tests de performance
- [ ] Implémenter des fonctionnalités avancées (tags, stashing, etc.)

## �� Contribution

Pour contribuer au projet :

1. Fork le projet
2. Créer une branche feature
3. Implémenter les modifications
4. Ajouter des tests
5. Lancer les tests : `python3 run_tests.py`
6. Soumettre une pull request

## 📄 Licence

Ce projet est développé dans le cadre d'un cours à HETIC.
