import argparse
from src.commands.hash_object import hash_object_git
from src.commands.init import init
from src.commands.add import add_files, ls_files
from src.commands.status import git_status
from src.commands.objects import cat_file, write_tree, create_commit
from src.commands.gitignore import read_gitignore

def create_gitignore(pattern):
    """Crée ou met à jour le fichier .gitignore avec un pattern"""
    try:
        with open('.gitignore', 'a') as f:
            f.write(f"{pattern}\n")
        print(f"Pattern '{pattern}' ajouté au fichier .gitignore")
        return True
    except Exception as e:
        print(f"Erreur lors de la création/modification de .gitignore: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(prog="gitBis", description="Mini Git en python", epilog="Merci d'utiliser gitBis !")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Commandes disponibles")

    # Sous-commande : init
    parser_init = subparsers.add_parser("init", help="Initialiser un nouveau dépôt Git")

    # Sous-commande : add
    parser_add = subparsers.add_parser("add", help="Ajouter des fichiers à l'index")
    parser_add.add_argument("files", nargs="+", help="Fichiers à ajouter")

    # Sous-commande : ls-files
    parser_ls_files = subparsers.add_parser("ls-files", help="Lister les fichiers dans l'index")
    parser_ls_files.add_argument("-v", "--verbose", action="store_true", help="Afficher les hashes")

    # Sous-commande : status
    parser_status = subparsers.add_parser("status", help="Afficher l'état du dépôt")

    # Sous-commande : gitignore
    parser_gitignore = subparsers.add_parser("gitignore", help="Gérer les fichiers .gitignore")
    parser_gitignore.add_argument("pattern", help="Pattern à ajouter au fichier .gitignore")

    # Sous-commande : cat-file
    parser_cat_file = subparsers.add_parser("cat-file", help="Afficher le contenu d'un objet Git")
    parser_cat_file.add_argument("sha", help="Hash de l'objet")
    parser_cat_file.add_argument("-t", action="store_true", help="Afficher le type de l'objet")
    parser_cat_file.add_argument("-p", action="store_true", help="Afficher le contenu de l'objet")

    # Sous-commande : write-tree
    parser_write_tree = subparsers.add_parser("write-tree", help="Créer un objet tree à partir de l'index")

    # Sous-commande : commit-tree
    parser_commit_tree = subparsers.add_parser("commit-tree", help="Créer un objet commit à partir d'un tree")
    parser_commit_tree.add_argument("tree_sha", help="Hash du tree à committer")
    parser_commit_tree.add_argument("-m", "--message", required=True, help="Message du commit")
    parser_commit_tree.add_argument("-p", "--parent", help="Hash du commit parent")

    # Sous-commande : hash-object
    parser_hash = subparsers.add_parser("hash-object", help="Calculer le hash d'un fichier")
    parser_hash.add_argument("file", type=str, help="Le fichier à hacher")
    parser_hash.add_argument("-w", "--write", action="store_true", help="Écrire l'objet dans le dépôt Git")

    args = parser.parse_args()

    if args.command == "init":
        init()
    elif args.command == "add":
        add_files(args.files)
    elif args.command == "ls-files":
        ls_files(verbose=args.verbose)
    elif args.command == "status":
        git_status()
    elif args.command == "gitignore":
        create_gitignore(args.pattern)
    elif args.command == "cat-file":
        try:
            if args.t:
                cat_file("-t", args.sha)
            elif args.p:
                cat_file("-p", args.sha)
            else:
                print("Erreur: Vous devez spécifier -t ou -p")
        except Exception as e:
            print(f"Erreur: {e}")
    elif args.command == "write-tree":
        try:
            result = write_tree()
            if result:
                # Ne pas afficher de message supplémentaire, juste le hash
                pass
            else:
                print("Erreur lors de la création du tree.")
        except Exception as e:
            print(f"Erreur: {e}")
    elif args.command == "commit-tree":
        try:
            result = create_commit(args.tree_sha, parent_sha1=args.parent, message=args.message)
            if result:
                # Ne pas afficher de message supplémentaire, juste le hash
                pass
            else:
                print("Erreur lors de la création du commit.")
        except Exception as e:
            print(f"Erreur: {e}")
    elif args.command == "hash-object":
        try:
            result = hash_object_git(args.file, write=args.write)
            if result:
                print(f"Hash SHA-1 de '{args.file}': {result}")
            else:
                print("Erreur lors du hash ou de l'écriture.")
        except Exception as e:
            print(f"Erreur: {e}")
    else:
        print("Commande non reconnue. Utilisez --help pour voir les options disponibles.")

if __name__ == "__main__":
    main()
