# objects.py

## Gestion des objets et trees Git

import hashlib
import os
import zlib
import argparse


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

## Test de la fonction hash_object et de create_tree
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


# L'objet blob et l'arbre ont été correctement stockés dans le dépôt Git.
# Utilisation ultérieure :
# - Pour ajouter des fichiers, utiliser hash_object avec l'option --write.
# - Pour créer des arbres, utiliser create_tree avec les entrées appropriées.
# - Pour lire des objets, utiliser cat-file (à implémenter dans un futur module).
# - Pour gérer les commits, implémenter une fonction similaire pour les commits.
# - Pour gérer les références, implémenter une fonction pour écrire dans .git/refs/heads.
# - Pour gérer les tags, implémenter une fonction pour écrire dans .git/refs/tags.
# - Pour gérer les branches, implémenter une fonction pour lire et écrire dans .git/refs/heads.


# Donc cela fait partie des commandes dites de "plumbing" de Git ?
# Dans la suite il est indiqué de faire git cat-file, write-tree et commit-tree. Donc je commence par quoi maintenant ?
# Il est recommandé de commencer par implémenter la commande `git cat-file` pour lire les objets Git,
# car cela vous permettra de vérifier que les objets que vous avez créés sont corrects. 
# Ensuite, vous pouvez implémenter `write-tree` pour créer des arbres à partir des objets et
#  enfin `commit-tree` pour gérer les commits.
## Bien je viens de créer cat_file.py, quelle est la suite ?
# La suite consiste à implémenter la commande `git cat-file` pour lire les objets Git.
# Cette commande vous permettra de vérifier que les objets que vous avez créés sont corrects.
# Vous pouvez commencer par créer un fichier `cat_file.py` dans le même répertoire que `objects.py`.
