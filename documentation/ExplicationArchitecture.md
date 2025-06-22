# Explication de l'architecture du projet Mini Git

Ce projet est une réimplémentation simplifiée de Git en Python. Il a pour but de reproduire certaines commandes internes de Git afin de mieux comprendre son fonctionnement.

---

## 🔹 Point d'entrée

Le fichier principal du projet est :

```bash
gitBis.py
```

Ce fichier agit comme un mini `git` :

* Il utilise `argparse` pour parser les sous-commandes (ex : `hash-object`)
* Il délègue l'exécution de chaque commande à un module séparé

---

## 🔹 Dossier `src/`

C’est le cœur de ton projet Python. Il contient :

### 1. `core/`

Contient la **logique interne (plomberie)** des commandes Git :

* `hash_object.py` : gère le calcul du hash SHA-1 Git, la compression zlib, et l’écriture dans `.git/objects/`

Ce dossier contiendra plus tard :

* `commit.py`, `cat_file.py`, etc. selon les commandes que tu ajoutes

### 2. `commands/`

C’est un **pont entre l’utilisateur et la logique Git**. Chaque fichier ici :

* récupère les arguments en ligne de commande
* appelle les fonctions dans `core/`

Exemple : `hash_object_cmd.py` appelle `hash_object_git()` depuis `core/hash_object.py`

### 3. `utils/`

Ce dossier est **optionnel**, prévu pour :

* des fonctions d’aide générales
* des décorateurs, helpers, gestion de fichiers, etc.

Pour l’instant tu peux laisser `extensions.py` vide, ou supprimer le fichier si tu ne l’utilises pas.

---

## 🔹 Dossier `tests/`

Contient les **tests unitaires**. Exemple fourni :

* `test_hash_object.py` : vérifie que `hash_object_git()` renvoie bien un hash SHA-1 valide sans écrire dans `.git/`

Tu peux exécuter les tests avec `pytest`.

---

## 🔹 Dossier `documentation/`

Ce dossier contient des fichiers de **documentation technique ou de rapport**.

Exemple :

* `README_DOC.txt` : notes, schémas, objectifs techniques, explication des algos, etc.

---

## 🔹 Fichiers à la racine

* `gitBis.py` : point d’entrée CLI
* `requirements.txt` : dépendances Python
* `.gitignore` : fichiers/dossiers à exclure de Git
* `README.md` : explication du projet et des étapes d’installation

---

## 🔹 Exemple d'exécution

```bash
git init
echo "bonjour" > test.txt
python gitBis.py hash-object test.txt --write
```

Cela va :

1. Lire le fichier
2. Le transformer en objet Git de type `blob`
3. Générer le hash SHA-1
4. Le compresser et l’écrire dans `.git/objects/xx/yyyyyy`

---

## Résumé logique

| Fichier         | Rôle                                        |
| --------------- | ------------------------------------------- |
| `gitBis.py`     | Gère l’interface CLI principale             |
| `src/core/`     | Contient la logique Git réelle (bas niveau) |
| `src/commands/` | Sert d’intermédiaire entre CLI et logique   |
| `src/utils/`    | Aides générales (optionnelles)              |
| `tests/`        | Tests unitaires                             |

Tu es sur de très bonnes bases 👍
