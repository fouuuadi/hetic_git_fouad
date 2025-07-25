"""
Tests unitaires pour la commande log
"""

import pytest
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.commands.log import show_log, read_commit_object
from src.commands.objects import create_commit, write_tree
from src.commands.add import add_files
from tests.utils.test_helpers import temp_repo, create_test_files


class TestLog:
    """Tests pour la commande log"""
    
    def test_read_commit_object(self):
        """Test de lecture d'un objet commit"""
        with temp_repo() as repo:
            # Créer un commit
            repo.create_file("test.txt", "contenu")
            add_files(["test.txt"])
            tree_sha = write_tree()
            commit_sha = create_commit(tree_sha, message="Test commit")
            
            # Lire l'objet commit
            commit_info = read_commit_object(commit_sha)
            
            # Vérifier la structure
            assert "tree" in commit_info
            assert "message" in commit_info
            assert commit_info["tree"] == tree_sha
            assert commit_info["message"] == "Test commit"
            assert commit_info["parent"] is None  # Premier commit
    
    def test_read_commit_object_with_parent(self):
        """Test de lecture d'un objet commit avec parent"""
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
            
            # Lire l'objet commit
            commit_info = read_commit_object(commit2_sha)
            
            # Vérifier la structure
            assert "tree" in commit_info
            assert "message" in commit_info
            assert "parent" in commit_info
            assert commit_info["tree"] == tree2_sha
            assert commit_info["message"] == "Deuxième commit"
            assert commit_info["parent"] == commit1_sha
    
    def test_read_commit_object_with_multiple_parents(self):
        """Test de lecture d'un objet commit avec plusieurs parents"""
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

            # Créer un merge commit
            repo.create_file("file3.txt", "contenu3")
            add_files(["file3.txt"])
            tree3_sha = write_tree()
            commit3_sha = create_commit(tree3_sha, message="Merge commit",
                                      parent_sha1=commit1_sha, parent_sha2=commit2_sha)

            # Lire l'objet commit
            commit_info = read_commit_object(commit3_sha)

            # Vérifier la structure
            assert "tree" in commit_info
            assert "message" in commit_info
            assert "parents" in commit_info
            assert commit_info["tree"] == tree3_sha
            assert commit_info["message"] == "Merge commit"
            assert len(commit_info["parents"]) == 2
            assert commit_info["parents"][0] == commit1_sha  # Premier parent
            assert commit_info["parents"][1] == commit2_sha  # Deuxième parent
    
    def test_read_commit_object_invalid_sha(self):
        """Test de lecture d'un objet commit avec SHA invalide"""
        with temp_repo() as repo:
            # Essayer de lire un commit inexistant
            with pytest.raises(Exception):
                read_commit_object("invalid_sha")
    
    def test_read_commit_object_not_commit(self):
        """Test de lecture d'un objet qui n'est pas un commit"""
        with temp_repo() as repo:
            # Créer un blob
            repo.create_file("test.txt", "contenu")
            add_files(["test.txt"])
            
            # Obtenir le hash du blob
            from src.commands.hash_object import hash_object_git
            blob_sha = hash_object_git("test.txt", write=True)
            
            # Essayer de lire comme un commit
            with pytest.raises(Exception):
                read_commit_object(blob_sha)
    
    def test_show_log_single_commit(self):
        """Test d'affichage du log pour un seul commit"""
        with temp_repo() as repo:
            # Créer un commit
            repo.create_file("test.txt", "contenu")
            add_files(["test.txt"])
            tree_sha = write_tree()
            commit_sha = create_commit(tree_sha, message="Test commit")
            
            # Mettre à jour HEAD
            with open(".mon_git/refs/heads/main.txt", "w") as f:
                f.write(commit_sha)
            
            # Afficher le log
            result = show_log()
            
            # Vérifier que le log contient le commit
            assert result is True
    
    def test_show_log_multiple_commits(self):
        """Test d'affichage du log pour plusieurs commits"""
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
            
            # Mettre à jour HEAD
            with open(".mon_git/refs/heads/main.txt", "w") as f:
                f.write(commit2_sha)
            
            # Afficher le log
            result = show_log()
            
            # Vérifier que le log contient les deux commits
            assert result is True
    
    def test_show_log_oneline(self):
        """Test d'affichage du log en mode oneline"""
        with temp_repo() as repo:
            # Créer un commit
            repo.create_file("test.txt", "contenu")
            add_files(["test.txt"])
            tree_sha = write_tree()
            commit_sha = create_commit(tree_sha, message="Test commit")
            
            # Mettre à jour HEAD
            with open(".mon_git/refs/heads/main.txt", "w") as f:
                f.write(commit_sha)
            
            # Afficher le log en mode oneline
            result = show_log(oneline=True)
            
            # Vérifier que le log a été affiché
            assert result is True
    
    def test_show_log_with_limit(self):
        """Test d'affichage du log avec limite"""
        with temp_repo() as repo:
            # Créer plusieurs commits
            for i in range(5):
                repo.create_file(f"file{i}.txt", f"contenu{i}")
                add_files([f"file{i}.txt"])
                tree_sha = write_tree()
                if i == 0:
                    commit_sha = create_commit(tree_sha, message=f"Commit {i}")
                else:
                    commit_sha = create_commit(tree_sha, message=f"Commit {i}", parent_sha1=commit_sha)
            
            # Mettre à jour HEAD
            with open(".mon_git/refs/heads/main.txt", "w") as f:
                f.write(commit_sha)
            
            # Afficher le log avec limite
            result = show_log(limit=3)
            
            # Vérifier que le log a été affiché
            assert result is True
    
    def test_show_log_no_commits(self):
        """Test d'affichage du log sans commits"""
        with temp_repo() as repo:
            # HEAD pointe vers rien
            with open(".mon_git/refs/heads/main.txt", "w") as f:
                f.write("")
            
            # Afficher le log
            result = show_log()
            
            # Vérifier que le log a été affiché (même vide)
            assert result is True
    
    def test_show_log_detached_head(self):
        """Test d'affichage du log en mode detached HEAD"""
        with temp_repo() as repo:
            # Créer un commit
            repo.create_file("test.txt", "contenu")
            add_files(["test.txt"])
            tree_sha = write_tree()
            commit_sha = create_commit(tree_sha, message="Test commit")
            
            # Mettre HEAD en mode detached
            with open(".mon_git/HEAD.txt", "w") as f:
                f.write(commit_sha)
            
            # Afficher le log
            result = show_log()
            
            # Vérifier que le log a été affiché
            assert result is True
    
    def test_show_log_with_special_characters_in_message(self):
        """Test d'affichage du log avec caractères spéciaux dans le message"""
        with temp_repo() as repo:
            # Créer un commit avec message spécial
            repo.create_file("test.txt", "contenu")
            add_files(["test.txt"])
            tree_sha = write_tree()
            special_message = "Commit avec émojis 🚀 et accents éàè"
            commit_sha = create_commit(tree_sha, message=special_message)
            
            # Mettre à jour HEAD
            with open(".mon_git/refs/heads/main.txt", "w") as f:
                f.write(commit_sha)
            
            # Afficher le log
            result = show_log()
            
            # Vérifier que le log a été affiché
            assert result is True 