import os
import struct
import hashlib
import zlib
from .gitignore import read_gitignore, should_ignore, filter_ignored_files

def get_git_dir():
    """
    Détecte automatiquement le répertoire Git à utiliser.
    Priorité : GIT_DIR env > .mon_git > .mon_git{1-150}
    """
    # Utilisation de la variable d'environnement GIT_DIR si définie
    if 'GIT_DIR' in os.environ:
        return os.environ['GIT_DIR']
    
    # Vérifier si .mon_git existe
    if os.path.exists('.mon_git'):
        return '.mon_git'
    
    # Chercher un répertoire .mon_git{nombre}
    for i in range(1, 151):
        git_dir = f".mon_git{i}"
        if os.path.exists(git_dir):
            return git_dir
    
    # Par défaut, utiliser .mon_git
    return '.mon_git'

# Utilisation de la fonction de détection automatique
GIT_DIR = get_git_dir()
INDEX_PATH = os.path.join(GIT_DIR, 'index.txt')

def read_index():
    """Lire l'index texte Git"""
    git_dir = get_git_dir()
    index_path = os.path.join(git_dir, 'index.txt')
    if not os.path.exists(index_path):
        return {}
    
    index_data = {}
    try:
        with open(index_path, 'r') as f:
            for line in f:
                line = line.strip()
                # Ignorer les commentaires et lignes vides
                if line and not line.startswith('#'):
                    # Format: mode|hash|filename
                    if '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 3:
                            mode = int(parts[0])
                            sha = parts[1]
                            filename = parts[2]
                            index_data[filename] = sha
    except Exception as e:
        print(f"Erreur lors de la lecture de l'index: {e}")
        return {}
    
    return index_data

def write_index(index_data):
    """Écrire l'index au format texte Git"""
    git_dir = get_git_dir()
    index_path = os.path.join(git_dir, 'index.txt')
    try:
        with open(index_path, 'w') as f:
            f.write("# Git Index File\n")
            f.write("# Version: 2\n")
            f.write(f"# Number of entries: {len(index_data)}\n")
            f.write("# Format: mode|hash|filename\n")
            
            # Écrire chaque entrée
            for file_path, sha in index_data.items():
                # Mode (100644 pour les fichiers normaux)
                mode = 100644
                f.write(f"{mode}|{sha}|{file_path}\n")
                
    except Exception as e:
        print(f"Erreur lors de l'écriture de l'index: {e}")

def add_files(paths):
    """Ajouter des fichiers à l'index (staging area)"""
    from .objects import hash_object
    
    index = read_index()
    files_to_add = []
    gitignore_patterns = read_gitignore()

    # Collecter tous les fichiers à ajouter
    for path in paths:
        if os.path.isfile(path):
            files_to_add.append(path)
        elif os.path.isdir(path):
            # Parcourir récursivement le dossier
            for root, dirs, files in os.walk(path):
                # Ignorer les dossiers .git et .mon_git
                dirs[:] = [d for d in dirs if d not in ['.git', '.mon_git']]
                for file in files:
                    full_path = os.path.join(root, file)
                    files_to_add.append(full_path)
        else:
            print(f"Erreur : '{path}' n'est ni un fichier ni un dossier")
            continue

    # Filtrer les fichiers ignorés
    files_to_add = filter_ignored_files(files_to_add, gitignore_patterns)

    # Traiter chaque fichier
    for file_path in files_to_add:
        relative_path = os.path.relpath(file_path, start=os.getcwd())
        
        # Vérifier si le fichier est déjà dans l'index
        if relative_path in index:
            print(f"Déjà ajouté : {relative_path}")
            continue

        # Calculer le hash et ajouter à l'index
        try:
            sha = hash_object(file_path, write=True)
            if sha:
                index[relative_path] = sha
                print(f"Ajouté : {relative_path}")
            else:
                print(f"Erreur lors de l'ajout de : {relative_path}")
        except Exception as e:
            print(f"Erreur avec {relative_path}: {e}")

    # Sauvegarder l'index mis à jour
    write_index(index)
    print(f"Index mis à jour avec {len(files_to_add)} fichier(s)")

def ls_files(verbose=False):
    """Lister les fichiers dans l'index"""
    index = read_index()
    
    if not index:
        print("Aucun fichier dans l'index")
        return
    
    for file_path in sorted(index.keys()):
        if verbose:
            print(f"{index[file_path]} {file_path}")
        else:
            print(file_path) 