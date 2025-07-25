#!/usr/bin/env python3
"""
Module pour la commande show-ref
Affiche les références du dépôt Git
"""

import os
import glob
from pathlib import Path


def get_git_dir():
    """Retourne le chemin du dossier .mon_git"""
    return ".mon_git"


def read_ref_file(ref_path):
    """Lit le contenu d'un fichier de référence"""
    try:
        with open(ref_path, 'r') as f:
            content = f.read().strip()
            # Ignorer les lignes de commentaire
            if content.startswith('#'):
                return None
            return content
    except FileNotFoundError:
        return None


def get_all_refs():
    """
    Récupère toutes les références du dépôt
    
    Returns:
        list: Liste de tuples (sha, ref_name)
    """
    refs = []
    git_dir = get_git_dir()
    
    # Chercher dans refs/heads/
    heads_dir = os.path.join(git_dir, "refs", "heads")
    if os.path.exists(heads_dir):
        for branch_file in os.listdir(heads_dir):
            if branch_file.endswith('.txt'):
                branch_name = branch_file[:-4]  # Enlever l'extension .txt
                ref_path = os.path.join(heads_dir, branch_file)
                sha = read_ref_file(ref_path)
                if sha:
                    refs.append((sha, f"refs/heads/{branch_name}"))
    
    # Chercher dans refs/tags/ (pour les futures extensions)
    tags_dir = os.path.join(git_dir, "refs", "tags")
    if os.path.exists(tags_dir):
        for tag_file in os.listdir(tags_dir):
            if tag_file.endswith('.txt'):
                tag_name = tag_file[:-4]  # Enlever l'extension .txt
                ref_path = os.path.join(tags_dir, tag_file)
                sha = read_ref_file(ref_path)
                if sha:
                    refs.append((sha, f"refs/tags/{tag_name}"))
    
    # Chercher dans refs/remotes/ (pour les futures extensions)
    remotes_dir = os.path.join(git_dir, "refs", "remotes")
    if os.path.exists(remotes_dir):
        for remote_dir in os.listdir(remotes_dir):
            remote_path = os.path.join(remotes_dir, remote_dir)
            if os.path.isdir(remote_path):
                for branch_file in os.listdir(remote_path):
                    if branch_file.endswith('.txt'):
                        branch_name = branch_file[:-4]
                        ref_path = os.path.join(remote_path, branch_file)
                        sha = read_ref_file(ref_path)
                        if sha:
                            refs.append((sha, f"refs/remotes/{remote_dir}/{branch_name}"))
    
    return refs


def show_refs(heads_only=False, tags_only=False):
    """
    Affiche les références du dépôt
    
    Args:
        heads_only (bool): Afficher seulement les branches
        tags_only (bool): Afficher seulement les tags
    """
    refs = get_all_refs()
    
    if not refs:
        print("Aucune référence trouvée dans le dépôt.")
        return
    
    # Filtrer selon les options
    if heads_only:
        refs = [ref for ref in refs if ref[1].startswith("refs/heads/")]
    elif tags_only:
        refs = [ref for ref in refs if ref[1].startswith("refs/tags/")]
    
    # Trier par nom de référence
    refs.sort(key=lambda x: x[1])
    
    # Afficher les références
    for sha, ref_name in refs:
        print(f"{sha} {ref_name}")


def main():
    """Fonction principale pour la commande show-ref"""
    import sys
    
    # Parser les arguments
    heads_only = False
    tags_only = False
    
    for arg in sys.argv[1:]:
        if arg == "--heads":
            heads_only = True
        elif arg == "--tags":
            tags_only = True
        elif arg == "--help" or arg == "-h":
            print("Usage: gitBis show-ref [--heads] [--tags]")
            print("  --heads    Afficher seulement les branches")
            print("  --tags     Afficher seulement les tags")
            sys.exit(0)
        else:
            print(f"Option inconnue: {arg}")
            print("Usage: gitBis show-ref [--heads] [--tags]")
            sys.exit(1)
    
    show_refs(heads_only=heads_only, tags_only=tags_only)


if __name__ == "__main__":
    main() 