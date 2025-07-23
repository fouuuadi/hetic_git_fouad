import argparse
from src.commands.hash_object import hash_object_git
from src.commands.init import init
from src.commands.add import add_files, ls_files
from src.commands.status import git_status

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
