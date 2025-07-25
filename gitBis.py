import argparse
from src.commands.hash_object import hash_object_git
from src.commands.init import init
from src.commands.add import add_files, ls_files, read_index
from src.commands.status import git_status
from src.commands.objects import cat_file, write_tree, create_commit
from src.commands.gitignore import read_gitignore
from src.commands.rev_parse import rev_parse
from src.commands.show_ref import show_refs
from src.commands.log import show_log

def create_gitignore(pattern):
    """Crée ou met à jour le fichier .gitignore avec un pattern"""
    try:
        with open('.gitignore', 'a') as f:
            f.write(f"{pattern}\n")
        print(f"Pattern '{pattern}' ajouté au fichier .gitignore")
        return True
    except Exception as e:
        print(f"Erreur lors de la création/modification de .gitignore: {e}")
        return False

def index_to_tree():
    """Crée un tree à partir de l'index actuel"""
    index = read_index()
    if not index:
        print("Aucun fichier dans l'index. Utilisez 'gitBis add' d'abord.")
        return None
    
    # Créer les entrées pour le tree
    entries = []
    for file_path, sha in index.items():
        mode = 0o100644  # Mode pour un fichier normal
        entries.append((mode, file_path, sha))
    
    # Utiliser write_tree() qui crée un tree à partir des fichiers actuels
    return write_tree()

def commit_with_message(message):
    """Crée un commit avec un message (commande porcelain)"""
    # Créer un tree à partir de l'index
    tree_sha = index_to_tree()
    if not tree_sha:
        return None
    
    # Récupérer le commit parent actuel
    parent_sha = None
    try:
        with open('.mon_git/refs/heads/main.txt', 'r') as f:
            content = f.read().strip()
            if not content.startswith('#'):
                parent_sha = content
    except FileNotFoundError:
        pass
    
    # Créer le commit
    commit_sha = create_commit(tree_sha, message=message, parent_sha1=parent_sha)
    if commit_sha:
        print(f"Commit créé : {commit_sha}")
        
        # Mettre à jour HEAD et la branche
        try:
            # Mettre à jour la branche main
            with open('.mon_git/refs/heads/main.txt', 'w') as f:
                f.write(commit_sha)
            
            print(f"Branche main mise à jour vers {commit_sha[:7]}")
            return commit_sha
        except Exception as e:
            print(f"Erreur lors de la mise à jour de HEAD : {e}")
            return commit_sha
    else:
        print("Erreur lors de la création du commit.")
        return None

def main():
    parser = argparse.ArgumentParser(prog="gitBis", description="Mini Git en python", epilog="Merci d'utiliser gitBis !")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Commandes disponibles")

    # Sous-commande : init
    parser_init = subparsers.add_parser("init", help="Initialiser un nouveau dépôt Git")

    # Sous-commande : add
    parser_add = subparsers.add_parser("add", help="Ajouter des fichiers à l'index")
    parser_add.add_argument("files", nargs="+", help="Fichiers à ajouter")

    # Sous-commande : ls-files
    parser_ls_files = subparsers.add_parser("ls-files", help="Lister les fichiers dans l'index")
    parser_ls_files.add_argument("-v", "--verbose", action="store_true", help="Afficher les hashes")

    # Sous-commande : status
    parser_status = subparsers.add_parser("status", help="Afficher l'état du dépôt")

    # Sous-commande : gitignore
    parser_gitignore = subparsers.add_parser("gitignore", help="Gérer les fichiers .gitignore")
    parser_gitignore.add_argument("pattern", help="Pattern à ajouter au fichier .gitignore")

    # Sous-commande : commit
    parser_commit = subparsers.add_parser("commit", help="Créer un commit avec message")
    parser_commit.add_argument("-m", "--message", required=True, help="Message du commit")

    # Sous-commande : cat-file
    parser_cat_file = subparsers.add_parser("cat-file", help="Afficher le contenu d'un objet Git")
    parser_cat_file.add_argument("sha", help="Hash de l'objet")
    parser_cat_file.add_argument("-t", action="store_true", help="Afficher le type de l'objet")
    parser_cat_file.add_argument("-p", action="store_true", help="Afficher le contenu de l'objet")

    # Sous-commande : write-tree
    parser_write_tree = subparsers.add_parser("write-tree", help="Créer un objet tree à partir de l'index")

    # Sous-commande : commit-tree
    parser_commit_tree = subparsers.add_parser("commit-tree", help="Créer un objet commit à partir d'un tree")
    parser_commit_tree.add_argument("tree_sha", help="Hash du tree à committer")
    parser_commit_tree.add_argument("-m", "--message", required=True, help="Message du commit")
    parser_commit_tree.add_argument("-p", "--parent", help="Hash du commit parent")

    # Sous-commande : hash-object
    parser_hash = subparsers.add_parser("hash-object", help="Calculer le hash d'un fichier")
    parser_hash.add_argument("file", type=str, help="Le fichier à hacher")
    parser_hash.add_argument("-w", "--write", action="store_true", help="Écrire l'objet dans le dépôt Git")

    # Sous-commande : rev-parse
    parser_rev_parse = subparsers.add_parser("rev-parse", help="Convertir une référence en SHA-1")
    parser_rev_parse.add_argument("ref", help="Référence à résoudre (HEAD, nom de branche, SHA-1 partiel, etc.)")

    # Sous-commande : show-ref
    parser_show_ref = subparsers.add_parser("show-ref", help="Afficher les références du dépôt")
    parser_show_ref.add_argument("--heads", action="store_true", help="Afficher seulement les branches")
    parser_show_ref.add_argument("--tags", action="store_true", help="Afficher seulement les tags")

    # Sous-commande : log
    parser_log = subparsers.add_parser("log", help="Afficher l'historique des commits")
    parser_log.add_argument("--oneline", action="store_true", help="Afficher en format compact")
    parser_log.add_argument("-n", "--max-count", type=int, help="Limiter le nombre de commits")
    parser_log.add_argument("commit", nargs="?", default="HEAD", help="Commit de départ (par défaut: HEAD)")

    args = parser.parse_args()

    if args.command == "init":
        init()
    elif args.command == "add":
        add_files(args.files)
    elif args.command == "ls-files":
        ls_files(verbose=args.verbose)
    elif args.command == "status":
        git_status()
    elif args.command == "gitignore":
        create_gitignore(args.pattern)
    elif args.command == "commit":
        commit_with_message(args.message)
    elif args.command == "cat-file":
        try:
            if args.t:
                cat_file("-t", args.sha)
            elif args.p:
                cat_file("-p", args.sha)
            else:
                print("Erreur: Vous devez spécifier -t ou -p")
        except Exception as e:
            print(f"Erreur: {e}")
    elif args.command == "write-tree":
        try:
            result = write_tree()
            if result:
                # Ne pas afficher de message supplémentaire, juste le hash
                pass
            else:
                print("Erreur lors de la création du tree.")
        except Exception as e:
            print(f"Erreur: {e}")
    elif args.command == "commit-tree":
        try:
            result = create_commit(args.tree_sha, parent_sha1=args.parent, message=args.message)
            if result:
                # Ne pas afficher de message supplémentaire, juste le hash
                pass
            else:
                print("Erreur lors de la création du commit.")
        except Exception as e:
            print(f"Erreur: {e}")
    elif args.command == "hash-object":
        try:
            result = hash_object_git(args.file, write=args.write)
            if result:
                print(f"Hash SHA-1 de '{args.file}': {result}")
            else:
                print("Erreur lors du hash ou de l'écriture.")
        except Exception as e:
            print(f"Erreur: {e}")
    elif args.command == "rev-parse":
        try:
            result = rev_parse(args.ref)
            if result:
                print(result)
            else:
                print(f"fatal: ambiguous argument '{args.ref}': unknown revision or path not in the working tree.")
        except Exception as e:
            print(f"Erreur: {e}")
    elif args.command == "show-ref":
        try:
            show_refs(heads_only=args.heads, tags_only=args.tags)
        except Exception as e:
            print(f"Erreur: {e}")
    elif args.command == "log":
        try:
            show_log(start_ref=args.commit, oneline=args.oneline, max_count=args.max_count)
        except Exception as e:
            print(f"Erreur: {e}")
    else:
        print("Commande non reconnue. Utilisez --help pour voir les options disponibles.")

if __name__ == "__main__":
    main()
