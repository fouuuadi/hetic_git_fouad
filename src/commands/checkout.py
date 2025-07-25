#!/usr/bin/env python3
"""
Module pour la commande checkout
Basculer de branche ou créer une branche
"""

import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.commands.rev_parse import rev_parse


def get_git_dir():
    """Retourne le chemin du dossier .mon_git"""
    return ".mon_git"


def branch_exists(branch_name):
    """
    Vérifie si une branche existe
    
    Args:
        branch_name (str): Nom de la branche
    
    Returns:
        bool: True si la branche existe
    """
    branch_file = f".mon_git/refs/heads/{branch_name}.txt"
    return os.path.exists(branch_file)


def create_branch(branch_name, commit_sha):
    """
    Crée une nouvelle branche
    
    Args:
        branch_name (str): Nom de la nouvelle branche
        commit_sha (str): SHA-1 du commit de départ
    
    Returns:
        bool: True si la branche a été créée
    """
    try:
        # Créer le fichier de la branche
        branch_file = f".mon_git/refs/heads/{branch_name}.txt"
        os.makedirs(os.path.dirname(branch_file), exist_ok=True)
        
        with open(branch_file, 'w') as f:
            f.write(commit_sha)
        
        return True
    except Exception as e:
        print(f"Erreur lors de la création de la branche: {e}")
        return False


def update_head(branch_name=None, commit_sha=None):
    """
    Met à jour HEAD
    
    Args:
        branch_name (str): Nom de la branche (si basculer vers une branche)
        commit_sha (str): SHA-1 du commit (si basculer vers un commit)
    
    Returns:
        bool: True si HEAD a été mis à jour
    """
    try:
        if branch_name:
            # HEAD pointe vers une branche
            with open('.mon_git/HEAD.txt', 'w') as f:
                f.write(f"ref: refs/heads/{branch_name}")
        elif commit_sha:
            # HEAD pointe directement vers un commit (detached HEAD)
            with open('.mon_git/HEAD.txt', 'w') as f:
                f.write(commit_sha)
        
        return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour de HEAD: {e}")
        return False


def get_current_branch():
    """
    Récupère le nom de la branche actuelle
    
    Returns:
        str: Nom de la branche actuelle ou None si detached HEAD
    """
    try:
        with open('.mon_git/HEAD.txt', 'r') as f:
            content = f.read().strip()
        
        if content.startswith('ref: refs/heads/'):
            return content[16:]  # Enlever "ref: refs/heads/"
        else:
            return None  # Detached HEAD
    except Exception:
        return None


def checkout_branch(branch_name):
    """
    Basculer vers une branche existante
    
    Args:
        branch_name (str): Nom de la branche
    
    Returns:
        bool: True si le basculement a réussi
    """
    if not branch_exists(branch_name):
        print(f"fatal: A branch named '{branch_name}' could not be found.")
        return False
    
    # Récupérer le SHA-1 de la branche
    try:
        with open(f'.mon_git/refs/heads/{branch_name}.txt', 'r') as f:
            commit_sha = f.read().strip()
    except Exception as e:
        print(f"Erreur lors de la lecture de la branche: {e}")
        return False
    
    # Mettre à jour HEAD
    if update_head(branch_name=branch_name):
        print(f"Switched to branch '{branch_name}'")
        return True
    else:
        return False


def checkout_commit(commit_sha):
    """
    Basculer vers un commit spécifique (detached HEAD)
    
    Args:
        commit_sha (str): SHA-1 du commit
    
    Returns:
        bool: True si le basculement a réussi
    """
    # Vérifier que le commit existe
    resolved_sha = rev_parse(commit_sha)
    if not resolved_sha:
        print(f"fatal: reference is not a tree: {commit_sha}")
        return False
    
    # Mettre à jour HEAD
    if update_head(commit_sha=resolved_sha):
        print(f"Note: checking out '{resolved_sha[:7]}'.")
        print("You are in 'detached HEAD' state.")
        return True
    else:
        return False


def create_and_checkout_branch(branch_name, start_point="HEAD"):
    """
    Créer une nouvelle branche et basculer dessus
    
    Args:
        branch_name (str): Nom de la nouvelle branche
        start_point (str): Point de départ (commit ou branche)
    
    Returns:
        bool: True si la création et le basculement ont réussi
    """
    if branch_exists(branch_name):
        print(f"fatal: A branch named '{branch_name}' already exists.")
        return False
    
    # Récupérer le SHA-1 du point de départ
    commit_sha = rev_parse(start_point)
    if not commit_sha:
        print(f"fatal: reference is not a tree: {start_point}")
        return False
    
    # Créer la branche
    if not create_branch(branch_name, commit_sha):
        return False
    
    # Basculer vers la nouvelle branche
    if update_head(branch_name=branch_name):
        print(f"Switched to a new branch '{branch_name}'")
        return True
    else:
        return False


def checkout(target, create_branch_flag=False, start_point="HEAD"):
    """
    Fonction principale de checkout
    
    Args:
        target (str): Cible (nom de branche, SHA-1, ou nouvelle branche)
        create_branch_flag (bool): True si créer une nouvelle branche
        start_point (str): Point de départ pour la nouvelle branche
    
    Returns:
        bool: True si le checkout a réussi
    """
    if create_branch_flag:
        # Créer et basculer vers une nouvelle branche
        return create_and_checkout_branch(target, start_point)
    else:
        # Vérifier si c'est une branche existante
        if branch_exists(target):
            return checkout_branch(target)
        else:
            # Essayer de basculer vers un commit
            return checkout_commit(target)


def main():
    """Fonction principale pour la commande checkout"""
    
    if len(sys.argv) < 2:
        print("Usage: gitBis checkout <branch|commit>")
        print("   or: gitBis checkout -b <new_branch> [<start_point>]")
        sys.exit(1)
    
    args = sys.argv[1:]
    create_branch_flag = False
    target = None
    start_point = "HEAD"
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg == "-b":
            create_branch_flag = True
            if i + 1 < len(args):
                target = args[i + 1]
                i += 1
            else:
                print("fatal: -b requires a branch name")
                sys.exit(1)
        elif arg == "--help" or arg == "-h":
            print("Usage: gitBis checkout <branch|commit>")
            print("   or: gitBis checkout -b <new_branch> [<start_point>]")
            print("")
            print("Basculer vers une branche ou un commit")
            print("  -b    Créer et basculer vers une nouvelle branche")
            sys.exit(0)
        elif not target:
            target = arg
            # Vérifier s'il y a un point de départ pour -b
            if create_branch_flag and i + 1 < len(args):
                start_point = args[i + 1]
        else:
            print(f"Option inconnue: {arg}")
            sys.exit(1)
        
        i += 1
    
    if not target:
        print("fatal: A branch name or commit is required")
        sys.exit(1)
    
    success = checkout(target, create_branch_flag, start_point)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main() 