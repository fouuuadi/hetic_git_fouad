import os
import shutil
import json
import tempfile
import io
from contextlib import redirect_stdout


from git_scratch import init_repo, add, read_index, ls_files, ls_tree, write_tree

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

def test_add_single_file():
    with tempfile.TemporaryDirectory() as repo:
        os.chdir(repo)
        init_repo()

        write_file("file1.txt", "hello")
        add(["file1.txt"])

        index = read_index()
        assert "file1.txt" in index
        assert len(index["file1.txt"]) == 40  # SHA-1

def test_add_directory_with_files():
    with tempfile.TemporaryDirectory() as repo:
        os.chdir(repo)
        init_repo()

        write_file("src/a.txt", "alpha")
        write_file("src/b.txt", "beta")
        add(["src"])

        index = read_index()
        assert "src/a.txt" in index
        assert "src/b.txt" in index

def test_ignore_dot_git_folder():
    with tempfile.TemporaryDirectory() as repo:
        os.chdir(repo)
        init_repo()

        # Simule un fichier dans .git (ce qui ne doit pas arriver)
        write_file(".git/fake.txt", "do not add")
        write_file("real.txt", "add me")
        add(["."])  # Ajoute tout

        index = read_index()
        assert "real.txt" in index
        assert ".git/fake.txt" not in index

def test_skip_already_added_files():
    with tempfile.TemporaryDirectory() as repo:
        os.chdir(repo)
        init_repo()

        write_file("repeat.txt", "once")
        add(["repeat.txt"])
        index1 = read_index()

        write_file("repeat.txt", "twice")  # change content, but add() should skip it
        add(["repeat.txt"])  # should skip, based on relpath in your code
        index2 = read_index()

        # Index should remain unchanged
        assert index1 == index2

def test_nested_directory_add():
    with tempfile.TemporaryDirectory() as repo:
        os.chdir(repo)
        init_repo()

        write_file("nested/dir/file.txt", "nested file")
        add(["nested"])

        index = read_index()
        assert "nested/dir/file.txt" in index




def test_ls_files_lists_added_files():
    with tempfile.TemporaryDirectory() as repo:
        os.chdir(repo)
        init_repo()

        write_file("a.txt", "a")
        write_file("b.txt", "b")
        add(["a.txt", "b.txt"])

        f = io.StringIO()
        with redirect_stdout(f):
            ls_files()

        output = f.getvalue().strip().splitlines()
        assert sorted(output) == ["a.txt", "b.txt"]



def test_ls_tree_lists_tree_contents():
    with tempfile.TemporaryDirectory() as repo:
        os.chdir(repo)
        init_repo()

        write_file("hello.txt", "world")
        write_file("src/code.py", "print('hi')")
        add(["."])

        tree_sha = write_tree()

        f = io.StringIO()
        with redirect_stdout(f):
            ls_tree(tree_sha)

        output = f.getvalue().strip().splitlines()

        # Vérifie que les lignes contiennent le bon format : "100644 <sha> <filename>"
        # Tu peux aussi parser et valider les noms
        assert any("hello.txt" in line for line in output)
        assert any("code.py" in line for line in output)
