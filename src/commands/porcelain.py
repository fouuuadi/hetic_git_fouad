# commandes haut niveau (add, rm, commit, status, etc.)

import os


def init_repo(path='.'):
    git_dir = os.path.join(path, '.git')
    
    if os.path.exists(git_dir):
        print(f"Repository already initialized in {git_dir}")
        return

    #je crée la structure de dossier .git/
    os.makedirs(os.path.join(git_dir, 'objects'))
    os.makedirs(os.path.join(git_dir, 'refs', 'heads'))

    #je crée le fichier HEAD
    with open(os.path.join(git_dir, 'HEAD'), 'w') as f:
        f.write("ref: refs/heads/master\n")

    print(f"Initialized empty Git repository in {os.path.abspath(git_dir)}")
