import sys
from git_scratch import init_repo, hash_object, cat_file, add
import status


def main():
    # Affichage de l'aide si aucune commande n'est fournie
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [<args>]")
        print("Commands:")
        print("  init [<directory>]")
        print("  hash-object <file>")
        print("  cat-file -t|-p <sha>")
        print("  add <file> [<file>...]")
        print("  commit -m \"message\"")
        print("  rm [--cached] <file> [<file>...]")
        print("  log")
        print("  status")
        return

    command = sys.argv[1]

    if command == 'init':
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

    elif command == 'commit':
        if '-m' not in sys.argv:
            print("Usage: python main.py commit -m \"message\"")
            return
        msg_index = sys.argv.index('-m') + 1
        if msg_index >= len(sys.argv):
            print("Message de commit manquant.")
            return
        message = sys.argv[msg_index]
        from git_scratch import index_to_tree
        from objects import create_commit
        tree_sha1 = index_to_tree()
        commit_sha1 = create_commit(tree_sha1, message=message)
        if commit_sha1:
            print(f"Commit créé : {commit_sha1}")
        else:
            print("Erreur lors de la création du commit.")
    elif command == 'rm':
        if len(sys.argv) < 3:
            print("Usage: python main.py rm [--cached] <file> [<file>...]")
            return
        from git_scratch import rm
        cached = False
        files = sys.argv[2:]
        if files and files[0] == '--cached':
            cached = True
            files = files[1:]
        rm(files, cached=cached)
    elif command == 'log':
        from log import git_log
        git_log()
    elif command == 'status':
        # Nouvelle commande pour afficher l'état du dépôt
        status.git_status()

    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()