import argparse
from src.commands.hash_object import hash_object_git
from src.commands.init import init

def main():
    parser = argparse.ArgumentParser(prog="gitBis", description="Mini Git en python", epilog="Merci d'utiliser gitBis !")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Commandes disponibles")

    # Sous-commande : init
    parser_init = subparsers.add_parser("init", help="Initialiser un nouveau dépôt Git")

    # Sous-commande : hash-object
    parser_hash = subparsers.add_parser("hash-object", help="Calculer le hash d'un fichier")
    parser_hash.add_argument("file", type=str, help="Le fichier à hacher")
    parser_hash.add_argument("-w", "--write", action="store_true", help="Écrire l'objet dans le dépôt Git")

    args = parser.parse_args()

    if args.command == "init":
        init()
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
