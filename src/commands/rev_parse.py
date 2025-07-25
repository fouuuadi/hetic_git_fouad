#!/usr/bin/env python3
"""
Module pour la commande rev-parse
Convertit une référence en SHA-1
"""

import os
import re
from pathlib import Path


def get_git_dir():
    """Retourne le chemin du dossier .mon_git"""
    return ".mon_git"


def read_head():
    """Lit le contenu de HEAD"""
    head_path = os.path.join(get_git_dir(), "HEAD.txt")
    try:
        with open(head_path, 'r') as f:
            content = f.read().strip()
        return content
    except FileNotFoundError:
        return None


def read_branch_ref(branch_name):
    """Lit la référence d'une branche"""
    ref_path = os.path.join(get_git_dir(), "refs", "heads", f"{branch_name}.txt")
    try:
        with open(ref_path, 'r') as f:
            content = f.read().strip()
            # Ignorer les lignes de commentaire
            if content.startswith('#'):
                return None
            return content
    except FileNotFoundError:
        return None


def is_valid_sha1(sha1):
    """Vérifie si une chaîne est un SHA-1 valide (40 caractères hexadécimaux)"""
    if not sha1:
        return False
    return bool(re.match(r'^[a-f0-9]{40}$', sha1))


def is_partial_sha1(sha1):
    """Vérifie si c'est un SHA-1 partiel (moins de 40 caractères)"""
    if not sha1:
        return False
    return bool(re.match(r'^[a-f0-9]{1,39}$', sha1))


def find_object_by_partial_sha1(partial_sha):
    """Trouve un objet par son SHA-1 partiel"""
    objects_dir = os.path.join(get_git_dir(), "objects")
    
    if not os.path.exists(objects_dir):
        return None
    
    # Chercher dans les sous-dossiers
    for subdir in os.listdir(objects_dir):
        subdir_path = os.path.join(objects_dir, subdir)
        if os.path.isdir(subdir_path):
            for filename in os.listdir(subdir_path):
                # Vérifier si le nom du fichier commence par la suite du SHA-1 partiel
                if filename.startswith(partial_sha[2:]):  # Enlever les 2 premiers caractères
                    # Vérifier si c'est un fichier .txt (objet Git)
                    if filename.endswith('.txt'):
                        return subdir + filename[:-4]  # Retirer l'extension .txt
                    else:
                        return subdir + filename
                # Vérifier aussi si le SHA-1 complet commence par le SHA-1 partiel
                elif (subdir + filename[:-4] if filename.endswith('.txt') else subdir + filename).startswith(partial_sha):
                    if filename.endswith('.txt'):
                        return subdir + filename[:-4]
                    else:
                        return subdir + filename
    
    return None


def rev_parse(ref):
    """
    Convertit une référence en SHA-1 complet
    
    Args:
        ref (str): La référence à résoudre (HEAD, nom de branche, SHA-1 partiel, etc.)
    
    Returns:
        str: Le SHA-1 complet ou None si la référence n'est pas trouvée
    """
    if not ref:
        return None
    
    # Cas 1: SHA-1 complet déjà
    if is_valid_sha1(ref):
        return ref
    
    # Cas 2: HEAD
    if ref.upper() == "HEAD":
        head_content = read_head()
        if head_content and head_content.startswith("ref: "):
            # HEAD pointe vers une branche
            branch_name = head_content[5:].strip()  # Enlever "ref: " et les espaces
            return read_branch_ref(branch_name.split('/')[-1])  # Prendre juste le nom de la branche
        else:
            # HEAD pointe directement vers un commit
            return head_content
    
    # Cas 3: Nom de branche
    branch_sha = read_branch_ref(ref)
    if branch_sha:
        return branch_sha
    
    # Cas 4: SHA-1 partiel
    if is_partial_sha1(ref):
        full_sha = find_object_by_partial_sha1(ref)
        if full_sha:
            return full_sha
    
    # Cas 5: Référence avec refs/heads/
    if ref.startswith("refs/heads/"):
        branch_name = ref[11:]  # Enlever "refs/heads/"
        return read_branch_ref(branch_name)
    
    # Cas 6: Référence avec refs/
    if ref.startswith("refs/"):
        ref_path = os.path.join(get_git_dir(), ref + ".txt")
        try:
            with open(ref_path, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            pass
    
    return None


def main():
    """Fonction principale pour la commande rev-parse"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: gitBis rev-parse <ref>")
        sys.exit(1)
    
    ref = sys.argv[1]
    result = rev_parse(ref)
    
    if result:
        print(result)
        sys.exit(0)
    else:
        print(f"fatal: ambiguous argument '{ref}': unknown revision or path not in the working tree.")
        sys.exit(1)


if __name__ == "__main__":
    main() 