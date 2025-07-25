
# Cette fonction lit un objet Git (blob) à partir du répertoire `.mon_git/objects` 
# avec gestion des erreurs et vérification de la validité du SHA-1.
import os
import sys
import zlib

GIT_DIR = ".mon_git"

def cat_file(sha1):
    """
    Lit un objet Git à partir du répertoire .mon_git/objects et affiche son contenu.
    :param sha1: SHA-1 de l'objet Git à lire.
    """
    # Vérification de la longueur du SHA-1
    if len(sha1) != 40:
        print(f"Erreur : SHA-1 invalide '{sha1}'. Il doit contenir 40 caractères hexadécimaux.")
        return

    obj_dir = os.path.join(GIT_DIR, "objects", sha1[:2])
    obj_path = os.path.join(obj_dir, sha1[2:])

    if not os.path.exists(obj_path):
        print(f"Erreur : L'objet '{sha1}' n'existe pas.")
        return
    
    # Lecture du contenu de l'objet
    with open(obj_path, "rb") as f:
        compressed_data = f.read()

    decompressed_data = zlib.decompress(compressed_data)

    # Extraction du type et de la taille
    header, content = decompressed_data.split(b'\x00', 1)
    header_parts = header.split()
    if len(header_parts) != 2:
        print(f"Erreur : En-tête invalide pour l'objet '{sha1}'.")
        return  
    obj_type, size = header_parts
    size = int(size)

    # Affichage des informations de l'objet
    print(f"Type : {obj_type.decode('utf-8')}")
    print(f"Taille : {size} octets")
    print("Contenu :")

    if obj_type == b'blob':
        # Affichage du contenu d'un objet blob
        print(content.decode('utf-8', errors='replace'))
    elif obj_type == b'tree':
        # Affichage du contenu d'un objet tree
        entries = content.split(b'\x00')
        for entry in entries:
            if entry:
                parts = entry.split(b' ')
                if len(parts) >= 3:
                    mode = parts[0].decode('utf-8')
                    name = parts[1].decode('utf-8')
                    sha1 = parts[2].decode('utf-8')
                    print(f"{mode} {name} {sha1}")
                else:
                    print(f"Entrée invalide : {entry}")
    elif obj_type == b'commit':
        # Affichage du contenu d'un objet commit
        commit_info = content.decode('utf-8', errors='replace')
        print(commit_info)
    else:
        print(f"Type d'objet inconnu : {obj_type.decode('utf-8')}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python cat_file.py <SHA-1>")
        sys.exit(1)
    sha1 = sys.argv[1]
    cat_file(sha1)


    
