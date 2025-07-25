# gestion du working directory (checkout, reset, etc.)
import os
from . import read_object, parse_tree


def checkout(ref, new_branch=False):
    head_path = os.path.join('.mon_git', 'HEAD')
    refs_heads = os.path.join('.mon_git', 'refs', 'heads')
    branch_path = os.path.join(refs_heads, ref)

    if new_branch:
        with open(head_path, 'r') as f:
            head_ref = f.read().strip()
        if head_ref.startswith('ref:'):
            current_branch = head_ref.split(' ')[1]
            with open(os.path.join('.mon_git', current_branch), 'r') as f:
                sha = f.read().strip()
        else:
            sha = head_ref
        with open(branch_path, 'w') as f:
            f.write(sha)
        with open(head_path, 'w') as f:
            f.write(f"ref: refs/heads/{ref}\n")
        print(f"Nouvelle branche '{ref}' créée et checkout.")
    else:
        if os.path.exists(branch_path):
            with open(branch_path, 'r') as f:
                sha = f.read().strip()
            with open(head_path, 'w') as f:
                f.write(f"ref: refs/heads/{ref}\n")
            print(f"Basculé sur la branche '{ref}'.")
        else:
            sha = ref
            with open(head_path, 'w') as f:
                f.write(f"{sha}\n")
            print(f"HEAD détaché à {sha}.")

    # Lecture du commit et du tree (aucune gestion d'erreur)
    commit_type, commit_content = read_object(sha)
    tree_sha = commit_content.decode().splitlines()[0].split()[1]
    obj_type, tree_content = read_object(tree_sha)
    files_dict = parse_tree(tree_content)

    # Suppression brutale du working dir (hors .mon_git)
    for fname in os.listdir('.'):
        if fname != '.mon_git':
            if os.path.isfile(fname):
                os.remove(fname)
            elif os.path.isdir(fname):
                import shutil
                shutil.rmtree(fname)

    # Restauration des fichiers du tree
    for path, blob_sha in files_dict.items():
        obj_type, content = read_object(blob_sha)
        if os.path.dirname(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(content)
    print("Working directory mis à jour.")