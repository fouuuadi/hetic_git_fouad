import hashlib
import zlib
import os

def hashObjectGit(file, write=False):
    try:
        with open(file, "rb") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Erreur : le fichier '{file}' est introuvable.")
        return None
    except PermissionError:
        print(f"Erreur : permissions insuffisantes pour lire '{file}'.")
        return None

    taille = len(content)
    header = b"blob " + str(taille).encode() + b"\0"
    data = header + content

    hash_sha1 = hashlib.sha1(data).hexdigest()
    compressed = zlib.compress(data)

    if write:
        if not os.path.isdir(".git"):
            print("Erreur : ce répertoire n'est pas un dépôt Git ('.git' manquant).")
            return None

        directory = hash_sha1[:2]
        filename = hash_sha1[2:]
        folder_path = os.path.join(".git", "objects", directory)
        full_path = os.path.join(folder_path, filename)

        try:
            os.makedirs(folder_path, exist_ok=True)
            with open(full_path, "wb") as f:
                f.write(compressed)
        except PermissionError:
            print(f"Erreur : permissions insuffisantes pour écrire dans '{folder_path}'.")
            return None
        except OSError as e:
            print(f"Erreur système : {e}")
            return None

    return hash_sha1

# Ce bloc ne s'exécute que si on lance directement ce fichier
if __name__ == "__main__":
    print(hashObjectGit("fichier.txt", write=True))
    print(hashObjectGit("fichier.txt", write=False))
