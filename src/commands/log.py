#!/usr/bin/env python3
"""
Module pour la commande log
Affiche l'historique des commits
"""

import os
import time
import sys
from datetime import datetime

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.commands.rev_parse import rev_parse
from src.commands.objects import read_object


def get_git_dir():
    """Retourne le chemin du dossier .mon_git"""
    return ".mon_git"


def read_commit_object(commit_sha):
    """
    Lit et parse un objet commit
    
    Args:
        commit_sha (str): SHA-1 du commit
    
    Returns:
        dict: Dictionnaire contenant les informations du commit
    """
    try:
        result = read_object(commit_sha)
        if not result or len(result) != 2 or result[0] != 'commit':
            raise ValueError(f"Invalid commit object: {commit_sha}")
        
        content = result[1].decode('utf-8') if isinstance(result[1], bytes) else result[1]
        
        lines = content.split('\n')
        commit_info = {
            'tree': None,
            'parent': None,
            'parents': [],  # Liste pour gérer les parents multiples
            'author': None,
            'committer': None,
            'message': []
        }
        
        in_message = False
        for i, line in enumerate(lines):
            if line.startswith('tree '):
                commit_info['tree'] = line[5:]
            elif line.startswith('parent '):
                parent_sha = line[7:]  # Corriger l'index
                commit_info['parents'].append(parent_sha)
                # Pour la compatibilité, garder le premier parent dans 'parent'
                if commit_info['parent'] is None:
                    commit_info['parent'] = parent_sha
            elif line.startswith('author '):
                commit_info['author'] = line[7:]
            elif line.startswith('committer '):
                commit_info['committer'] = line[10:]
            elif line == '':
                in_message = True
            else:
                # Si ce n'est pas une métadonnée et qu'on a déjà vu tree, c'est le message
                if commit_info['tree'] is not None:
                    clean_line = line.strip().rstrip('%')
                    if clean_line:
                        commit_info['message'].append(clean_line)
        
        # Convertir la liste de messages en une seule chaîne
        commit_info['message'] = '\n'.join(commit_info['message'])
        
        return commit_info
    except Exception as e:
        raise Exception(f"Error reading commit object {commit_sha}: {str(e)}")


def format_commit_line(commit_sha, commit_info, oneline=False):
    """
    Formate une ligne de commit pour l'affichage
    
    Args:
        commit_sha (str): SHA-1 du commit
        commit_info (dict): Informations du commit
        oneline (bool): Format compact si True
    
    Returns:
        str: Ligne formatée
    """
    short_sha = commit_sha[:7]
    
    if oneline:
        message = commit_info['message'] if commit_info['message'] else "No message"
        return f"{short_sha} {message}"
    else:
        # Format détaillé
        lines = []
        lines.append(f"commit {commit_sha}")
        
        if commit_info['parent']:
            lines.append(f"parent {commit_info['parent']}")
        
        if commit_info['author']:
            lines.append(f"author {commit_info['author']}")
        
        if commit_info['committer']:
            lines.append(f"committer {commit_info['committer']}")
        
        lines.append("")
        
        if commit_info['message']:
            lines.extend(commit_info['message'].split('\n')) # Split the message into lines
        
        lines.append("")
        return "\n".join(lines)


def get_commit_history(start_ref="HEAD", max_count=None):
    """
    Récupère l'historique des commits
    
    Args:
        start_ref (str): Référence de départ (HEAD par défaut)
        max_count (int): Nombre maximum de commits à afficher
    
    Returns:
        list: Liste des SHA-1 des commits dans l'ordre chronologique inverse
    """
    commits = []
    current_sha = rev_parse(start_ref)
    
    if not current_sha:
        return commits
    
    visited = set()
    queue = [current_sha]
    
    while queue and (max_count is None or len(commits) < max_count):
        commit_sha = queue.pop(0)
        
        if commit_sha in visited:
            continue
        
        visited.add(commit_sha)
        commits.append(commit_sha)
        
        # Lire le commit pour trouver le parent
        commit_info = read_commit_object(commit_sha)
        if commit_info and commit_info['parent']:
            queue.append(commit_info['parent'])
    
    return commits


def show_log(start_ref="HEAD", oneline=False, limit=None):
    """
    Affiche l'historique des commits
    
    Args:
        start_ref (str): Référence de départ
        oneline (bool): Format compact
        limit (int): Nombre maximum de commits
    
    Returns:
        bool: True si succès, False si échec
    """
    try:
        commits = get_commit_history(start_ref, limit)
        
        if not commits:
            print("Aucun commit trouvé.")
            return True
        
        for commit_sha in commits:
            commit_info = read_commit_object(commit_sha)
            if commit_info:
                print(format_commit_line(commit_sha, commit_info, oneline))
        
        return True
    except Exception as e:
        print(f"Erreur lors de l'affichage du log: {e}")
        return False


def main():
    """Fonction principale pour la commande log"""
    
    # Parser les arguments
    oneline = False
    max_count = None
    start_ref = "HEAD"
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == "--oneline":
            oneline = True
        elif arg == "-n" or arg == "--max-count":
            if i + 1 < len(sys.argv):
                try:
                    max_count = int(sys.argv[i + 1])
                    i += 1
                except ValueError:
                    print(f"Erreur: '{sys.argv[i + 1]}' n'est pas un nombre valide")
                    sys.exit(1)
            else:
                print("Erreur: -n/--max-count nécessite un argument")
                sys.exit(1)
        elif arg == "--help" or arg == "-h":
            print("Usage: gitBis log [--oneline] [-n <num>] [<commit>]")
            print("  --oneline    Afficher en format compact")
            print("  -n, --max-count <num>  Limiter le nombre de commits")
            print("  <commit>     Commit de départ (par défaut: HEAD)")
            sys.exit(0)
        elif not arg.startswith("-"):
            start_ref = arg
        else:
            print(f"Option inconnue: {arg}")
            print("Usage: gitBis log [--oneline] [-n <num>] [<commit>]")
            sys.exit(1)
        
        i += 1
    
    show_log(start_ref, oneline, max_count)


if __name__ == "__main__":
    main() 