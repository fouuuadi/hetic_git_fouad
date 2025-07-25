"""
Tests unitaires pour la commande commit
"""

import pytest
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.commands.objects import create_commit, write_tree
from src.commands.add import add_files
from tests.utils.test_helpers import temp_repo, create_test_files


class TestCommit:
    """Tests pour la commande commit"""
    
    def test_create_commit_with_message(self):
        """Test de création d'un commit avec un message"""
        with temp_repo() as repo:
            # Créer des fichiers et les ajouter
            files = {"file1.txt": "contenu1", "file2.txt": "contenu2"}
            create_test_files(repo, files)
            add_files(list(files.keys()))
            
            # Créer un tree
            tree_sha = write_tree()
            
            # Créer un commit
            commit_sha = create_commit(tree_sha, message="Premier commit")
            
            # Vérifier que le commit a été créé
            assert commit_sha is not None
            assert len(commit_sha) == 40  # SHA-1 complet
            
            # Vérifier que l'objet commit existe
            from src.commands.objects import read_object
            obj_type, content = read_object(commit_sha)
            assert obj_type == "commit"
            assert "tree" in content.decode()
            assert "Premier commit" in content.decode()
    
    def test_create_commit_with_parent(self):
        """Test de création d'un commit avec un parent"""
        with temp_repo() as repo:
            # Créer le premier commit
            files1 = {"file1.txt": "contenu1"}
            create_test_files(repo, files1)
            add_files(list(files1.keys()))
            tree1_sha = write_tree()
            commit1_sha = create_commit(tree1_sha, message="Premier commit")
            
            # Créer le deuxième commit avec parent
            files2 = {"file2.txt": "contenu2"}
            create_test_files(repo, files2)
            add_files(list(files2.keys()))
            tree2_sha = write_tree()
            commit2_sha = create_commit(tree2_sha, message="Deuxième commit", parent_sha1=commit1_sha)
            
            # Vérifier que le deuxième commit a un parent
            from src.commands.objects import read_object
            obj_type, content = read_object(commit2_sha)
            content_str = content.decode()
            assert "parent" in content_str
            assert commit1_sha in content_str
    
    def test_create_commit_with_multiple_parents(self):
        """Test de création d'un commit avec plusieurs parents"""
        with temp_repo() as repo:
            # Créer le premier commit
            files1 = {"file1.txt": "contenu1"}
            create_test_files(repo, files1)
            add_files(list(files1.keys()))
            tree1_sha = write_tree()
            commit1_sha = create_commit(tree1_sha, message="Premier commit")
            
            # Créer le deuxième commit
            files2 = {"file2.txt": "contenu2"}
            create_test_files(repo, files2)
            add_files(list(files2.keys()))
            tree2_sha = write_tree()
            commit2_sha = create_commit(tree2_sha, message="Deuxième commit", parent_sha1=commit1_sha)
            
            # Créer un troisième commit avec deux parents
            files3 = {"file3.txt": "contenu3"}
            create_test_files(repo, files3)
            add_files(list(files3.keys()))
            tree3_sha = write_tree()
            commit3_sha = create_commit(tree3_sha, message="Merge commit", 
                                      parent_sha1=commit1_sha, parent_sha2=commit2_sha)
            
            # Vérifier que le troisième commit a deux parents
            from src.commands.objects import read_object
            obj_type, content = read_object(commit3_sha)
            content_str = content.decode()
            assert content_str.count("parent") == 2
            assert commit1_sha in content_str
            assert commit2_sha in content_str
    
    def test_create_commit_empty_message(self):
        """Test de création d'un commit avec un message vide"""
        with temp_repo() as repo:
            # Créer un fichier et l'ajouter
            repo.create_file("test.txt", "contenu")
            add_files(["test.txt"])
            
            # Créer un tree
            tree_sha = write_tree()
            
            # Créer un commit avec message vide
            commit_sha = create_commit(tree_sha, message="")
            
            # Vérifier que le commit a été créé
            assert commit_sha is not None
            
            # Vérifier le contenu du commit
            from src.commands.objects import read_object
            obj_type, content = read_object(commit_sha)
            content_str = content.decode()
            assert "tree" in content_str
            # Le message peut être vide ou contenir un message par défaut
    
    def test_create_commit_with_special_characters_in_message(self):
        """Test de création d'un commit avec des caractères spéciaux dans le message"""
        with temp_repo() as repo:
            # Créer un fichier et l'ajouter
            repo.create_file("test.txt", "contenu")
            add_files(["test.txt"])
            
            # Créer un tree
            tree_sha = write_tree()
            
            # Créer un commit avec message spécial
            special_message = "Commit avec émojis 🚀 et accents éàè"
            commit_sha = create_commit(tree_sha, message=special_message)
            
            # Vérifier que le commit a été créé
            assert commit_sha is not None
            
            # Vérifier le contenu du commit
            from src.commands.objects import read_object
            obj_type, content = read_object(commit_sha)
            content_str = content.decode()
            assert special_message in content_str
    
    def test_write_tree_empty_index(self):
        """Test de création d'un tree avec un index vide"""
        with temp_repo() as repo:
            # Créer un tree sans fichiers
            tree_sha = write_tree()
            
            # Vérifier que le tree a été créé
            assert tree_sha is not None
            
            # Vérifier que l'objet tree existe
            from src.commands.objects import read_object
            obj_type, content = read_object(tree_sha)
            assert obj_type == "tree"
    
    def test_write_tree_with_files(self):
        """Test de création d'un tree avec des fichiers"""
        with temp_repo() as repo:
            # Créer des fichiers et les ajouter
            files = {"file1.txt": "contenu1", "file2.txt": "contenu2"}
            create_test_files(repo, files)
            add_files(list(files.keys()))
            
            # Créer un tree
            tree_sha = write_tree()
            
            # Vérifier que le tree a été créé
            assert tree_sha is not None
            
            # Vérifier que l'objet tree existe
            from src.commands.objects import read_object
            obj_type, content = read_object(tree_sha)
            assert obj_type == "tree"
    
    def test_write_tree_with_subdirectories(self):
        """Test de création d'un tree avec des sous-répertoires"""
        with temp_repo() as repo:
            # Créer une structure avec sous-répertoires
            os.makedirs("subdir", exist_ok=True)
            repo.create_file("file1.txt", "contenu1")
            repo.create_file("subdir/file2.txt", "contenu2")
            
            # Ajouter les fichiers
            add_files(["file1.txt", "subdir/file2.txt"])
            
            # Créer un tree
            tree_sha = write_tree()
            
            # Vérifier que le tree a été créé
            assert tree_sha is not None
            
            # Vérifier que l'objet tree existe
            from src.commands.objects import read_object
            obj_type, content = read_object(tree_sha)
            assert obj_type == "tree"
    
    def test_commit_chain(self):
        """Test d'une chaîne de commits"""
        with temp_repo() as repo:
            # Premier commit
            repo.create_file("file1.txt", "contenu1")
            add_files(["file1.txt"])
            tree1_sha = write_tree()
            commit1_sha = create_commit(tree1_sha, message="Premier commit")
            
            # Deuxième commit
            repo.create_file("file2.txt", "contenu2")
            add_files(["file2.txt"])
            tree2_sha = write_tree()
            commit2_sha = create_commit(tree2_sha, message="Deuxième commit", parent_sha1=commit1_sha)
            
            # Troisième commit
            repo.create_file("file3.txt", "contenu3")
            add_files(["file3.txt"])
            tree3_sha = write_tree()
            commit3_sha = create_commit(tree3_sha, message="Troisième commit", parent_sha1=commit2_sha)
            
            # Vérifier que tous les commits existent
            from src.commands.objects import read_object
            
            # Vérifier le premier commit
            obj_type, content = read_object(commit1_sha)
            assert obj_type == "commit"
            content_str = content.decode()
            assert "Premier commit" in content_str
            assert "parent" not in content_str
            
            # Vérifier le deuxième commit
            obj_type, content = read_object(commit2_sha)
            assert obj_type == "commit"
            content_str = content.decode()
            assert "Deuxième commit" in content_str
            assert f"parent {commit1_sha}" in content_str
            
            # Vérifier le troisième commit
            obj_type, content = read_object(commit3_sha)
            assert obj_type == "commit"
            content_str = content.decode()
            assert "Troisième commit" in content_str
            assert f"parent {commit2_sha}" in content_str 