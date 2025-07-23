import os
import hashlib
import re

GIT_DIR = ".mon_git"

def read_head():
    """Lit .mon_git/HEAD pour obtenir la référence (branche ou SHA)"""
    head_path = os.path.join(GIT_DIR, "HEAD")
    try:
        ref = open(head_path).read().strip()
        if ref.startswith("ref:"):
            # HEAD pointe vers une branche
            ref_path = ref.split()[1]
            ref_file = os.path.join(GIT_DIR, ref_path)
            try:
                commit_sha = open(ref_file).read().strip()
                if commit_sha:  # Si le fichier contient un SHA
                    return commit_sha
                else:  # Si le fichier est vide
                    return ref_path.split('/')[-1]  # Retourne le nom de la branche
            except FileNotFoundError:
                # Aucune validation encore : retourne le nom de la branche
                return ref_path.split('/')[-1]
        # HEAD détaché : retourne le SHA
        return ref
    except FileNotFoundError:
        return None

def hash_file(path):
    """Calcule le SHA-1 Git d'un fichier (blob)"""
    try:
        with open(path, "rb") as f:
            data = f.read()
        header = f"blob {len(data)}\0".encode()
        return hashlib.sha1(header + data).hexdigest()
    except Exception:
        return None

def read_index():
    """Lit l'index pour obtenir les fichiers suivis"""
    from .add import read_index
    return read_index()

def git_status():
    """Affiche le statut du dépôt Git"""
    
    # 1. Vérifier si on est dans un dépôt Git
    if not os.path.isdir(GIT_DIR):
        print("Erreur : ce répertoire n'est pas un dépôt Git ('.mon_git' manquant).")
        return

    # 2. Branche / HEAD
    head = read_head()
    if head is None:
        print("Sur la branche main")
        print("Aucun commit encore")
    elif len(head) == 40 and re.fullmatch(r"[0-9a-f]{40}", head):
        print(f"Sur la branche main (commit {head[:7]})")
    else:
        print(f"Sur la branche {head}")
        print("Aucun commit encore")

    # 3. Lire l'index (staging area)
    index_files = read_index()
    
    # 4. Lire les patterns .gitignore
    from .gitignore import read_gitignore, filter_ignored_files
    gitignore_patterns = read_gitignore()
    
    # 5. Fichiers du working tree
    work_files = []
    for root, dirs, files in os.walk('.'):
        # Ignorer les dossiers .git et .mon_git
        dirs[:] = [d for d in dirs if d not in ['.git', '.mon_git']]
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, '.')
            # Uniformiser les séparateurs en '/'
            rel = rel.replace(os.sep, '/')
            work_files.append(rel)

    # 6. Filtrer les fichiers ignorés
    work_files = filter_ignored_files(work_files, gitignore_patterns)

    # 7. Détecter les nouveaux fichiers (non suivis)
    untracked = [f for f in work_files if f not in index_files]
    
    # 8. Détecter les fichiers modifiés (différents de l'index)
    modified = []
    for f in work_files:
        if f in index_files:
            current_hash = hash_file(f)
            if current_hash and current_hash != index_files[f]:
                modified.append(f)
    
    # 9. Détecter les fichiers supprimés (dans l'index mais pas dans le working tree)
    deleted = [f for f in index_files if f not in work_files]
    
    # 10. Détecter les fichiers prêts à être commités (dans l'index)
    staged = [f for f in index_files if f in work_files and hash_file(f) == index_files[f]]

    # Affichage
    if staged:
        print("\nModifications prêtes à être validées :")
        for f in staged:
            print(f"  nouveau fichier : {f}")
    
    if modified:
        print("\nModifications non indexées :")
        for f in modified:
            print(f"  modifié         : {f}")
    
    if deleted:
        print("\nModifications non indexées :")
        for f in deleted:
            print(f"  supprimé        : {f}")
    
    if untracked:
        print("\nFichiers non suivis :")
        for f in untracked:
            print(f"  {f}")
    
    if not any([staged, modified, deleted, untracked]):
        print("\nAucune modification")
        print("working tree propre") 