import argparse
from src.commands.hash_object_cmd import handle_hash_object

parser = argparse.ArgumentParser(prog="gitBis", description="Mini Git en python", epilog="Merci d'utiliser gitBis !")
subparsers = parser.add_subparsers(dest="command", required=True, help="Commandes disponibles")

# Sous-commande : hash-object
parser_hash = subparsers.add_parser("hash-object", help="Calculer le hash d'un fichier")
parser_hash.add_argument("file", type=str, help="Le fichier à hacher")
parser_hash.add_argument("-w", "--write", action="store_true", help="Écrire l'objet dans le dépôt Git")

args = parser.parse_args()

if args.command == "hash-object":
    handle_hash_object(args)
else:
    print("Commande non reconnue. Utilisez --help pour voir les options disponibles.")
