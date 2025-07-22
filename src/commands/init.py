import os

GIT_DIR = ".mon_git"


def init():
    # Créer le dossier principal .mon_git
    os.makedirs(GIT_DIR, exist_ok=True)
    
    # Créer la structure des dossiers
    os.makedirs(os.path.join(GIT_DIR, "objects"), exist_ok=True)
    os.makedirs(os.path.join(GIT_DIR, "refs", "heads"), exist_ok=True)
    
    # Créer le fichier HEAD
    with open(os.path.join(GIT_DIR, "HEAD"), "w") as f:
        f.write("ref: refs/heads/main\n")
    
    # Créer le fichier config
    with open(os.path.join(GIT_DIR, "config"), "w") as f:
        f.write("[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n")
    
    # Créer le fichier index (staging area)
    with open(os.path.join(GIT_DIR, "index"), "w") as f:
        f.write("")  # Fichier vide pour commencer
    
    # Créer le fichier main dans refs/heads
    with open(os.path.join(GIT_DIR, "refs", "heads", "main"), "w") as f:
        f.write("")  # Fichier vide pour commencer
    
    print("Dépôt Git initialisé avec la structure .mon_git")


if __name__ == "__main__":
    init()
    print("Vous pouvez maintenant utiliser ce dépôt Git pour stocker des objets.")
