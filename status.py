# status.py
# -*- coding: utf-8 -*-
"""
status.py - Implémente la commande `git status` en Python.
Affiche la branche courante, les changements mis en scène (staged),
les changements non indexés (unstaged) et les fichiers non suivis.
"""

import os
import hashlib
import fnmatch

GIT_DIR = ".git"


def read_head():
    # Lit .git/HEAD pour obtenir la référence (branche ou SHA)
    ref = open(os.path.join(GIT_DIR, "HEAD")).read().strip()
    if ref.startswith("ref:"):
        ref_path = ref.split()[1]
        # Retourne le SHA de la branche courante
        return open(os.path.join(GIT_DIR, ref_path)).read().strip()
    # HEAD détaché : retour direct du SHA
    return ref


def hash_file(path):
    # Calcule le SHA-1 Git d'un fichier (blob)
    with open(path, "rb") as f:
        data = f.read()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def load_index():
    """
    Charge l'index Git sous forme de dict {chemin: blob_sha}.
    Pour l'instant, on utilise `git ls-files -s` en attendant un parser binaire.
    """
    index = {}
    lines = os.popen(f"git --git-dir={GIT_DIR} ls-files -s").read().splitlines()
    for line in lines:
        parts = line.split()
        blob_sha = parts[1]
        path = parts[3]
        index[path] = blob_sha
    return index


def ls_tree(tree_sha):
    """
    Liste récursivement le contenu d'un arbre Git (tree) donné.
    Retourne un dict {chemin: blob_sha}.
    """
    tree = {}
    lines = os.popen(f"git --git-dir={GIT_DIR} ls-tree -r {tree_sha}").read().splitlines()
    for line in lines:
        parts = line.split()
        blob_sha = parts[2]
        path = parts[3]
        tree[path] = blob_sha
    return tree


def load_gitignore():
    # Charge les patterns de .gitignore (simplifié)
    patterns = []
    try:
        with open('.gitignore') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
    except FileNotFoundError:
        pass
    return patterns


def is_ignored(path, patterns):
    # Vérifie qu'un chemin matche un pattern de .gitignore
    for pat in patterns:
        if fnmatch.fnmatch(path, pat):
            return True
    return False


def git_status():
    """
    Affiche l'état du dépôt :
    - branche courante
    - changements staged vs HEAD
    - changements unstaged vs index
    - fichiers non suivis
    """
    # 1. Branche / HEAD
    head_sha = read_head()
    print(f"Sur la branche {head_sha[:7]}")

    # 2. Arbre HEAD
    commit_info = os.popen(f"git --git-dir={GIT_DIR} cat-file -p {head_sha}").read()
    tree_sha = [l.split()[1] for l in commit_info.splitlines() if l.startswith('tree')][0]
    head_tree = ls_tree(tree_sha)

    # 3. Index
    index = load_index()

    # 4. Staged changes (index vs HEAD)
    staged_new, staged_mod, staged_del = [], [], []
    for path, sha in index.items():
        if path not in head_tree:
            staged_new.append(path)
        elif head_tree[path] != sha:
            staged_mod.append(path)
    for path in head_tree:
        if path not in index:
            staged_del.append(path)
    if staged_new or staged_mod or staged_del:
        print("\nModifications prêtes à être validées :")
        for p in staged_new:
            print(f"  nouveau fichier : {p}")
        for p in staged_mod:
            print(f"  modifié         : {p}")
        for p in staged_del:
            print(f"  supprimé        : {p}")

    # 5. Unstaged changes (working tree vs index)
    unstaged_mod, unstaged_del = [], []
    for path, sha in index.items():
        if not os.path.exists(path):
            unstaged_del.append(path)
        else:
            current_sha = hash_file(path)
            if current_sha != sha:
                unstaged_mod.append(path)
    if unstaged_mod or unstaged_del:
        print("\nModifications non indexées :")
        for p in unstaged_mod:
            print(f"  modifié         : {p}")
        for p in unstaged_del:
            print(f"  supprimé        : {p}")

    # 6. Fichiers non suivis
    patterns = load_gitignore()
    work_files = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d != GIT_DIR]
        for f in files:
            rel_path = os.path.join(root, f).lstrip('./')
            work_files.append(rel_path)
    untracked = [f for f in work_files if f not in index and not is_ignored(f, patterns)]
    if untracked:
        print("\nFichiers non suivis :")
        for p in untracked:
            print(f"  {p}")


if __name__ == "__main__":
    git_status()