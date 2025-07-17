import os
import hashlib
import re

GIT_DIR = ".git"


def read_head():
    # Lit .git/HEAD pour obtenir la référence (branche ou SHA)
    head_path = os.path.join(GIT_DIR, "HEAD")
    ref = open(head_path).read().strip()
    if ref.startswith("ref:"):
        # HEAD pointe vers une branche
        ref_path = ref.split()[1]
        ref_file = os.path.join(GIT_DIR, ref_path)
        try:
            return open(ref_file).read().strip()
        except FileNotFoundError:
            # Aucune validation encore : retourne le nom de la branche
            return ref_path.split('/')[-1]
    # HEAD détaché : retourne le SHA
    return ref


def hash_file(path):
    # Calcule le SHA-1 Git d'un fichier (blob)
    with open(path, "rb") as f:
        data = f.read()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def ls_tree(tree_sha):
    # Liste récursivement le contenu d'un arbre Git (tree)
    tree = {}
    output = os.popen(f"git --git-dir={GIT_DIR} ls-tree -r {tree_sha}").read().splitlines()
    for line in output:
        parts = line.split()
        sha = parts[2]
        path = parts[3]
        tree[path] = sha
    return tree


def git_status():
    # 1. Branche / HEAD
    head = read_head()
    print(f"Sur la branche {head[:7]}")

    # Si pas de commit (head non-SHA1 long), on arrête là
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        return

    # 2. Arbre de HEAD
    commit_info = os.popen(f"git --git-dir={GIT_DIR} cat-file -p {head}").read()
    tree_sha = [l.split()[1] for l in commit_info.splitlines() if l.startswith('tree')][0]
    head_tree = ls_tree(tree_sha)

    # 3. Fichiers du working tree
    work_files = []
    for root, dirs, files in os.walk('.'):
        # Ignorer le dossier .git
        dirs[:] = [d for d in dirs if d != GIT_DIR]
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, '.')
            # Uniformiser les séparateurs en '/'
            rel = rel.replace(os.sep, '/')
            work_files.append(rel)

    # 4. Détecter les nouveaux fichiers
    new_files = [f for f in work_files if f not in head_tree]
    # 5. Détecter les suppressions
    removed = [f for f in head_tree if f not in work_files]
    # 6. Détecter les modifications
    modified = [f for f in work_files
                if f in head_tree and hash_file(f) != head_tree[f]]

    # Affichage
    if new_files or modified:
        print("\nModifications prêtes à être validées :")
        for f in new_files:
            print(f"  nouveau fichier : {f}")
        for f in modified:
            print(f"  modifié         : {f}")

    if removed:
        print("\nModifications non indexées :")
        for f in removed:
            print(f"  supprimé        : {f}")


if __name__ == "__main__":
    git_status()