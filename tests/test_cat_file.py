"""
Tests unitaires pour la commande cat-file
"""

import pytest
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.commands.cat_file import cat_file
from src.commands.objects import read_object
from src.commands.objects import create_commit, write_tree
from src.commands.add import add_files
from tests.utils.test_helpers import temp_repo, create_test_files


class TestCatFile:
    """Tests pour la commande cat-file"""
    
    def test_cat_file_blob(self):
        """Test d'affichage d'un blob"""
        with temp_repo() as repo:
            # Créer un fichier et l'ajouter
            repo.create_file("test.txt", "contenu test")
            add_files(["test.txt"])
            
            # Obtenir le hash du blob
            from src.commands.hash_object import hash_object_git
            blob_sha = hash_object_git("test.txt", write=True)
            
            # Afficher le blob
            result = cat_file(blob_sha)
            assert result is True
    
    def test_cat_file_tree(self):
        """Test d'affichage d'un tree"""
        with temp_repo() as repo:
            # Créer des fichiers et un tree
            files = {"file1.txt": "contenu1", "file2.txt": "contenu2"}
            create_test_files(repo, files)
            add_files(list(files.keys()))
            tree_sha = write_tree()
            
            # Afficher le tree
            result = cat_file(tree_sha)
            assert result is True
    
    def test_cat_file_commit(self):
        """Test d'affichage d'un commit"""
        with temp_repo() as repo:
            # Créer un commit
            repo.create_file("test.txt", "contenu")
            add_files(["test.txt"])
            tree_sha = write_tree()
            commit_sha = create_commit(tree_sha, message="Test commit")
            
            # Afficher le commit
            result = cat_file(commit_sha)
            assert result is True
    
    def test_cat_file_invalid_sha(self):
        """Test d'affichage d'un objet avec SHA invalide"""
        with temp_repo() as repo:
            # Essayer d'afficher un objet inexistant
            result = cat_file("invalid_sha")
            assert result is False
    
    def test_cat_file_with_short_sha(self):
        """Test d'affichage d'un objet avec SHA court"""
        with temp_repo() as repo:
            # Créer un fichier et l'ajouter
            repo.create_file("test.txt", "contenu test")
            add_files(["test.txt"])
            
            # Obtenir le hash du blob
            from src.commands.hash_object import hash_object_git
            blob_sha = hash_object_git("test.txt", write=True)
            
            # Afficher le blob avec SHA court
            short_sha = blob_sha[:7]
            result = cat_file(short_sha)
            assert result is True
    
    def test_read_object_blob(self):
        """Test de lecture d'un objet blob"""
        with temp_repo() as repo:
            # Créer un fichier et l'ajouter
            repo.create_file("test.txt", "contenu test")
            add_files(["test.txt"])
            
            # Obtenir le hash du blob
            from src.commands.hash_object import hash_object_git
            blob_sha = hash_object_git("test.txt", write=True)
            
            # Lire l'objet
            obj_type, content = read_object(blob_sha)
            
            # Vérifier le type et le contenu
            assert obj_type == "blob"
            assert content.decode() == "contenu test"
    
    def test_read_object_tree(self):
        """Test de lecture d'un objet tree"""
        with temp_repo() as repo:
            # Créer des fichiers et un tree
            files = {"file1.txt": "contenu1", "file2.txt": "contenu2"}
            create_test_files(repo, files)
            add_files(list(files.keys()))
            tree_sha = write_tree()
            
            # Lire l'objet
            obj_type, content = read_object(tree_sha)
            
            # Vérifier le type
            assert obj_type == "tree"
            # Le contenu est binaire, on peut juste vérifier qu'il n'est pas vide
            assert len(content) > 0
    
    def test_read_object_commit(self):
        """Test de lecture d'un objet commit"""
        with temp_repo() as repo:
            # Créer un commit
            repo.create_file("test.txt", "contenu")
            add_files(["test.txt"])
            tree_sha = write_tree()
            commit_sha = create_commit(tree_sha, message="Test commit")
            
            # Lire l'objet
            obj_type, content = read_object(commit_sha)
            
            # Vérifier le type et le contenu
            assert obj_type == "commit"
            content_str = content.decode()
            assert "tree" in content_str
            assert "Test commit" in content_str
    
    def test_read_object_invalid_sha(self):
        """Test de lecture d'un objet avec SHA invalide"""
        with temp_repo() as repo:
            # Essayer de lire un objet inexistant
            with pytest.raises(Exception):
                read_object("invalid_sha")
    
    def test_cat_file_with_special_characters(self):
        """Test d'affichage d'un objet avec caractères spéciaux"""
        with temp_repo() as repo:
            # Créer un fichier avec caractères spéciaux
            special_content = "contenu avec émojis 🚀 et accents éàè"
            repo.create_file("test.txt", special_content)
            add_files(["test.txt"])
            
            # Obtenir le hash du blob
            from src.commands.hash_object import hash_object_git
            blob_sha = hash_object_git("test.txt", write=True)
            
            # Afficher le blob
            result = cat_file(blob_sha)
            assert result is True
    
    def test_cat_file_large_content(self):
        """Test d'affichage d'un objet avec contenu volumineux"""
        with temp_repo() as repo:
            # Créer un fichier avec beaucoup de contenu
            large_content = "ligne\n" * 1000
            repo.create_file("large.txt", large_content)
            add_files(["large.txt"])
            
            # Obtenir le hash du blob
            from src.commands.hash_object import hash_object_git
            blob_sha = hash_object_git("large.txt", write=True)
            
            # Afficher le blob
            result = cat_file(blob_sha)
            assert result is True
    
    def test_cat_file_empty_content(self):
        """Test d'affichage d'un objet avec contenu vide"""
        with temp_repo() as repo:
            # Créer un fichier vide
            repo.create_file("empty.txt", "")
            add_files(["empty.txt"])
            
            # Obtenir le hash du blob
            from src.commands.hash_object import hash_object_git
            blob_sha = hash_object_git("empty.txt", write=True)
            
            # Afficher le blob
            result = cat_file(blob_sha)
            assert result is True
    
    def test_cat_file_commit_with_parent(self):
        """Test d'affichage d'un commit avec parent"""
        with temp_repo() as repo:
            # Créer le premier commit
            repo.create_file("file1.txt", "contenu1")
            add_files(["file1.txt"])
            tree1_sha = write_tree()
            commit1_sha = create_commit(tree1_sha, message="Premier commit")
            
            # Créer le deuxième commit
            repo.create_file("file2.txt", "contenu2")
            add_files(["file2.txt"])
            tree2_sha = write_tree()
            commit2_sha = create_commit(tree2_sha, message="Deuxième commit", parent_sha1=commit1_sha)
            
            # Afficher le deuxième commit
            result = cat_file(commit2_sha)
            assert result is True
    
    def test_cat_file_tree_with_subdirectories(self):
        """Test d'affichage d'un tree avec sous-répertoires"""
        with temp_repo() as repo:
            # Créer une structure avec sous-répertoires
            os.makedirs("subdir", exist_ok=True)
            repo.create_file("file1.txt", "contenu1")
            repo.create_file("subdir/file2.txt", "contenu2")
            
            # Ajouter les fichiers
            add_files(["file1.txt", "subdir/file2.txt"])
            tree_sha = write_tree()
            
            # Afficher le tree
            result = cat_file(tree_sha)
            assert result is True 