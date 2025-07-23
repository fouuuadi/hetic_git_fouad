import os

GIT_DIR = ".git"

def git_show_ref():
    """
    Parcourt le dossier .git/refs et le fichier packed-refs pour
    afficher chaque référence sous la forme "<sha> <refname>".
    """
    refs = []

    #Dossiers sous .git/refs (heads, tags, remotes...)
    refs_dir = os.path.join(GIT_DIR, "refs")
    for root, dirs, files in os.walk(refs_dir):
        for fname in files:
            ref_path = os.path.join(root, fname)
            try:
                sha = open(ref_path, "r").read().strip()
            except IOError:
                continue
            # nom de la ref relative à .git, par ex. "refs/heads/main"
            refname = os.path.relpath(ref_path, GIT_DIR).replace(os.sep, "/")
            refs.append((sha, refname))

    #Fichier packed-refs
    packed = os.path.join(GIT_DIR, "packed-refs")
    if os.path.exists(packed):
        with open(packed, "r") as f:
            for line in f:
                line = line.strip()
                # ignorer commentaires et lignes de peeling (^...)
                if not line or line.startswith("#") or line.startswith("^"):
                    continue
                parts = line.split()
                if len(parts) == 2:
                    sha, refname = parts
                    refs.append((sha, refname))

    #Affichage trié par nom de ref
    for sha, refname in sorted(refs, key=lambda x: x[1]):
        print(f"{sha} {refname}")

if __name__ == "__main__":
    git_show_ref()
