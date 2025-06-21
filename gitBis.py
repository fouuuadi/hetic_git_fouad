import argparse
from hashObjectGit import hashObjectGit

parser =  argparse.ArgumentParser(prog="gitBis", description="Mini Git en python", epilog="Merci d'utiliser gitBis !")
subparsers = parser.add_subparsers(dest="command", required=True, help="Commandes disponibles")


# Sous-commande :

parser_hash = subparsers.add_parser("hash-object", help="Calculer le hash d'un fichier")
parser_hash.add_argument("file", type=str, help="Le fichier à hacher")
parser_hash.add_argument("-w", "--write", action="store_true", help="Écrire l'objet dans le dépôt Git")

args = parser.parse_args()


if args.command == "hash-object":
    hash_result = hashObjectGit(args.file, write=args.write)
    if hash_result:
        print(f"Hash SHA-1 de '{args.file}': {hash_result}")
    else:
        print("Erreur lors du calcul du hash ou de l'écriture dans le dépôt Git.")
else:
    print("Commande non reconnue. Utilisez --help pour voir les options disponibles.")
# Si la commande n'est pas reconnue, le message d'erreur s'affiche.
# Pour exécuter ce script, utilisez la commande :
# python gitBis.py hash-object fichier.txt --write
# Ou pour juste calculer le hash sans écrire :
# python gitBis.py hash-object fichier.txt
