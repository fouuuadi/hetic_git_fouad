# objects.py

## Gestion des objets Git (blobs, trees, commits)

import hashlib
import os
import zlib
import argparse
import struct


def get_git_dir():
    """
    Retourne toujours le répertoire Git .mon_git.
    """
    return '.mon_git'

# Utilisation de la fonction de détection automatique
GIT_DIR = get_git_dir()

def hash_object(file_path, write=True):
    """
    Calcule le hash SHA-1 d'un fichier et optionnellement l'écrit dans .mon_git/objects.
    
    IMPACT SUR .MON_GIT :
    - Si write=True : Crée le dossier .mon_git/objects/<2_premiers_caracteres>/ et y écrit le fichier texte
    - Format : <type>|<taille>|<contenu> en format texte lisible
    - Structure : .mon_git/objects/ab/cdef1234...txt (ab = 2 premiers caractères du hash)
    
    Args:
        file_path (str): Chemin vers le fichier à hacher
        write (bool): Si True, écrit l'objet dans .mon_git/objects
    
    Returns:
        str: Hash SHA-1 de l'objet
    """
    if not os.path.isfile(file_path):
        raise ValueError(f"File not found: {file_path}")

    with open(file_path, 'rb') as f:
        content = f.read()

    header = f"blob {len(content)}\0".encode()
    store = header + content

    sha1 = hashlib.sha1(store).hexdigest()

    if write:
        git_dir = get_git_dir()
        object_path = os.path.join(git_dir, 'objects', sha1[:2], f"{sha1[2:]}.txt")
        dir_path = os.path.dirname(object_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(object_path, 'w') as f:
            f.write(f"# Git Object: {sha1}\n")
            f.write(f"# Type: blob\n")
            f.write(f"# Size: {len(content)}\n")
            f.write(f"blob|{len(content)}|\n")
            f.write(content.decode('utf-8', errors='replace'))

    print(sha1)
    return sha1

def read_object(sha):
    """
    Lit et décompresse un objet Git depuis .mon_git/objects.
    
    IMPACT SUR .MON_GIT :
    - Aucun impact (lecture seule)
    - Lit depuis .mon_git/objects/<2_premiers>/<reste_hash>.txt
    - Décompresse avec zlib et parse l'en-tête
    
    Args:
        sha (str): Hash SHA-1 de l'objet à lire
    
    Returns:
        tuple: (type_objet, contenu_decompressé)
    """
    git_dir = get_git_dir()
    path = os.path.join(git_dir, 'objects', sha[:2], f"{sha[2:]}.txt")
    if not os.path.exists(path):
        raise ValueError(f"Object {sha} not found.")

    with open(path, 'r') as f:
        content = f.read()
        
    # Le contenu est stocké en texte, on le décode
    try:
        # Supprimer les commentaires et lignes vides
        lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
        if not lines:
            raise ValueError(f"Object {sha} is empty or invalid.")
            
        # La première ligne contient l'en-tête
        header_line = lines[0]
        if '|' in header_line:
            obj_type, size = header_line.split('|')[:2]
            size = int(size)
            # Le reste du contenu
            content_data = '\n'.join(lines[1:]).encode('utf-8')
        else:
            # Format legacy
            null_index = content.find('\0')
            if null_index == -1:
                raise ValueError(f"Invalid object format for {sha}")
            header = content[:null_index]
            content_data = content[null_index+1:].encode('utf-8')
            obj_type, size = header.split()
            size = int(size)
            
        return obj_type, content_data
    except Exception as e:
        raise ValueError(f"Error reading object {sha}: {e}")

def cat_file(option, sha):
    """
    Affiche le type ou le contenu d'un objet Git (équivalent à git cat-file).
    
    IMPACT SUR .MON_GIT :
    - Aucun impact (lecture seule)
    - Utilise read_object() pour lire depuis .mon_git/objects
    
    Args:
        option (str): '-t' pour type, '-p' pour contenu
        sha (str): Hash SHA-1 de l'objet
    """
    obj_type, content = read_object(sha)

    if option == '-t':
        print(obj_type)
    elif option == '-p':
        if obj_type == 'blob':
            print(content.decode('utf-8', errors='replace'), end='')
        elif obj_type == 'tree':
            # Affichage formaté pour les objets tree
            i = 0
            while i < len(content):
                # Recherche de la fin du mode
                space_pos = content.find(b' ', i)
                if space_pos == -1:
                    break
                
                # Extraction du mode
                try:
                    mode = content[i:space_pos].decode('utf-8')
                except UnicodeDecodeError:
                    mode = content[i:space_pos].decode('utf-8', errors='replace')
                
                # Recherche de la fin du nom
                null_pos = content.find(b'\0', space_pos)
                if null_pos == -1:
                    break
                
                # Extraction du nom
                try:
                    name = content[space_pos+1:null_pos].decode('utf-8')
                except UnicodeDecodeError:
                    name = content[space_pos+1:null_pos].decode('utf-8', errors='replace')
                
                # Extraction du hash (20 bytes après le null)
                if null_pos + 21 > len(content):
                    break
                hash_bytes = content[null_pos+1:null_pos+21]
                hash_hex = hash_bytes.hex()
                
                # Détermination du type d'objet (blob ou tree)
                # Pour simplifier, on considère que les dossiers sont des trees
                # et les fichiers sont des blobs
                if mode.startswith('04'):  # Dossier
                    obj_type_str = 'tree'
                else:  # Fichier
                    obj_type_str = 'blob'
                
                # Affichage formaté
                print(f"{mode} {obj_type_str} {hash_hex}    {name}")
                
                # Passage à l'entrée suivante
                i = null_pos + 21
        elif obj_type == 'commit':
            print(content.decode('utf-8', errors='replace'), end='')
        else:
            print(f"Pretty print not supported yet for type {obj_type}")
    else:
        raise ValueError("Invalid option. Use -t or -p.")

def read_index():
    """
    Lit le fichier index Git (.mon_git/index.txt) et retourne la liste des fichiers indexés.
    
    IMPACT SUR .MON_GIT :
    - Aucun impact (lecture seule)
    - Lit le fichier texte .mon_git/index.txt
    - Parse les entrées selon le format texte
    
    Returns:
        list: Liste des tuples (mode, nom_fichier, hash_sha1) pour chaque fichier indexé
    """
    git_dir = get_git_dir()
    index_path = os.path.join(git_dir, 'index.txt')
    if not os.path.exists(index_path):
        return []
    
    entries = []
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
                            sha1 = parts[1]
                            filename = parts[2]
                            entries.append((mode, filename, sha1))
    except Exception as e:
        print(f"Erreur lors de la lecture de l'index: {e}")
        return []
    
    return entries

def write_tree():
    """
    Crée un objet tree à partir des fichiers du répertoire de travail.
    
    IMPACT SUR .MON_GIT :
    - Crée un nouvel objet tree dans .mon_git/objects/<2_premiers>/<reste_hash>.txt
    - Le tree représente l'état actuel des fichiers du répertoire
    - Format tree : <mode> <nom>\0<hash_binaire> pour chaque fichier
    - Structure : .mon_git/objects/ab/cdef1234...txt (ab = 2 premiers caractères du hash)
    
    Returns:
        str: Hash SHA-1 de l'objet tree créé
    """
    # Pour simplifier, on va créer un tree basé sur les fichiers actuels
    # plutôt que de lire l'index qui semble corrompu
    entries = []
    
    # Parcours des fichiers du répertoire de travail
    for root, dirs, files in os.walk('.'):
        # Ignorer .mon_git et .git
        if '.mon_git' in dirs:
            dirs.remove('.mon_git')
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            file_path = os.path.join(root, file)
            # Ignorer les fichiers cachés et les fichiers spéciaux
            if file.startswith('.') and file != '.gitignore':
                continue
            
            # Calculer le hash du fichier
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                header = f"blob {len(content)}\0".encode()
                store = header + content
                sha1 = hashlib.sha1(store).hexdigest()
                
                # Mode pour un fichier normal (100644)
                mode = 0o100644
                
                # Chemin relatif
                rel_path = os.path.relpath(file_path, '.')
                entries.append((mode, rel_path, sha1))
                
            except Exception as e:
                print(f"Erreur lors du traitement de {file_path}: {e}")
    
    # Création du contenu du tree (même vide)
    tree_content = b""
    for mode, name, sha1 in entries:
        # Conversion du mode en format octal (ex: 100644)
        mode_str = f"{mode:06o}"
        # Conversion du hash en bytes
        sha_bytes = bytes.fromhex(sha1)
        # Construction de l'entrée : mode nom\0hash
        entry = f"{mode_str} {name}\0".encode() + sha_bytes
        tree_content += entry
    
    # Calcul du hash du tree
    tree_hash = hashlib.sha1(tree_content).hexdigest()
    
    # Création de l'objet tree
    header = f"tree {len(tree_content)}\0".encode()
    store = header + tree_content
    
    # Écriture dans .mon_git/objects
    git_dir = get_git_dir()
    object_path = os.path.join(git_dir, 'objects', tree_hash[:2], f"{tree_hash[2:]}.txt")
    os.makedirs(os.path.dirname(object_path), exist_ok=True)
    
    with open(object_path, 'w') as f:
        f.write(f"# Git Object: {tree_hash}\n")
        f.write(f"# Type: tree\n")
        f.write(f"# Size: {len(tree_content)}\n")
        f.write(f"tree|{len(tree_content)}|\n")
        # Écrire les entrées en format lisible
        for mode, name, sha1 in entries:
            mode_str = f"{mode:06o}"
            f.write(f"{mode_str} {name} {sha1}\n")
    
    if not entries:
        print("Aucun fichier trouvé pour créer le tree.")
    
    print(tree_hash)
    return tree_hash

def create_tree(entries):
    """
    Crée un objet tree Git à partir d'une liste d'entrées (fichiers/sous-dossiers).
    
    IMPACT SUR .MON_GIT :
    - Crée un nouvel objet tree dans .mon_git/objects/<2_premiers>/<reste_hash>
    - Format tree : <mode> <nom>\0<hash_binaire> pour chaque entrée
    - Structure : .mon_git/objects/ab/cdef1234... (ab = 2 premiers caractères du hash)
    
    Args:
        entries (list): Liste de tuples (mode, nom, hash) pour chaque fichier/dossier
    
    Returns:
        str: Hash SHA-1 de l'objet tree créé
    """
    tree_content = b""
    for mode, name, sha in entries:
        mode_str = mode.decode() if isinstance(mode, bytes) else mode
        # SHA doit être binaire, pas texte
        sha_bytes = bytes.fromhex(sha)
        tree_content += f"{mode_str} {name}\0".encode() + sha_bytes
    sha1 = hashlib.sha1(tree_content).hexdigest()
    store = f"tree {len(tree_content)}\0".encode() + tree_content
    object_path = os.path.join(GIT_DIR, 'objects', sha1[:2], sha1[2:])
    os.makedirs(os.path.dirname(object_path), exist_ok=True)
    with open(object_path, 'wb') as f:
        f.write(zlib.compress(store))
    return sha1

def parse_tree(tree_content):
    """
    Parse le contenu d'un objet tree Git pour extraire les informations des fichiers.
    
    IMPACT SUR .MON_GIT :
    - Aucun impact (fonction utilitaire pour parser le contenu)
    
    Args:
        tree_content (bytes): Contenu brut d'un objet tree
    
    Returns:
        dict: Dictionnaire {nom_fichier: hash_sha1} pour chaque entrée
    """
    files = {}
    i = 0
    while i < len(tree_content):
        mode_end = tree_content.find(b' ', i)
        name_end = tree_content.find(b'\0', mode_end)
        mode = tree_content[i:mode_end]
        name = tree_content[mode_end+1:name_end].decode()
        sha = tree_content[name_end+1:name_end+21].hex()
        files[name] = sha
        i = name_end + 21
    return files

def create_commit(tree_sha1, parent_sha1=None, parent_sha2=None, message="Initial commit"):
    """
    Crée un objet commit Git avec les métadonnées appropriées.
    
    IMPACT SUR .MON_GIT :
    - Crée un nouvel objet commit dans .mon_git/objects/<2_premiers>/<reste_hash>.txt
    - Format commit : tree <hash_tree>\nparent <hash_parent>\n\n<message>
    - Structure : .mon_git/objects/ab/cdef1234...txt (ab = 2 premiers caractères du hash)
    - Le commit référence un tree et optionnellement un ou deux parents
    - Vérifie que le tree existe avant de créer le commit
    
    Args:
        tree_sha1 (str): Hash du tree à référencer
        parent_sha1 (str, optional): Hash du premier commit parent
        parent_sha2 (str, optional): Hash du deuxième commit parent (pour les merges)
        message (str): Message du commit
    
    Returns:
        str: Hash SHA-1 de l'objet commit créé
    """
    import getpass, time
    
    git_dir = get_git_dir()
    
    # Vérification que le tree existe
    tree_path = os.path.join(git_dir, 'objects', tree_sha1[:2], f"{tree_sha1[2:]}.txt")
    if not os.path.exists(tree_path):
        raise ValueError(f"Tree {tree_sha1} not found. Use 'gitBis write-tree' first.")
    
    # Vérification que les parents existent si spécifiés
    if parent_sha1:
        parent_path = os.path.join(git_dir, 'objects', parent_sha1[:2], f"{parent_sha1[2:]}.txt")
        if not os.path.exists(parent_path):
            raise ValueError(f"Parent commit {parent_sha1} not found.")
    
    if parent_sha2:
        parent_path = os.path.join(git_dir, 'objects', parent_sha2[:2], f"{parent_sha2[2:]}.txt")
        if not os.path.exists(parent_path):
            raise ValueError(f"Parent commit {parent_sha2} not found.")
    
    # Récupération des informations d'auteur
    author = getpass.getuser()
    date = int(time.time())
    
    # Construction du contenu du commit
    commit_lines = [f"tree {tree_sha1}"]
    
    if parent_sha1:
        commit_lines.append(f"parent {parent_sha1}")
    
    if parent_sha2:
        commit_lines.append(f"parent {parent_sha2}")
    
    commit_lines.extend(["", message])
    commit_content = "\n".join(commit_lines).encode()

    # Création de l'objet commit
    store = f"commit {len(commit_content)}".encode() + b'\x00' + commit_content
    sha1 = hashlib.sha1(store).hexdigest()
    
    # Écriture dans .mon_git/objects
    object_path = os.path.join(git_dir, 'objects', sha1[:2], f"{sha1[2:]}.txt")
    os.makedirs(os.path.dirname(object_path), exist_ok=True)
    
    with open(object_path, 'w') as f:
        f.write(f"# Git Object: {sha1}\n")
        f.write(f"# Type: commit\n")
        f.write(f"# Size: {len(commit_content)}\n")
        f.write(f"commit|{len(commit_content)}|\n")
        f.write(f"tree {tree_sha1}\n")
        if parent_sha1:
            f.write(f"parent {parent_sha1}\n")
        if parent_sha2:
            f.write(f"parent {parent_sha2}\n")
        f.write(f"\n{message}\n")
    
    print(sha1)
    return sha1


## Test de la fonction hash_object, create_tree et create_commit
if __name__ == "__main__":
    data = b"Hello, Git!"
    
    sha1 = hash_object(data)
    
    print(f"SHA-1 de l'objet créé : {sha1}")
    
    entries = [
        (b"100644", "file1.txt", hash_object(b"Contenu du fichier 1")),
        (b"100644", "file2.txt", hash_object(b"Contenu du fichier 2")),
        (b"40000", "dir1", create_tree([(b"100644", "file3.txt", hash_object(b"Contenu du fichier 3"))]))
    ]

    tree_sha1 = create_tree(entries)    

    print(f"SHA-1 de l'arbre créé : {tree_sha1}")

    # Ajout d'un parser : le stockage de l'objet Git se fait seulement avec l'option -w/--write

    parser = argparse.ArgumentParser(description="Hash and optionally store a Git object.")
    parser.add_argument("file", help="File to hash")
    parser.add_argument("-t", "--type", default="blob", help="Type of Git object (default: blob)")
    parser.add_argument("-w", "--write", action="store_true", help="Actually write the object into .mon_git/objects")

    args = parser.parse_args()

    # Lecture du fichier
    with open(args.file, "rb") as f:
        data = f.read()

    # Hash et (optionnellement) écriture
    sha1 = hash_object(data, type_=args.type, write=args.write)
    print(sha1)

    
    # Vérification du stockage de l'objet blob
    blob_obj_path = os.path.join(GIT_DIR, "objects", sha1[:2], sha1[2:])
    if os.path.exists(blob_obj_path):
        print(f"Objet blob stocké correctement à {blob_obj_path}")
    else:
        print("L'objet blob n'a pas été stocké correctement.")

    # Vérification du stockage de l'arbre
    tree_obj_path = os.path.join(GIT_DIR, "objects", tree_sha1[:2], tree_sha1[2:])
    if os.path.exists(tree_obj_path):
        print(f"Arbre stocké correctement à {tree_obj_path}")
    else:
        print("L'arbre n'a pas été stocké correctement.")

    # Test de la création d'un commit avec parent
    parent_commit_sha1 = create_commit(tree_sha1, message="Parent commit")
    commit_with_parent_sha1 = create_commit(tree_sha1, parent_sha1=parent_commit_sha1, message="Troisième commit avec parent")
    print(f"SHA-1 du commit avec parent créé : {commit_with_parent_sha1}")
    commit_with_parent_obj_path = os.path.join(GIT_DIR, "objects", commit_with_parent_sha1[:2], commit_with_parent_sha1[2:])
    if os.path.exists(commit_with_parent_obj_path):
        print(f"Objet commit avec parent stocké correctement à {commit_with_parent_obj_path}")
    else:
        print("L'objet commit avec parent n'a pas été stocké correctement.")
    # Test de la création d'un commit sans parent
    commit_without_parent_sha1 = create_commit(tree_sha1, message="Premier commit sans parent")
    print(f"SHA-1 du commit sans parent créé : {commit_without_parent_sha1}")
    commit_without_parent_obj_path = os.path.join(GIT_DIR, "objects", commit_without_parent_sha1[:2], commit_without_parent_sha1[2:])   
    if os.path.exists(commit_without_parent_obj_path):
        print(f"Objet commit sans parent stocké correctement à {commit_without_parent_obj_path}")
    else:
        print("L'objet commit sans parent n'a pas été stocké correctement.")


