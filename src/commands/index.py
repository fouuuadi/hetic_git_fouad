# gestion de l'index (staging area)

import os
import json
from . import create_tree, hash_object
INDEX_PATH = '.git/index'


def read_index():
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, 'r') as f:
            return json.load(f)
    return {}

def write_index(index):
    with open(INDEX_PATH, 'w') as f:
        json.dump(index, f, indent=2)

def add(files):
    index = read_index()

    for file_path in files:
        if not os.path.isfile(file_path):
            print(f"Skipped (not a file): {file_path}")
            continue

        sha = hash_object(file_path)
        index[file_path] = sha
        print(f"Added {file_path}")

    write_index(index)

def rm(files, cached=False):
    index = read_index()
    for file_path in files:
        # Suppression du fichier sur le disque sauf si --cached
        if not cached and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Supprimé du disque : {file_path}")
            except Exception as e:
                print(f"Erreur lors de la suppression de {file_path} : {e}")
        elif not cached:
            print(f"Fichier non trouvé sur le disque : {file_path}")

        # Suppression de l'index
        if file_path in index:
            del index[file_path]
            print(f"Supprimé de l'index : {file_path}")
        else:
            print(f"Fichier non présent dans l'index : {file_path}")

    write_index(index)


def index_to_tree():
    index = read_index()
    entries = []
    for path, sha in index.items():
        mode = b"100644" 
        name = os.path.basename(path)
        entries.append((mode, name, sha))
    tree_sha1 = create_tree(entries)
    print("DEBUG tree_sha1:", tree_sha1)
    return tree_sha1

