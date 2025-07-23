# tests/test_show_ref.py

import os
import subprocess
import pytest
import re

# Chemin absolu vers votre CLI main.py
CLI = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main.py'))


def run(cmd, cwd):
    """Exécute une commande shell et retourne (returncode, stdout_lines)."""
    proc = subprocess.run(
        cmd, cwd=cwd, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    # Retourne le code et la sortie découpée en lignes
    return proc.returncode, proc.stdout.strip().splitlines()


@pytest.fixture

def repo(tmp_path):
    """Crée un dépôt Git temporaire pour les tests."""
    d = tmp_path / "repo"
    d.mkdir()
    subprocess.run("git init", cwd=d, shell=True, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return str(d)


def test_show_ref_empty(repo):
    # Aucune ref dans un dépôt fraîchement initialisé
    code, out = run(f"python {CLI} show-ref", repo)
    assert code == 0
    assert out == []


def test_show_ref_after_commit(repo):
    # Commit initial
    file_path = os.path.join(repo, "a.txt")
    with open(file_path, "w") as f:
        f.write("foo")
    subprocess.run("git add a.txt", cwd=repo, shell=True, check=True)
    subprocess.run("git commit -m \"init\"", cwd=repo, shell=True, check=True)

    code, out = run(f"python {CLI} show-ref", repo)
    assert code == 0
    # Doit lister exactement une ref de branche
    assert len(out) == 1
    sha, ref = out[0].split()
    assert re.fullmatch(r"[0-9a-f]{40}", sha)
    assert ref in ("refs/heads/master", "refs/heads/main")


def test_show_ref_with_tag(repo):
    # Commit de départ
    file_path = os.path.join(repo, "b.txt")
    with open(file_path, "w") as f:
        f.write("bar")
    subprocess.run("git add b.txt", cwd=repo, shell=True, check=True)
    subprocess.run("git commit -m \"second\"", cwd=repo, shell=True, check=True)

    # Création d'un tag annoté avec double-quotes pour compatibilité Windows
    subprocess.run("git tag -a v1.0 -m \"version 1.0\"", cwd=repo, shell=True, check=True)

    code, out = run(f"python {CLI} show-ref", repo)
    assert code == 0
    # On devrait voir au moins la branche et le tag
    refs = {line.split()[1] for line in out}
    assert any(r.startswith("refs/heads/") for r in refs)
    assert "refs/tags/v1.0" in refs
