import os
import struct

def init():
    """
    Initialise un nouveau dépôt Git en créant la structure .mon_git.
    
    IMPACT SUR LE SYSTÈME :
    - Si .mon_git existe déjà : le supprime et en crée un nouveau
    - Si .mon_git n'existe pas : le crée
    - Crée le répertoire avec tous les sous-dossiers nécessaires
    - Crée les fichiers de configuration de base (HEAD.txt, config.txt, index.txt)
    - Initialise la branche main par défaut
    """
    git_dir = '.mon_git'
    
    # Si .mon_git existe déjà, le supprimer
    if os.path.exists(git_dir):
        import shutil
        shutil.rmtree(git_dir)
        print(f"Ancien dépôt {git_dir} supprimé.")
    
    # Création de la structure de base
    os.makedirs(git_dir, exist_ok=True)
    os.makedirs(os.path.join(git_dir, 'objects'), exist_ok=True)
    os.makedirs(os.path.join(git_dir, 'refs', 'heads'), exist_ok=True)
    os.makedirs(os.path.join(git_dir, 'refs', 'tags'), exist_ok=True)
    
    # Création du fichier HEAD.txt
    with open(os.path.join(git_dir, 'HEAD.txt'), 'w') as f:
        f.write('ref: refs/heads/main\n')
    
    # Création du fichier config.txt
    with open(os.path.join(git_dir, 'config.txt'), 'w') as f:
        f.write('[core]\n')
        f.write(f'\trepositoryformatversion = 0\n')
        f.write(f'\tfilemode = true\n')
        f.write(f'\tbare = false\n')
        f.write(f'\tlogallrefupdates = true\n')
        f.write(f'\tignorecase = true\n')
        f.write(f'\tprecomposeunicode = true\n')
    
    # Création du fichier index.txt (format texte au lieu de binaire)
    with open(os.path.join(git_dir, 'index.txt'), 'w') as f:
        f.write('# Git Index File\n')
        f.write('# Version: 2\n')
        f.write('# Number of entries: 0\n')
        f.write('# Format: mode|hash|filename\n')
    
    # Création de la branche main (vide pour l'instant)
    with open(os.path.join(git_dir, 'refs', 'heads', 'main.txt'), 'w') as f:
        f.write('# Branch main - no commits yet\n')
    
    print(f"Dépôt Git initialisé avec la structure {git_dir}")


if __name__ == "__main__":
    init()
    print("Vous pouvez maintenant utiliser ce dépôt Git pour stocker des objets.")
