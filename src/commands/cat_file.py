
# Cette fonction lit un objet Git (blob) à partir du répertoire `.mon_git/objects` 
# avec gestion des erreurs et vérification de la validité du SHA-1.
import os
import sys
import zlib
import glob

GIT_DIR = ".mon_git"

def resolve_short_sha(short_sha):
    """
    Résout un SHA court en SHA complet
    
    Args:
        short_sha (str): SHA court (7+ caractères)
    
    Returns:
        str: SHA complet ou None si non trouvé
    """
    if len(short_sha) >= 40:
        return short_sha
    
    git_dir = get_git_dir()
    objects_dir = os.path.join(git_dir, "objects")
    
    # Chercher dans tous les sous-répertoires
    for subdir in os.listdir(objects_dir):
        subdir_path = os.path.join(objects_dir, subdir)
        if os.path.isdir(subdir_path) and len(subdir) == 2:
            # Chercher les fichiers qui commencent par le SHA court
            pattern = os.path.join(subdir_path, f"{short_sha[len(subdir):]}*")
            matches = glob.glob(pattern)
            if matches:
                # Extraire le nom du fichier (sans extension)
                filename = os.path.basename(matches[0])
                if filename.endswith('.txt'):
                    filename = filename[:-4]
                return subdir + filename
    
    return None

def get_git_dir():
    """Retourne le chemin du dossier .mon_git"""
    return ".mon_git"

def cat_file(sha1):
    """
    Lit un objet Git à partir du répertoire .mon_git/objects et affiche son contenu.
    :param sha1: SHA-1 de l'objet Git à lire.
    :return: True si succès, False si échec
    """
    try:
        # Résoudre le SHA court si nécessaire
        if len(sha1) < 40:
            resolved_sha = resolve_short_sha(sha1)
            if resolved_sha is None:
                print(f"Erreur : SHA-1 invalide '{sha1}'. Il doit contenir 40 caractères hexadécimaux.")
                return False
            sha1 = resolved_sha
        
        # Utiliser read_object de objects.py
        from src.commands.objects import read_object
        obj_type, content = read_object(sha1)
        
        # Affichage des informations de l'objet
        print(f"Type : {obj_type}")
        print(f"Taille : {len(content)} octets")
        print("Contenu :")

        if obj_type == 'blob':
            # Affichage du contenu d'un objet blob
            print(content.decode('utf-8', errors='replace'))
        elif obj_type == 'tree':
            # Affichage du contenu d'un objet tree
            if isinstance(content, bytes):
                content_str = content.decode('utf-8')
            else:
                content_str = content
            
            lines = content_str.strip().split('\n')
            for line in lines:
                if line.strip():
                    print(line)
        elif obj_type == 'commit':
            # Affichage du contenu d'un objet commit
            if isinstance(content, bytes):
                commit_info = content.decode('utf-8', errors='replace')
            else:
                commit_info = content
            print(commit_info)
        else:
            print(f"Type d'objet inconnu : {obj_type}")
        
        return True
    except Exception as e:
        print(f"Erreur : {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python cat_file.py <SHA-1>")
        sys.exit(1)
    sha1 = sys.argv[1]
    cat_file(sha1)


    
