import os

GIT_DIR = ".mon_git"


def init():
    os.makedirs(GIT_DIR, exist_ok=True)
    
    os.makedirs(os.path.join(GIT_DIR, "objects"), exist_ok=True)
    os.makedirs(os.path.join(GIT_DIR, "refs", "heads"), exist_ok=True)
    

    with open(os.path.join(GIT_DIR, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")
    
    with open(os.path.join(GIT_DIR, "config"), "w") as f:
        f.write("[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n")
    
    print("Dépôt Git initialisé.")


if __name__ == "__main__":
    init()
    print("Vous pouvez maintenant utiliser ce dépôt Git pour stocker des objets.")
