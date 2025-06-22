import sys
from git_scratch import init_repo, hash_object, cat_file, add

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py init [<directory>]")
        return

    command = sys.argv[1]

    if command == 'init':
        #j'utilise le répertoire passé en argument ou courant
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
            print("Usage: python main.py rm [--cached] <test.txt> [<test.txt>...]")
            return
        from git_scratch import rm
        cached = False
        files = sys.argv[2:]
        if files[0] == '--cached':
            cached = True
            files = files[1:]
        rm(files, cached=cached)
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()