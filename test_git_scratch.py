import os
import shutil
import json
import tempfile

from git_scratch import init_repo, add, read_index

def test_add_single_file():
    with tempfile.TemporaryDirectory() as repo_dir:
        os.chdir(repo_dir)
        init_repo()

        #je rcrée un fichier test
        with open("hello.txt", "w") as f:
            f.write("Hello staging!")


        add(["hello.txt"])

        index = read_index()

        assert "hello.txt" in index
        assert len(index["hello.txt"]) == 40  
