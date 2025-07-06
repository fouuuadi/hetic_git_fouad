# objects.py

## Gestion des objets et trees Git

import hashlib
import os
import zlib
import argparse
import time
import getpass


GIT_DIR = ".git"

def hash_object(data, type_="blob", write=True):
    try:
        header = f"{type_} {len(data)}".encode()
        full_data = header + b'\x00' + data

        sha1 = hashlib.sha1(full_data).hexdigest()

        if write:
            obj_dir = os.path.join(GIT_DIR, "objects", sha1[:2])
            obj_path = os.path.join(obj_dir, sha1[2:])

            if not os.access(GIT_DIR, os.W_OK):
                raise PermissionError(f"Pas les droits d'écriture dans le dossier {GIT_DIR}")
            
            # Création du répertoire si besoin
            os.makedirs(obj_dir, exist_ok=True)

            compressed = zlib.compress(full_data)
            with open(obj_path, "wb") as f:
                f.write(compressed)

        return sha1

    except PermissionError as e:
        print(f"Erreur de permission : {e}")
        return None
    except OSError as e:
        print(f"Erreur lors de l'écriture de l'objet : {e}")
        return None
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return None


def create_tree(entries):

    tree_content = b"".join(f"{mode} {name}\0{sha}\n".encode() for mode, name, sha in entries)
    
    sha1 = hashlib.sha1(tree_content).hexdigest()
    
    compressed = zlib.compress(f"tree {len(tree_content)}\0".encode() + tree_content)
    
    obj_dir = os.path.join(GIT_DIR, "objects", sha1[:2])
    obj_path = os.path.join(obj_dir, sha1[2:])
    
    os.makedirs(obj_dir, exist_ok=True)
    
    with open(obj_path, "wb") as f:
        f.write(compressed)
    
    return sha1

# implémenter la fonction `create_commit` dans `objects.py` pour générer un objet commit, puis l'appeler dans un fichier `commit.py`. 
def create_commit(tree_sha1, parent_sha1=None, message="Initial commit"):
    author = getpass.getuser()
    date = int(time.time())
    try:
        if parent_sha1:
            commit_content = f"tree {tree_sha1}\nparent {parent_sha1}\n\n{message}".encode()
        else:
            commit_content = f"tree {tree_sha1}\n\n{message}".encode()
        header = f"commit {len(commit_content)}".encode()
        full_data = header + b'\x00' + commit_content
        sha1 = hashlib.sha1(full_data).hexdigest()
        compressed = zlib.compress(full_data)
        
        obj_dir = os.path.join(GIT_DIR, "objects", sha1[:2])
        obj_path = os.path.join(obj_dir, sha1[2:])
        os.makedirs(obj_dir, exist_ok=True)
        with open(obj_path, "wb") as f:
            f.write(compressed)

        return sha1
    except PermissionError as e:
        print(f"Erreur de permission : {e}")
        return None
    except OSError as e:
        print(f"Erreur lors de l'écriture de l'objet commit : {e}")
        return None
    
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return None



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
    parser.add_argument("-w", "--write", action="store_true", help="Actually write the object into .git/objects")

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


