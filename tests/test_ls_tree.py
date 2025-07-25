"""
Tests unitaires pour la commande ls-tree
"""

import pytest
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.commands.ls_tree import show_tree, parse_tree_content, format_tree_entry
from src.commands.objects import create_commit, write_tree
from src.commands.add import add_files
from tests.utils.test_helpers import temp_repo, create_test_files


class TestLsTree:
    """Tests pour la commande ls-tree"""
    
    def test_parse_tree_content(self):
        """Test de parsing du contenu d'un tree"""
        with temp_repo() as repo:
            # Créer des fichiers et un tree
            files = {"file1.txt": "contenu1", "file2.txt": "contenu2"}
            create_test_files(repo, files)
            add_files(list(files.keys()))
            tree_sha = write_tree()
            
            # Lire le contenu du tree
            from src.commands.objects import read_object
            obj_type, content = read_object(tree_sha)
            assert obj_type == "tree"
            
            # Parser le contenu
            entries = parse_tree_content(content)
            
            # Vérifier la structure
            assert len(entries) == 2
            assert any(entry["name"] == "file1.txt" for entry in entries)
            assert any(entry["name"] == "file2.txt" for entry in entries)
            
            # Vérifier que chaque entrée a les bons champs
            for entry in entries:
                assert "mode" in entry
                assert "type" in entry
                assert "sha" in entry
                assert "name" in entry
    
    def test_parse_tree_content_with_subdirectories(self):
        """Test de parsing du contenu d'un tree avec sous-répertoires"""
        with temp_repo() as repo:
            # Créer une structure avec sous-répertoires
            os.makedirs("subdir", exist_ok=True)
            repo.create_file("file1.txt", "contenu1")
            repo.create_file("subdir/file2.txt", "contenu2")
            
            # Ajouter les fichiers
            add_files(["file1.txt", "subdir/file2.txt"])
            tree_sha = write_tree()
            
            # Lire et parser le contenu du tree
            from src.commands.objects import read_object
            obj_type, content = read_object(tree_sha)
            entries = parse_tree_content(content)
            
            # Vérifier la structure
            assert len(entries) == 2
            assert any(entry["name"] == "file1.txt" for entry in entries)
            assert any(entry["name"] == "subdir/file2.txt" for entry in entries)
    
    def test_parse_tree_content_empty(self):
        """Test de parsing du contenu d'un tree vide"""
        with temp_repo() as repo:
            # Créer un tree vide
            tree_sha = write_tree()
            
            # Lire et parser le contenu du tree
            from src.commands.objects import read_object
            obj_type, content = read_object(tree_sha)
            entries = parse_tree_content(content)
            
            # Vérifier que le tree est vide
            assert len(entries) == 0
    
    def test_format_tree_entry(self):
        """Test de formatage d'une entrée de tree"""
        entry = {
            "mode": "100644",
            "type": "blob",
            "sha": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
            "name": "test.txt"
        }
        
        # Formater l'entrée
        formatted = format_tree_entry(entry)
        expected = "100644 blob a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2\ttest.txt"
        assert formatted == expected
    
    def test_format_tree_entry_tree_type(self):
        """Test de formatage d'une entrée de tree de type tree"""
        entry = {
            "mode": "040000",
            "type": "tree",
            "sha": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
            "name": "subdir"
        }
        
        # Formater l'entrée
        formatted = format_tree_entry(entry)
        expected = "040000 tree a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2\tsubdir"
        assert formatted == expected
    
    def test_show_tree(self):
        """Test d'affichage d'un tree"""
        with temp_repo() as repo:
            # Créer des fichiers et un tree
            files = {"file1.txt": "contenu1", "file2.txt": "contenu2"}
            create_test_files(repo, files)
            add_files(list(files.keys()))
            tree_sha = write_tree()
            
            # Afficher le tree
            result = show_tree(tree_sha)
            assert result is True
    
    def test_show_tree_with_long_format(self):
        """Test d'affichage d'un tree en format long"""
        with temp_repo() as repo:
            # Créer des fichiers et un tree
            files = {"file1.txt": "contenu1", "file2.txt": "contenu2"}
            create_test_files(repo, files)
            add_files(list(files.keys()))
            tree_sha = write_tree()
            
            # Afficher le tree en format long
            result = show_tree(tree_sha, long_format=True)
            assert result is True
    
    def test_show_tree_invalid_sha(self):
        """Test d'affichage d'un tree avec SHA invalide"""
        with temp_repo() as repo:
            # Essayer d'afficher un tree inexistant
            result = show_tree("invalid_sha")
            assert result is False
    
    def test_show_tree_not_tree_object(self):
        """Test d'affichage d'un objet qui n'est pas un tree"""
        with temp_repo() as repo:
            # Créer un blob
            repo.create_file("test.txt", "contenu")
            add_files(["test.txt"])
            
            # Obtenir le hash du blob
            from src.commands.hash_object import hash_object_git
            blob_sha = hash_object_git("test.txt", write=True)
            
            # Essayer d'afficher comme un tree
            result = show_tree(blob_sha)
            assert result is False
    
    def test_show_tree_with_short_sha(self):
        """Test d'affichage d'un tree avec SHA court"""
        with temp_repo() as repo:
            # Créer des fichiers et un tree
            files = {"file1.txt": "contenu1", "file2.txt": "contenu2"}
            create_test_files(repo, files)
            add_files(list(files.keys()))
            tree_sha = write_tree()
            
            # Afficher le tree avec SHA court
            short_sha = tree_sha[:7]
            result = show_tree(short_sha)
            assert result is True
    
    def test_show_tree_complex_structure(self):
        """Test d'affichage d'un tree avec structure complexe"""
        with temp_repo() as repo:
            # Créer une structure complexe
            os.makedirs("dir1", exist_ok=True)
            os.makedirs("dir2", exist_ok=True)
            repo.create_file("file1.txt", "contenu1")
            repo.create_file("dir1/file2.txt", "contenu2")
            repo.create_file("dir2/file3.txt", "contenu3")

            # Ajouter les fichiers
            add_files(["file1.txt", "dir1/file2.txt", "dir2/file3.txt"])
            tree_sha = write_tree()

            # Afficher le tree
            result = show_tree(tree_sha)
            assert result is True
    
    def test_show_tree_empty_tree(self):
        """Test d'affichage d'un tree vide"""
        with temp_repo() as repo:
            # Créer un tree vide
            tree_sha = write_tree()
            
            # Afficher le tree
            result = show_tree(tree_sha)
            assert result is True
    
    def test_show_tree_from_commit(self):
        """Test d'affichage du tree d'un commit"""
        with temp_repo() as repo:
            # Créer un commit
            files = {"file1.txt": "contenu1", "file2.txt": "contenu2"}
            create_test_files(repo, files)
            add_files(list(files.keys()))
            tree_sha = write_tree()
            commit_sha = create_commit(tree_sha, message="Test commit")

            # Obtenir le tree du commit
            from src.commands.log import read_commit_object
            commit_info = read_commit_object(commit_sha)
            tree_sha_from_commit = commit_info["tree"]

            # Afficher le tree
            result = show_tree(tree_sha_from_commit)
            assert result is True
    
    def test_show_tree_with_special_characters_in_filename(self):
        """Test d'affichage d'un tree avec caractères spéciaux dans les noms de fichiers"""
        with temp_repo() as repo:
            # Créer des fichiers avec caractères spéciaux
            files = {"file-émoji🚀.txt": "contenu1", "file_avec_espaces.txt": "contenu2"}
            create_test_files(repo, files)
            add_files(list(files.keys()))
            tree_sha = write_tree()
            
            # Afficher le tree
            result = show_tree(tree_sha)
            assert result is True 