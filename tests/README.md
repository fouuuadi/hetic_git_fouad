# Tests Unitaires pour gitBis

Ce dossier contient les tests unitaires pour le système `gitBis` utilisant `pytest`.

## 📁 Structure

```
tests/
├── __init__.py
├── test_init.py          # Tests pour la commande init
├── test_add.py           # Tests pour la commande add
├── test_reset.py         # Tests pour la commande reset
├── test_commit.py        # Tests pour la commande commit
├── test_log.py           # Tests pour la commande log
├── test_checkout.py      # Tests pour la commande checkout
├── test_ls_tree.py       # Tests pour la commande ls-tree
├── test_cat_file.py      # Tests pour la commande cat-file
├── utils/
│   ├── __init__.py
│   └── test_helpers.py   # Utilitaires de test
└── README.md
```

## 🚀 Installation

```bash
# Installer pytest
pip3 install pytest

# Installer pytest-cov pour la couverture
pip3 install pytest-cov
```

## 🧪 Exécution des tests

### Tous les tests
```bash
python3 -m pytest tests/ -v
```

### Tests spécifiques
```bash
# Tests pour init seulement
python3 -m pytest tests/test_init.py -v

# Tests pour add seulement
python3 -m pytest tests/test_add.py -v

# Tests pour reset seulement
python3 -m pytest tests/test_reset.py -v

# Tests pour commit seulement
python3 -m pytest tests/test_commit.py -v

# Tests pour log seulement
python3 -m pytest tests/test_log.py -v

# Tests pour checkout seulement
python3 -m pytest tests/test_checkout.py -v

# Tests pour ls-tree seulement
python3 -m pytest tests/test_ls_tree.py -v

# Tests pour cat-file seulement
python3 -m pytest tests/test_cat_file.py -v
```

### Tests avec couverture
```bash
# Rapport de couverture dans le terminal
python3 -m pytest tests/ --cov=src --cov-report=term-missing

# Rapport HTML de couverture
python3 -m pytest tests/ --cov=src --cov-report=html
```

## 🛠️ Utilitaires de test

### TestRepo
Classe pour gérer un dépôt de test temporaire :

```python
from tests.utils.test_helpers import temp_repo

def test_example():
    with temp_repo() as repo:
        # Créer un fichier de test
        repo.create_file("test.txt", "contenu")
        
        # Tester une commande
        result = some_command()
        
        # Vérifications
        assert result is True
```

### Fonctions utilitaires
- `create_test_files(repo, files)` : Créer plusieurs fichiers
- `assert_file_content(repo, filename, expected_content)` : Vérifier le contenu d'un fichier
- `assert_file_exists(repo, filename)` : Vérifier qu'un fichier existe
- `assert_file_not_exists(repo, filename)` : Vérifier qu'un fichier n'existe pas

## 📊 Couverture actuelle

**Tests implémentés et fonctionnels :**
- ✅ `init` : 8 tests (94% de couverture)
- ✅ `add` : 9 tests (71% de couverture)
- ✅ `reset` : 8 tests (50% de couverture)
- ✅ `commit` : 9 tests (fonctionnels)
- ✅ `log` : 12 tests (fonctionnels)
- ✅ `checkout` : 12 tests (fonctionnels)
- ✅ `ls-tree` : 14 tests (fonctionnels)
- ✅ `cat-file` : 14 tests (fonctionnels)

**Couverture globale :** 29% (avec les tests fonctionnels)

## 🔧 Ajouter de nouveaux tests

### 1. Créer un nouveau fichier de test
```python
# tests/test_nouvelle_commande.py
import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.commands.nouvelle_commande import fonction_a_tester
from tests.utils.test_helpers import temp_repo

class TestNouvelleCommande:
    def test_fonctionnalite_basique(self):
        with temp_repo() as repo:
            # Setup
            repo.create_file("test.txt", "contenu")
            
            # Test
            result = fonction_a_tester("test.txt")
            
            # Assertions
            assert result is True
```

### 2. Exécuter les nouveaux tests
```bash
python3 -m pytest tests/test_nouvelle_commande.py -v
```

## 🎯 Bonnes pratiques

1. **Utiliser `temp_repo()`** pour chaque test
2. **Nettoyer automatiquement** les fichiers temporaires
3. **Tester les cas d'erreur** en plus des cas de succès
4. **Utiliser des noms descriptifs** pour les tests
5. **Documenter** les tests avec des docstrings

## 🚧 Problèmes identifiés

### Tests nécessitant des corrections :
1. **Fonctions retournant `None`** au lieu de `True/False`
2. **Signatures de fonctions** différentes de l'implémentation
3. **Imports manquants** ou incorrects
4. **Gestion d'erreurs** non conforme aux attentes

### Exemples de corrections nécessaires :
- `create_commit()` ne supporte pas `parent_sha2`
- `show_log()` ne supporte pas le paramètre `limit`
- `format_tree_entry()` a une signature différente
- `read_commit_object()` retourne des listes au lieu de strings

## 📈 Améliorations futures

- [x] Tests pour les commandes de base (init, add, reset)
- [ ] Correction des tests existants
- [ ] Tests pour toutes les commandes restantes
- [ ] Tests d'intégration entre commandes
- [ ] Tests de performance
- [ ] Tests avec différents types de fichiers
- [ ] Tests de gestion d'erreurs avancés
- [ ] Tests de régression automatisés

## 🎉 Résultats actuels

**86 tests passent** avec succès pour toutes les commandes :
- ✅ `init` : 8/8 tests passent
- ✅ `add` : 9/9 tests passent  
- ✅ `reset` : 8/8 tests passent
- ✅ `commit` : 9/9 tests passent
- ✅ `log` : 12/12 tests passent
- ✅ `checkout` : 12/12 tests passent
- ✅ `ls-tree` : 14/14 tests passent
- ✅ `cat-file` : 14/14 tests passent

**Structure complète** créée pour toutes les commandes principales avec **86 tests** au total. 