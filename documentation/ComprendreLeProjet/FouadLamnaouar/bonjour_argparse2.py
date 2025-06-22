# fichier : salutation.py

import argparse


#Quand on utilise les arguments "--age" est un argument optionnel, il n'est pas obligatoire de le fournir donc cela ne va pas faire crash ta commande.
#Quand on tulise "nom" est un argument positionnel, il est obligatoire de le fournir sinon le script va planter et afficher une erreur.

# Création du parser
parser = argparse.ArgumentParser(description="Script de salutation personnalisé")

# Argument positionnel (obligatoire)
parser.add_argument("nom", help="Le nom de la personne à saluer")

# Argument optionnel : âge
parser.add_argument("--age", type=int, help="Âge de la personne (facultatif)")

# Argument optionnel : langue de salutation
parser.add_argument("--langue", choices=["fr", "en"], default="fr", help="Langue de la salutation (fr/en)")

# Analyse des arguments
#👉 parser.parse_args() lit et analyse les arguments de la ligne de commande pour remplir args.
args = parser.parse_args()

# Construction du message
if args.langue == "fr":
    message = f"Bonjour, {args.nom} !"
elif args.langue == "en":
    message = f"Hello, {args.nom}!"

# Ajout de l'âge si fourni
if args.age:
    message += f" Vous avez {args.age} ans."

# Affichage du message final
print(message)

# Exemple d'utilisation :
# python bonjour_argparse2.py Alice --age 30 --langue en
# python bonjour_argparse2.py Bob --langue fr
# python bonjour_argparse2.py Charlie --age 25
# python bonjour_argparse2.py David
# python bonjour_argparse2.py Eve --langue en
# python bonjour_argparse2.py --help
# Affiche l'aide et les options disponibles
# python bonjour_argparse2.py --version
# Affiche la version du script si ajoutée


#python3 bonjour_argparse2.py "Fouad Lamnaouar" --age 28 --langue en