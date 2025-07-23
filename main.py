import sys
from git_scratch import init_repo, hash_object, cat_file, add, write_tree, ls_files, ls_tree

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <commande> [options]")
        return

    command = sys.argv[1]

    if command == 'init':
        # Utilise le répertoire passé en argument ou courant
        path = sys.argv[2] if len(sys.argv) > 2 else '.'
        init_repo(path)
    elif command == 'hash-object':
        if len(sys.argv) < 3:
            print("Usage: python main.py hash-object <file>")
            return
        file_path = sys.argv[2]
        hash_object(file_path)
    elif command == 'cat-file':
        if len(sys.argv) != 4:
            print("Usage: python main.py cat-file -t|-p <sha>")
            return
        option = sys.argv[2]
        sha = sys.argv[3]
        cat_file(option, sha)
    elif command == 'add':
        if len(sys.argv) < 3:
            print("Usage: python main.py add <file> [<file>...]")
            return
        add(sys.argv[2:])
    elif command == 'ls-tree':
        if len(sys.argv) != 3:
            print("Usage: python main.py ls-tree <sha>")
            return
        sha = sys.argv[2]
        ls_tree(sha)
    elif command == 'ls-files':
        ls_files()
    elif command == 'write-tree':
        write_tree()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()