#!/usr/bin/env python3
"""
Module pour la commande ls-tree
Affiche le contenu d'un objet tree
"""

import os
import sys
import glob

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.commands.objects import read_object


def get_git_dir():
    """Retourne le chemin du dossier .mon_git"""
    return ".mon_git"


def resolve_short_sha(short_sha):
    """
    Résout un SHA court en SHA complet
    
    Args:
        short_sha (str): SHA court (7+ caractères)
    
    Returns:
        str: SHA complet ou None si non trouvé
    """
    if len(short_sha) >= 40:
        return short_sha
    
    git_dir = get_git_dir()
    objects_dir = os.path.join(git_dir, "objects")
    
    # Chercher dans tous les sous-répertoires
    for subdir in os.listdir(objects_dir):
        subdir_path = os.path.join(objects_dir, subdir)
        if os.path.isdir(subdir_path) and len(subdir) == 2:
            # Chercher les fichiers qui commencent par le SHA court
            pattern = os.path.join(subdir_path, f"{short_sha[len(subdir):]}*")
            matches = glob.glob(pattern)
            if matches:
                # Extraire le nom du fichier (sans extension)
                filename = os.path.basename(matches[0])
                if filename.endswith('.txt'):
                    filename = filename[:-4]
                return subdir + filename
    
    return None


def parse_tree_content(tree_content):
    """
    Parse le contenu d'un objet tree
    
    Args:
        tree_content (bytes): Contenu brut de l'objet tree
    
    Returns:
        list: Liste des dictionnaires d'entrées du tree
    """
    entries = []
    
    # Convertir en string si c'est des bytes
    if isinstance(tree_content, bytes):
        content_str = tree_content.decode('utf-8')
    else:
        content_str = tree_content
    
    # Parser ligne par ligne
    lines = content_str.strip().split('\n')
    
    for line in lines:
        if not line.strip():
            continue
        
        # Format: mode name sha
        parts = line.split(' ')
        if len(parts) < 3:
            continue
        
        mode = parts[0]
        sha = parts[-1]  # Le SHA est à la fin
        name = ' '.join(parts[1:-1])  # Le nom peut contenir des espaces
        
        # Déterminer le type basé sur le mode
        if mode.startswith('100'):
            obj_type = 'blob'
        elif mode.startswith('400'):
            obj_type = 'tree'
        else:
            obj_type = 'unknown'
        
        entries.append({
            'mode': mode,
            'type': obj_type,
            'sha': sha,
            'name': name
        })
    
    return entries


def format_tree_entry(entry):
    """
    Formate une entrée de tree pour l'affichage
    
    Args:
        entry (dict): Dictionnaire contenant mode, type, sha, name
    
    Returns:
        str: Ligne formatée
    """
    return f"{entry['mode']} {entry['type']} {entry['sha']}\t{entry['name']}"


def show_tree(tree_sha, long_format=False):
    """
    Affiche le contenu d'un objet tree
    
    Args:
        tree_sha (str): SHA-1 de l'objet tree
        long_format (bool): Format long d'affichage
    
    Returns:
        bool: True si succès, False si échec
    """
    try:
        # Résoudre le SHA court si nécessaire
        if len(tree_sha) < 40:
            resolved_sha = resolve_short_sha(tree_sha)
            if resolved_sha is None:
                print(f"fatal: Not a valid object name '{tree_sha}'")
                return False
            tree_sha = resolved_sha
        
        # Lire l'objet tree
        result = read_object(tree_sha)
        if not result:
            print(f"fatal: Not a valid object name '{tree_sha}'")
            return False
        
        if len(result) != 2 or result[0] != 'tree':
            print(f"fatal: Not a tree object '{tree_sha}'")
            return False
        
        tree_content = result[1]
        
        # Parser le contenu du tree
        entries = parse_tree_content(tree_content)
        
        # Afficher les entrées
        for entry in entries:
            if long_format:
                print(format_tree_entry(entry))
            else:
                print(f"{entry['mode']} {entry['type']} {entry['sha']}\t{entry['name']}")
        
        return True
    except Exception as e:
        print(f"Erreur lors de la lecture du tree: {e}")
        return False


def main():
    """Fonction principale pour la commande ls-tree"""
    
    if len(sys.argv) < 2:
        print("Usage: gitBis ls-tree <tree_sha>")
        print("  <tree_sha>  SHA-1 de l'objet tree à afficher")
        sys.exit(1)
    
    tree_sha = sys.argv[1]
    
    if tree_sha == "--help" or tree_sha == "-h":
        print("Usage: gitBis ls-tree <tree_sha>")
        print("  <tree_sha>  SHA-1 de l'objet tree à afficher")
        print("")
        print("Affiche le contenu d'un objet tree (fichiers et répertoires)")
        sys.exit(0)
    
    success = show_tree(tree_sha)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main() 