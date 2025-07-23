import os
import struct

INDEX_PATH = os.path.join('.mon_git', 'index')

def read_index():
    """Lire l'index binaire Git"""
    if not os.path.exists(INDEX_PATH):
        return {}
    
    index_data = {}
    try:
        with open(INDEX_PATH, 'rb') as f:
            # Lire tout le contenu
            content = f.read()
            
            # Vérifier la signature "DIRC"
            if content[0:4] != b'DIRC':
                print("Signature d'index invalide")
                return {}
            
            # Lire le nombre d'entrées (4 bytes après l'en-tête)
            num_entries = struct.unpack('>I', content[8:12])[0]
            
            # Pour l'instant, lire directement les données selon l'hexdump
            if num_entries > 0:
                # Mode (4 bytes) - offset 12
                mode = struct.unpack('>I', content[12:16])[0]
                # SHA1 (20 bytes) - offset 18
                sha = content[18:38].hex()
                # Flags (2 bytes) - offset 38
                flags = struct.unpack('>H', content[38:40])[0]
                # Nom du fichier - à partir de l'offset 40
                name_end = content.find(b'\0', 40)
                if name_end > 40:
                    file_path = content[40:name_end].decode('utf-8')
                    index_data[file_path] = sha
                
    except Exception as e:
        print(f"Erreur lors de la lecture de l'index: {e}")
        import traceback
        traceback.print_exc()
        return {}
    
    return index_data

def write_index(index_data):
    """Écrire l'index au format binaire Git"""
    try:
        with open(INDEX_PATH, 'wb') as f:
            # En-tête (12 bytes)
            # Signature "DIRC" (4 bytes)
            f.write(b'DIRC')
            # Version (4 bytes)
            f.write(struct.pack('>I', 2))
            # Nombre d'entrées (4 bytes)
            f.write(struct.pack('>I', len(index_data)))
            
            # Écrire chaque entrée
            for file_path, sha in index_data.items():
                # Mode (4 bytes) - 100644 pour les fichiers normaux
                f.write(struct.pack('>I', 100644))
                # SHA1 (20 bytes)
                f.write(bytes.fromhex(sha))
                # Flags (2 bytes)
                name_len = len(file_path)
                f.write(struct.pack('>H', name_len))
                # Nom du fichier + \0
                f.write(file_path.encode('utf-8') + b'\0')
                
                # Alignement sur 8 bytes
                entry_size = 62 + len(file_path) + 1
                padding = (8 - entry_size % 8) % 8
                if padding > 0:
                    f.write(b'\0' * padding)
                
    except Exception as e:
        print(f"Erreur lors de l'écriture de l'index: {e}")

def add_files(paths):
    """Ajouter des fichiers à l'index (staging area)"""
    from .hash_object import hash_object_git
    from .gitignore import read_gitignore, filter_ignored_files
    
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
            sha = hash_object_git(file_path, write=True)
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