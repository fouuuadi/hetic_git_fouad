#commit.py

import argparse   
from objects import create_commit
def main():
    parser = argparse.ArgumentParser(description="Créer un commit Git.")
    parser.add_argument("tree_sha1", help="SHA-1 de l'arbre associé au commit")
    parser.add_argument("-p", "--parent", help="SHA-1 du commit parent (optionnel)")
    parser.add_argument("-m", "--message", required=True, help="Message du commit")
    args = parser.parse_args()

    # Création du commit
    commit_sha1 = create_commit(args.tree_sha1, parent_sha1=args.parent, message=args.message)
    if commit_sha1:
        print(f"Commit créé avec succès : {commit_sha1}")
    else:
        print("Échec de la création du commit.")


if __name__ == "__main__":
    main()

# Ce script permet de créer un commit Git en utilisant la fonction `create_commit` de `objects.py`.
