# fichier : bonjour_argparse.py

# On importe le module argparse pour gérer les arguments depuis la ligne de commande
import argparse

# On crée un analyseur d'arguments avec une description qui s'affiche avec --help
parser = argparse.ArgumentParser(description="Script qui salue une personne")

# On ajoute un argument obligatoire : 'nom', que l'utilisateur devra fournir
parser.add_argument("nom", help="Le nom de la personne à saluer")

# On peut aussi ajouter un argument optionnel qui accepte plusieurs valeurs
#parser.add_argument("nom", nargs='+', help="Le nom de la personne à saluer")


# On analyse les arguments fournis par l'utilisateur
args = parser.parse_args()

# On affiche un message personnalisé en utilisant la valeur de l'argument 'nom'
print(f"Bonjour, {args.nom} !")

# On peut aussi permettre à 'nom' d'accepter plusieurs valeurs
print(f"Bonjour, {' '.join(args.nom)} !")




