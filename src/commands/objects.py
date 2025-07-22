# objects.py

## Gestion des objets Git (blobs, trees, commits)

import hashlib
import os
import zlib
import argparse


GIT_DIR = ".git"

def hash_object(file_path, write=True):
    if not os.path.isfile(file_path):
        raise ValueError(f"File not found: {file_path}")

    with open(file_path, 'rb') as f:
        content = f.read()

    header = f"blob {len(content)}\0".encode()
    store = header + content

    sha1 = hashlib.sha1(store).hexdigest()

    if write:
        object_path = os.path.join('.git', 'objects', sha1[:2], sha1[2:])
        dir_path = os.path.dirname(object_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(object_path, 'wb') as f:
            f.write(zlib.compress(store))

    print(sha1)
    return sha1

def read_object(sha):
    path = os.path.join('.git', 'objects', sha[:2], sha[2:])
    if not os.path.exists(path):
        raise ValueError(f"Object {sha} not found.")

    with open(path, 'rb') as f:
        compressed = f.read()
        decompressed = zlib.decompress(compressed)

    null_index = decompressed.index(b'\0')
    header = decompressed[:null_index]
    content = decompressed[null_index+1:]

    obj_type, size = header.decode().split()
    return obj_type, content

def cat_file(option, sha):
    obj_type, content = read_object(sha)

    if option == '-t':
        print(obj_type)
    elif option == '-p':
        if obj_type == 'blob':
            print(content.decode('utf-8', errors='replace'), end='')
        elif obj_type in ('commit', 'tree'):
            print(content.decode('utf-8', errors='replace'), end='')
        else:
            print(f"Pretty print not supported yet for type {obj_type}")
    else:
        raise ValueError("Invalid option. Use -t or -p.")

def create_tree(entries):
    tree_content = b""
    for mode, name, sha in entries:
        mode_str = mode.decode() if isinstance(mode, bytes) else mode
        # SHA doit être binaire, pas texte
        sha_bytes = bytes.fromhex(sha)
        tree_content += f"{mode_str} {name}\0".encode() + sha_bytes
    sha1 = hashlib.sha1(tree_content).hexdigest()
    store = f"tree {len(tree_content)}\0".encode() + tree_content
    object_path = os.path.join('.git', 'objects', sha1[:2], sha1[2:])
    os.makedirs(os.path.dirname(object_path), exist_ok=True)
    with open(object_path, 'wb') as f:
        f.write(zlib.compress(store))
    return sha1

def parse_tree(tree_content):
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

# implémenter la fonction `create_commit` dans `objects.py` pour générer un objet commit, puis l'appeler dans un fichier `commit.py`. 
def create_commit(tree_sha1, parent_sha1=None, message="Initial commit"):
    import getpass, time
    author = getpass.getuser()
    date = int(time.time())
    if parent_sha1:
        commit_content = f"tree {tree_sha1}\nparent {parent_sha1}\n\n{message}".encode()
    else:
        commit_content = f"tree {tree_sha1}\n\n{message}".encode()
    store = f"commit {len(commit_content)}".encode() + b'\x00' + commit_content
    sha1 = hashlib.sha1(store).hexdigest()
    object_path = os.path.join('.git', 'objects', sha1[:2], sha1[2:])
    os.makedirs(os.path.dirname(object_path), exist_ok=True)
    with open(object_path, 'wb') as f:
        f.write(zlib.compress(store))
    print("DEBUG commit_content:", commit_content)
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


