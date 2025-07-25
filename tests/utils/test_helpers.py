"""
Utilitaires pour les tests unitaires de gitBis
"""

import os
import shutil
import tempfile
from contextlib import contextmanager


class TestRepo:
    """Classe pour gérer un dépôt de test temporaire"""
    
    def __init__(self):
        self.test_dir = None
        self.original_cwd = None
        self.git_dir = None
    
    def setup(self):
        """Créer un dépôt de test temporaire"""
        self.test_dir = tempfile.mkdtemp(prefix="gitbis_test_")
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Créer la structure .mon_git
        self.git_dir = os.path.join(self.test_dir, ".mon_git")
        os.makedirs(os.path.join(self.git_dir, "objects"), exist_ok=True)
        os.makedirs(os.path.join(self.git_dir, "refs", "heads"), exist_ok=True)
        
        # Créer HEAD.txt
        with open(os.path.join(self.git_dir, "HEAD.txt"), "w") as f:
            f.write("ref: refs/heads/main")
        
        # Créer la branche main
        with open(os.path.join(self.git_dir, "refs", "heads", "main.txt"), "w") as f:
            f.write("")
        
        return self.test_dir
    
    def cleanup(self):
        """Nettoyer le dépôt de test"""
        if self.test_dir and os.path.exists(self.test_dir):
            os.chdir(self.original_cwd)
            shutil.rmtree(self.test_dir)
    
    def create_file(self, filename, content=""):
        """Créer un fichier de test"""
        with open(filename, "w") as f:
            f.write(content)
        return filename
    
    def read_file(self, filename):
        """Lire le contenu d'un fichier"""
        with open(filename, "r") as f:
            return f.read()
    
    def file_exists(self, filename):
        """Vérifier si un fichier existe"""
        return os.path.exists(filename)


@contextmanager
def temp_repo():
    """Contexte manager pour un dépôt temporaire"""
    repo = TestRepo()
    try:
        repo.setup()
        yield repo
    finally:
        repo.cleanup()


def create_test_files(repo, files):
    """Créer plusieurs fichiers de test
    
    Args:
        repo: Instance de TestRepo
        files: Dict {filename: content}
    """
    created_files = []
    for filename, content in files.items():
        repo.create_file(filename, content)
        created_files.append(filename)
    return created_files


def assert_file_content(repo, filename, expected_content):
    """Assertion pour vérifier le contenu d'un fichier"""
    actual_content = repo.read_file(filename)
    assert actual_content == expected_content, f"Contenu attendu: {expected_content}, obtenu: {actual_content}"


def assert_file_exists(repo, filename):
    """Assertion pour vérifier qu'un fichier existe"""
    assert repo.file_exists(filename), f"Le fichier {filename} n'existe pas"


def assert_file_not_exists(repo, filename):
    """Assertion pour vérifier qu'un fichier n'existe pas"""
    assert not repo.file_exists(filename), f"Le fichier {filename} existe mais ne devrait pas" 