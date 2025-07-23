import os
import hashlib
import zlib
import json
import struct

INDEX_PATH = os.path.join('.git', 'index.json')

def init_repo(path='.'):
    git_dir = os.path.join(path, '.git')
    
    if os.path.exists(git_dir):
        print(f"Repository already initialized in {git_dir}")
        return

    #je crée la structure de dossier .git/
    os.makedirs(os.path.join(git_dir, 'objects'))
    os.makedirs(os.path.join(git_dir, 'refs', 'heads'))

    #je crée le fichier HEAD
    with open(os.path.join(git_dir, 'HEAD'), 'w') as f:
        f.write("ref: refs/heads/master\n")

    print(f"Initialized empty Git repository in {os.path.abspath(git_dir)}")


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
            print(content.decode('utf-8', errors='replace'), end='')  #affichage texte brut
        else:
            print(f"Pretty print not supported yet for type {obj_type}")
    else:
        raise ValueError("Invalid option. Use -t or -p.")


#commnd add
def read_index():
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, 'r') as f:
            return json.load(f)
    return {}

def write_index(index):
    with open(INDEX_PATH, 'w') as f:
        json.dump(index, f, indent=2)


def add(paths):
    index = read_index()
    files_to_add = []

    for path in paths:
        if os.path.isfile(path):
            files_to_add.append(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                if os.path.commonpath([root, '.git']) == '.git':
                    continue
                for file in files:
                    full_path = os.path.join(root, file)
                    files_to_add.append(full_path)
        else:
            print(f"Skipped (not a file or directory): {path}")
            continue

    for file_path in files_to_add:
        relative_path = os.path.relpath(file_path, start=os.getcwd())
        if relative_path in index:
            print(f"Skipped (already added): {relative_path}")
            continue

        sha = hash_object(file_path)
        index[file_path] = sha
        print(f"Added {file_path}")

    write_index(index)


#command git ls-tree

def ls_tree(sha):
    obj_type, content = read_object(sha)
    if obj_type != 'tree':
        raise ValueError(f"Object {sha} is not a tree.")

    i = 0
    while i < len(content):
        # Lire le mode (ex: 100644), suivi d’un espace
        space_index = content.index(b' ', i)
        mode = content[i:space_index].decode()
        i = space_index + 1

        # Lire le nom du fichier, suivi de \0
        null_index = content.index(b'\x00', i)
        name = content[i:null_index].decode()
        i = null_index + 1

        # Lire les 20 bytes du SHA-1 (binaire)
        sha_bin = content[i:i+20]
        sha_hex = sha_bin.hex()
        i += 20

        print(f"{mode} {sha_hex} {name}")






#comment ls-files
def ls_files(verbose=False):
    index = read_index()
    for file_path in sorted(index.keys()):
        if verbose:
            print(f"{index[file_path]} {file_path}")
        else:
            print(file_path)

#command write-tree
def write_tree():
    index = read_index()
    entries = []

    for path, sha in index.items():
        mode = '100644'  # On simplifie : tout est fichier normal
    
        path = path.replace(os.sep, '/')
        name = path.encode()
        sha_bytes = bytes.fromhex(sha)
        entry = f"{mode} ".encode() + name + b'\x00' + sha_bytes
        entries.append(entry)

    content = b''.join(entries)
    header = f"tree {len(content)}\0".encode()
    store = header + content

    sha1 = hashlib.sha1(store).hexdigest()

    # Sauvegarder dans .git/objects
    object_path = os.path.join('.git', 'objects', sha1[:2], sha1[2:])
    dir_path = os.path.dirname(object_path)
    os.makedirs(dir_path, exist_ok=True)

    with open(object_path, 'wb') as f:
        f.write(zlib.compress(store))

    print(sha1)
    return sha1