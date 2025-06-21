import sys

# On vérifie s'il y a un argument après le nom du script
if len(sys.argv) > 1:
    nom = sys.argv[1]
    print(f"Bonjour, {nom} !")
else:
    print("Bonjour, inconnu !")



#J'ai cree ce script pour tester le fonctionnement de l'argument de ligne de commande.
# Il affiche un message de bienvenue avec le nom passé en argument.
# Si aucun nom n'est passé, il affiche un message générique.
# Pour l'utiliser, exécutez-le avec un nom en argument :
# python ou python3 bonjour.py Alice