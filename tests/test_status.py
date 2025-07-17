import os
import subprocess
import tempfile
import shutil

import pytest

CLI = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main.py'))

def run(cmd, cwd):
    """Exécute une commande shell et retourne (code, stdout)."""
    proc = subprocess.run(cmd, cwd=cwd, shell=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          universal_newlines=True)
    return proc.returncode, proc.stdout

@pytest.fixture
def repo(tmp_path):
    """Prépare un dépôt Git vierge dans un dossier temporaire."""
    d = tmp_path / "repo"
    d.mkdir()
    subprocess.run("git init", cwd=d, shell=True, check=True,
                   stdout=subprocess.DEVNULL)
    return str(d)

def test_status_clean(repo):
    code, out = run(f"python {CLI} status", repo)
    assert code == 0
    assert "Sur la branche" in out
    assert "Modifications prêtes" not in out
    assert "Modifications non indexées" not in out
    assert "Fichiers non suivis" not in out

def test_status_staged_unstaged_untracked(repo):
    (tmp := os.path.join(repo, "a.txt"))
    with open(tmp, "w") as f: f.write("foo")
    subprocess.run("git add a.txt", cwd=repo, shell=True, check=True)
    subprocess.run("git commit -m 'init'", cwd=repo, shell=True, check=True)

    with open(os.path.join(repo, "b.txt"), "w") as f: f.write("bar")
    subprocess.run("python {0} add b.txt".format(CLI), cwd=repo, shell=True, check=True)
    with open(os.path.join(repo, "a.txt"), "a") as f: f.write("\nmod")
    os.remove(os.path.join(repo, "a.txt"))

    code, out = run(f"python {CLI} status", repo)
    assert code == 0
    assert "nouveau fichier" in out
    assert "supprimé" in out
    assert "Fichiers non suivis" not in out