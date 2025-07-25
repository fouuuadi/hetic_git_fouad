#!/usr/bin/env python3
"""
Module pour la commande reset
Réinitialiser HEAD et/ou l'index
"""

import os
import sys
import shutil

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.commands.rev_parse import rev_parse
from src.commands.objects import read_object


def get_git_dir():
    """Retourne le chemin du dossier .mon_git"""
    return ".mon_git"


def read_index():
    """
    Lit le contenu de l'index
    
    Returns:
        dict: Dictionnaire des fichiers dans l'index {filename: sha}
    """
    index_file = ".mon_git/index"
    index_content = {}
    
    if os.path.exists(index_file):
        try:
            with open(index_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and ' ' in line:
                        parts = line.split(' ', 1)
                        if len(parts) == 2:
                            sha, filename = parts
                            index_content[filename] = sha
        except Exception as e:
            print(f"Erreur lors de la lecture de l'index: {e}")
    
    return index_content


def write_index(index_content):
    """
    Écrit le contenu dans l'index
    
    Args:
        index_content (dict): Dictionnaire des fichiers {filename: sha}
    """
    index_file = ".mon_git/index"
    try:
        with open(index_file, 'w') as f:
            for filename, sha in index_content.items():
                f.write(f"{sha} {filename}\n")
    except Exception as e:
        print(f"Erreur lors de l'écriture de l'index: {e}")


def get_tree_content(tree_sha):
    """
    Récupère le contenu d'un tree
    
    Args:
        tree_sha (str): SHA-1 du tree
    
    Returns:
        dict: Dictionnaire des fichiers dans le tree {filename: sha}
    """
    tree_content = {}
    
    try:
        result = read_object(tree_sha)
        if not result or len(result) != 2 or result[0] != 'tree':
            return tree_content
        
        content = result[1]
        if isinstance(content, bytes):
            content_str = content.decode('utf-8')
        else:
            content_str = content
        
        lines = content_str.strip().split('\n')
        for line in lines:
            if line and ' ' in line:
                parts = line.split(' ', 2)
                if len(parts) >= 3:
                    mode, sha, filename = parts[0], parts[1], parts[2]
                    tree_content[filename] = sha
    except Exception as e:
        print(f"Erreur lors de la lecture du tree: {e}")
    
    return tree_content


def update_working_directory(tree_content):
    """
    Met à jour le working directory avec le contenu du tree
    
    Args:
        tree_content (dict): Dictionnaire des fichiers {filename: sha}
    """
    # Pour simplifier, on ne met à jour que les fichiers qui existent réellement
    for filename, sha in tree_content.items():
        try:
            result = read_object(sha)
            if result and len(result) == 2 and result[0] == 'blob':
                content = result[1]
                if isinstance(content, bytes):
                    content_str = content.decode('utf-8')
                else:
                    content_str = content
                
                # Créer les répertoires parents si nécessaire
                dir_path = os.path.dirname(filename)
                if dir_path:
                    os.makedirs(dir_path, exist_ok=True)
                
                with open(filename, 'w') as f:
                    f.write(content_str)
        except Exception as e:
            # Ignorer silencieusement les erreurs pour les fichiers non trouvés
            # Cela peut arriver si certains objets n'existent pas dans le dépôt
            pass


def update_head(commit_sha):
    """
    Met à jour HEAD vers le commit spécifié
    
    Args:
        commit_sha (str): SHA-1 du commit
    
    Returns:
        bool: True si HEAD a été mis à jour
    """
    try:
        with open('.mon_git/HEAD.txt', 'r') as f:
            head_content = f.read().strip()
        
        if head_content.startswith('ref: refs/heads/'):
            # HEAD pointe vers une branche
            branch_name = head_content[16:]  # Enlever "ref: refs/heads/"
            branch_file = f'.mon_git/refs/heads/{branch_name}.txt'
            
            with open(branch_file, 'w') as f:
                f.write(commit_sha)
        else:
            # HEAD pointe directement vers un commit (detached HEAD)
            with open('.mon_git/HEAD.txt', 'w') as f:
                f.write(commit_sha)
        
        return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour de HEAD: {e}")
        return False


def reset_soft(commit_sha):
    """
    Reset soft : réinitialise seulement HEAD
    
    Args:
        commit_sha (str): SHA-1 du commit cible
    
    Returns:
        bool: True si le reset a réussi
    """
    return update_head(commit_sha)


def reset_mixed(commit_sha):
    """
    Reset mixed : réinitialise HEAD et l'index
    
    Args:
        commit_sha (str): SHA-1 du commit cible
    
    Returns:
        bool: True si le reset a réussi
    """
    # Récupérer le tree du commit
    try:
        result = read_object(commit_sha)
        if not result or len(result) != 2 or result[0] != 'commit':
            print(f"fatal: Not a valid commit: {commit_sha}")
            return False
        
        content = result[1]
        if isinstance(content, bytes):
            content_str = content.decode('utf-8')
        else:
            content_str = content
        
        # Extraire le tree SHA
        lines = content_str.strip().split('\n')
        tree_sha = None
        for line in lines:
            if line.startswith('tree '):
                tree_sha = line[5:]
                break
        
        if not tree_sha:
            print(f"fatal: Invalid commit object: {commit_sha}")
            return False
        
        # Mettre à jour HEAD
        if not update_head(commit_sha):
            return False
        
        # Mettre à jour l'index avec le contenu du tree
        tree_content = get_tree_content(tree_sha)
        write_index(tree_content)
        
        return True
    except Exception as e:
        print(f"Erreur lors du reset mixed: {e}")
        return False


def reset_hard(commit_sha):
    """
    Reset hard : réinitialise HEAD, l'index et le working directory
    
    Args:
        commit_sha (str): SHA-1 du commit cible
    
    Returns:
        bool: True si le reset a réussi
    """
    # Récupérer le tree du commit
    try:
        result = read_object(commit_sha)
        if not result or len(result) != 2 or result[0] != 'commit':
            print(f"fatal: Not a valid commit: {commit_sha}")
            return False
        
        content = result[1]
        if isinstance(content, bytes):
            content_str = content.decode('utf-8')
        else:
            content_str = content
        
        # Extraire le tree SHA
        lines = content_str.strip().split('\n')
        tree_sha = None
        for line in lines:
            if line.startswith('tree '):
                tree_sha = line[5:]
                break
        
        if not tree_sha:
            print(f"fatal: Invalid commit object: {commit_sha}")
            return False
        
        # Mettre à jour HEAD
        if not update_head(commit_sha):
            return False
        
        # Mettre à jour l'index avec le contenu du tree
        tree_content = get_tree_content(tree_sha)
        write_index(tree_content)
        
        # Mettre à jour le working directory
        update_working_directory(tree_content)
        
        return True
    except Exception as e:
        print(f"Erreur lors du reset hard: {e}")
        return False


def reset(target, mode="mixed"):
    """
    Fonction principale de reset
    
    Args:
        target (str): Cible (commit SHA ou référence)
        mode (str): Mode de reset (soft, mixed, hard)
    
    Returns:
        bool: True si le reset a réussi
    """
    # Résoudre la référence en SHA-1
    commit_sha = rev_parse(target)
    if not commit_sha:
        print(f"fatal: Not a valid object name: {target}")
        return False
    
    # Vérifier que c'est bien un commit
    try:
        result = read_object(commit_sha)
        if not result or len(result) != 2 or result[0] != 'commit':
            print(f"fatal: Not a valid commit: {target}")
            return False
    except Exception as e:
        print(f"fatal: Not a valid object name: {target}")
        return False
    
    # Exécuter le reset selon le mode
    if mode == "soft":
        return reset_soft(commit_sha)
    elif mode == "mixed":
        return reset_mixed(commit_sha)
    elif mode == "hard":
        return reset_hard(commit_sha)
    else:
        print(f"fatal: Invalid reset mode: {mode}")
        return False


def main():
    """Fonction principale pour la commande reset"""
    
    if len(sys.argv) < 2:
        print("Usage: gitBis reset [--soft|--mixed|--hard] <commit>")
        print("")
        print("Réinitialiser HEAD et/ou l'index vers un commit")
        print("  --soft    Réinitialiser seulement HEAD")
        print("  --mixed   Réinitialiser HEAD et l'index (défaut)")
        print("  --hard    Réinitialiser HEAD, l'index et le working directory")
        sys.exit(1)
    
    args = sys.argv[1:]
    mode = "mixed"
    target = None
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg == "--soft":
            mode = "soft"
        elif arg == "--mixed":
            mode = "mixed"
        elif arg == "--hard":
            mode = "hard"
        elif arg == "--help" or arg == "-h":
            print("Usage: gitBis reset [--soft|--mixed|--hard] <commit>")
            print("")
            print("Réinitialiser HEAD et/ou l'index vers un commit")
            print("  --soft    Réinitialiser seulement HEAD")
            print("  --mixed   Réinitialiser HEAD et l'index (défaut)")
            print("  --hard    Réinitialiser HEAD, l'index et le working directory")
            sys.exit(0)
        elif not target:
            target = arg
        else:
            print(f"Option inconnue: {arg}")
            sys.exit(1)
        
        i += 1
    
    if not target:
        print("fatal: A commit is required")
        sys.exit(1)
    
    success = reset(target, mode)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main() 