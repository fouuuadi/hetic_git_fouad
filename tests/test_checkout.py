"""
Tests unitaires pour la commande checkout
"""

import pytest
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.commands.checkout import checkout, checkout_branch, checkout_commit, create_and_checkout_branch
from src.commands.objects import create_commit, write_tree
from src.commands.add import add_files
from tests.utils.test_helpers import temp_repo, create_test_files


class TestCheckout:
    """Tests pour la commande checkout"""
    
    def test_checkout_branch(self):
        """Test de checkout vers une branche existante"""
        with temp_repo() as repo:
            # Créer un commit sur main
            repo.create_file("main_file.txt", "contenu main")
            add_files(["main_file.txt"])
            tree_sha = write_tree()
            main_commit = create_commit(tree_sha, message="Commit main")
            
            # Mettre à jour main
            with open(".mon_git/refs/heads/main.txt", "w") as f:
                f.write(main_commit)
            
            # Créer une branche feature
            with open(".mon_git/refs/heads/feature.txt", "w") as f:
                f.write(main_commit)
            
            # Checkout vers feature
            result = checkout_branch("feature")
            assert result is True
            
            # Vérifier que HEAD pointe vers feature
            with open(".mon_git/HEAD.txt", "r") as f:
                head_content = f.read().strip()
            assert head_content == "ref: refs/heads/feature"
    
    def test_checkout_nonexistent_branch(self):
        """Test de checkout vers une branche inexistante"""
        with temp_repo() as repo:
            # Essayer de checkout vers une branche inexistante
            result = checkout_branch("nonexistent")
            assert result is False
    
    def test_checkout_commit(self):
        """Test de checkout vers un commit spécifique (detached HEAD)"""
        with temp_repo() as repo:
            # Créer un commit
            repo.create_file("test.txt", "contenu")
            add_files(["test.txt"])
            tree_sha = write_tree()
            commit_sha = create_commit(tree_sha, message="Test commit")
            
            # Checkout vers le commit
            result = checkout_commit(commit_sha)
            assert result is True
            
            # Vérifier que HEAD pointe directement vers le commit
            with open(".mon_git/HEAD.txt", "r") as f:
                head_content = f.read().strip()
            assert head_content == commit_sha
    
    def test_checkout_commit_with_short_sha(self):
        """Test de checkout vers un commit avec SHA court"""
        with temp_repo() as repo:
            # Créer un commit
            repo.create_file("test.txt", "contenu")
            add_files(["test.txt"])
            tree_sha = write_tree()
            commit_sha = create_commit(tree_sha, message="Test commit")
            
            # Checkout vers le commit avec SHA court
            short_sha = commit_sha[:7]
            result = checkout_commit(short_sha)
            assert result is True
            
            # Vérifier que HEAD pointe vers le commit complet
            with open(".mon_git/HEAD.txt", "r") as f:
                head_content = f.read().strip()
            assert head_content == commit_sha
    
    def test_checkout_invalid_commit(self):
        """Test de checkout vers un commit invalide"""
        with temp_repo() as repo:
            # Essayer de checkout vers un commit inexistant
            result = checkout_commit("invalid_sha")
            assert result is False
    
    def test_create_and_checkout_branch(self):
        """Test de création et checkout d'une nouvelle branche"""
        with temp_repo() as repo:
            # Créer un commit sur main
            repo.create_file("main_file.txt", "contenu main")
            add_files(["main_file.txt"])
            tree_sha = write_tree()
            main_commit = create_commit(tree_sha, message="Commit main")
            
            # Mettre à jour main
            with open(".mon_git/refs/heads/main.txt", "w") as f:
                f.write(main_commit)
            
            # Créer et checkout une nouvelle branche
            result = create_and_checkout_branch("new_branch")
            assert result is True
            
            # Vérifier que la branche a été créée
            assert os.path.exists(".mon_git/refs/heads/new_branch.txt")
            
            # Vérifier que HEAD pointe vers la nouvelle branche
            with open(".mon_git/HEAD.txt", "r") as f:
                head_content = f.read().strip()
            assert head_content == "ref: refs/heads/new_branch"
            
            # Vérifier que la branche pointe vers le même commit que main
            with open(".mon_git/refs/heads/new_branch.txt", "r") as f:
                branch_content = f.read().strip()
            assert branch_content == main_commit
    
    def test_create_and_checkout_branch_from_commit(self):
        """Test de création et checkout d'une branche depuis un commit spécifique"""
        with temp_repo() as repo:
            # Créer plusieurs commits
            repo.create_file("file1.txt", "contenu1")
            add_files(["file1.txt"])
            tree1_sha = write_tree()
            commit1_sha = create_commit(tree1_sha, message="Commit 1")
            
            repo.create_file("file2.txt", "contenu2")
            add_files(["file2.txt"])
            tree2_sha = write_tree()
            commit2_sha = create_commit(tree2_sha, message="Commit 2", parent_sha1=commit1_sha)
            
            # Mettre à jour main
            with open(".mon_git/refs/heads/main.txt", "w") as f:
                f.write(commit2_sha)
            
            # Créer et checkout une branche depuis le premier commit
            result = create_and_checkout_branch("old_branch", commit1_sha)
            assert result is True
            
            # Vérifier que la branche pointe vers le premier commit
            with open(".mon_git/refs/heads/old_branch.txt", "r") as f:
                branch_content = f.read().strip()
            assert branch_content == commit1_sha
    
    def test_create_branch_already_exists(self):
        """Test de création d'une branche qui existe déjà"""
        with temp_repo() as repo:
            # Créer un commit
            repo.create_file("test.txt", "contenu")
            add_files(["test.txt"])
            tree_sha = write_tree()
            commit_sha = create_commit(tree_sha, message="Test commit")
            
            # Créer une branche
            with open(".mon_git/refs/heads/existing.txt", "w") as f:
                f.write(commit_sha)
            
            # Essayer de créer la même branche
            result = create_and_checkout_branch("existing")
            assert result is False
    
    def test_checkout_main_branch(self):
        """Test de checkout vers la branche main"""
        with temp_repo() as repo:
            # Créer un commit sur main
            repo.create_file("test.txt", "contenu")
            add_files(["test.txt"])
            tree_sha = write_tree()
            commit_sha = create_commit(tree_sha, message="Test commit")
            
            # Mettre à jour main
            with open(".mon_git/refs/heads/main.txt", "w") as f:
                f.write(commit_sha)
            
            # Checkout vers main
            result = checkout_branch("main")
            assert result is True
            
            # Vérifier que HEAD pointe vers main
            with open(".mon_git/HEAD.txt", "r") as f:
                head_content = f.read().strip()
            assert head_content == "ref: refs/heads/main"
    
    def test_checkout_from_detached_head(self):
        """Test de checkout depuis un état detached HEAD"""
        with temp_repo() as repo:
            # Créer un commit
            repo.create_file("test.txt", "contenu")
            add_files(["test.txt"])
            tree_sha = write_tree()
            commit_sha = create_commit(tree_sha, message="Test commit")
            
            # Mettre HEAD en mode detached
            with open(".mon_git/HEAD.txt", "w") as f:
                f.write(commit_sha)
            
            # Créer une branche depuis cet état
            result = create_and_checkout_branch("from_detached")
            assert result is True
            
            # Vérifier que HEAD pointe vers la nouvelle branche
            with open(".mon_git/HEAD.txt", "r") as f:
                head_content = f.read().strip()
            assert head_content == "ref: refs/heads/from_detached"
    
    def test_checkout_branch_with_special_characters(self):
        """Test de checkout avec des caractères spéciaux dans le nom de branche"""
        with temp_repo() as repo:
            # Créer un commit
            repo.create_file("test.txt", "contenu")
            add_files(["test.txt"])
            tree_sha = write_tree()
            commit_sha = create_commit(tree_sha, message="Test commit")
            
            # Mettre à jour main
            with open(".mon_git/refs/heads/main.txt", "w") as f:
                f.write(commit_sha)
            
            # Créer une branche avec caractères spéciaux
            special_branch = "feature/émojis-🚀"
            result = create_and_checkout_branch(special_branch)
            assert result is True
            
            # Vérifier que la branche a été créée
            branch_file = f".mon_git/refs/heads/{special_branch}.txt"
            assert os.path.exists(branch_file)
    
    def test_checkout_preserves_working_directory(self):
        """Test que checkout préserve le working directory"""
        with temp_repo() as repo:
            # Créer un commit avec un fichier
            repo.create_file("main_file.txt", "contenu main")
            add_files(["main_file.txt"])
            tree_sha = write_tree()
            main_commit = create_commit(tree_sha, message="Commit main")
            
            # Mettre à jour main
            with open(".mon_git/refs/heads/main.txt", "w") as f:
                f.write(main_commit)
            
            # Créer un fichier non commité
            repo.create_file("uncommitted.txt", "contenu non commité")
            
            # Checkout vers main (devrait fonctionner)
            result = checkout_branch("main")
            assert result is True
            
            # Vérifier que le fichier non commité existe toujours
            assert os.path.exists("uncommitted.txt")
            with open("uncommitted.txt", "r") as f:
                content = f.read()
            assert content == "contenu non commité" 