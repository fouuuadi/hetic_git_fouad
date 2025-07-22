# write_tree.py` pour implémenter la création d'arbres Git en utilisant la fonction
# create_tree de objects.py.

from git_scratch import create_tree

if __name__ == "__main__":
    # Exemple d'utilisation de create_tree
    entries = [
        (b"100644", "file1.txt", "d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2"),
        (b"100644", "file2.txt", "e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3e3"),
    ]
    sha1 = create_tree(entries)
    if sha1:    
        print(f"SHA-1 de l'objet tree créé : {sha1}")
    else:
        print("Échec de la création de l'objet tree.")


# à utiliser pour créer un objet tree dans un dépôt Git 



