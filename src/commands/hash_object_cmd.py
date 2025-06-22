from src.core.hash_object import hash_object_git

def handle_hash_object(args):
    result = hash_object_git(args.file, write=args.write)
    if result:
        print(f"Hash SHA-1 de '{args.file}': {result}")
    else:
        print("Erreur lors du hash ou de l'écriture.")
