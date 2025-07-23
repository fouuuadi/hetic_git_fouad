import os
import re
import fnmatch

def read_gitignore():
    """Lit le fichier .gitignore et retourne la liste des patterns"""
    gitignore_path = ".gitignore"
    patterns = []
    
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Ignorer les lignes vides et les commentaires
                    if line and not line.startswith('#'):
                        patterns.append(line)
        except Exception as e:
            print(f"Erreur lors de la lecture de .gitignore: {e}")
    
    return patterns

def should_ignore(path, patterns):
    """Détermine si un fichier/dossier doit être ignoré selon les patterns"""
    # Normaliser le chemin pour utiliser des slashes
    normalized_path = path.replace(os.sep, '/')
    
    for pattern in patterns:
        # Gérer les patterns avec des wildcards
        if fnmatch.fnmatch(normalized_path, pattern):
            return True
        
        # Gérer les patterns qui se terminent par /
        if pattern.endswith('/'):
            if normalized_path.startswith(pattern[:-1]) or normalized_path == pattern[:-1]:
                return True
        
        # Gérer les patterns qui commencent par /
        if pattern.startswith('/'):
            if normalized_path.endswith(pattern[1:]) or normalized_path == pattern[1:]:
                return True
        
        # Gérer les patterns simples
        if pattern in normalized_path:
            return True
    
    return False

def filter_ignored_files(files, patterns):
    """Filtre une liste de fichiers en excluant ceux qui correspondent aux patterns"""
    if not patterns:
        return files
    
    filtered_files = []
    for file_path in files:
        if not should_ignore(file_path, patterns):
            filtered_files.append(file_path)
    
    return filtered_files 