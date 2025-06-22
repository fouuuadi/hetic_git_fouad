import hashlib, zlib, os

def hash_object_git(file, write=False):
    try:
        with open(file, "rb") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Erreur : le fichier '{file}' est introuvable.")
        return None
    except PermissionError:
        print(f"Erreur : permissions insuffisantes pour lire '{file}'.")
        return None

    header = b"blob " + str(len(content)).encode() + b"\0"
    data = header + content

    sha1 = hashlib.sha1(data).hexdigest()
    compressed = zlib.compress(data)

    if write:
        if not os.path.isdir(".git"):
            print("Erreur : ce répertoire n'est pas un dépôt Git ('.git' manquant).")
            return None

        dir_path = os.path.join(".git", "objects", sha1[:2])
        file_path = os.path.join(dir_path, sha1[2:])
        try:
            os.makedirs(dir_path, exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(compressed)
        except Exception as e:
            print(f"Erreur lors de l'écriture : {e}")
            return None
    return sha1
