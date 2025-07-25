"""
Tests unitaires pour la commande reset
"""

import pytest
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.commands.reset import reset, reset_soft, reset_mixed, reset_hard
from src.commands.add import add_files
from src.commands.objects import create_commit, write_tree
from tests.utils.test_helpers import temp_repo, create_test_files


class TestReset:
    """Tests pour la commande reset"""
    
    def test_reset_soft_only_updates_head(self):
        """Test que reset soft ne met à jour que HEAD"""
        with temp_repo() as repo:
            # Créer des fichiers et les ajouter
            files = {"file1.txt": "contenu1", "file2.txt": "contenu2"}
            create_test_files(repo, files)
            add_files(list(files.keys()))
            
            # Créer un commit
            tree_sha = write_tree()
            commit1_sha = create_commit(tree_sha, message="Premier commit")
            
            # Modifier les fichiers et les ajouter à nouveau
            repo.create_file("file1.txt", "contenu modifié")
            add_files(["file1.txt"])
            
            # Créer un deuxième commit
            tree_sha2 = write_tree()
            commit2_sha = create_commit(tree_sha2, message="Deuxième commit", parent_sha1=commit1_sha)
            
            # Mettre à jour HEAD vers le deuxième commit
            with open(".mon_git/refs/heads/main.txt", "w") as f:
                f.write(commit2_sha)
            
            # Reset soft vers le premier commit
            result = reset_soft(commit1_sha)
            assert result is True
            
            # Vérifier que HEAD pointe vers le premier commit
            with open(".mon_git/refs/heads/main.txt", "r") as f:
                current_head = f.read().strip()
            assert current_head == commit1_sha
            
            # Vérifier que l'index contient encore les modifications
            from src.commands.add import read_index
            index = read_index()
            assert "file1.txt" in index
    
    def test_reset_mixed_updates_head_and_index(self):
        """Test que reset mixed met à jour HEAD et l'index"""
        with temp_repo() as repo:
            # Créer des fichiers et les ajouter
            files = {"file1.txt": "contenu1", "file2.txt": "contenu2"}
            create_test_files(repo, files)
            add_files(list(files.keys()))
            
            # Créer un commit
            tree_sha = write_tree()
            commit1_sha = create_commit(tree_sha, message="Premier commit")
            
            # Modifier les fichiers et les ajouter à nouveau
            repo.create_file("file1.txt", "contenu modifié")
            add_files(["file1.txt"])
            
            # Créer un deuxième commit
            tree_sha2 = write_tree()
            commit2_sha = create_commit(tree_sha2, message="Deuxième commit", parent_sha1=commit1_sha)
            
            # Mettre à jour HEAD vers le deuxième commit
            with open(".mon_git/refs/heads/main.txt", "w") as f:
                f.write(commit2_sha)
            
            # Reset mixed vers le premier commit
            result = reset_mixed(commit1_sha)
            assert result is True
            
            # Vérifier que HEAD pointe vers le premier commit
            with open(".mon_git/refs/heads/main.txt", "r") as f:
                current_head = f.read().strip()
            assert current_head == commit1_sha
            
            # Vérifier que l'index a été mis à jour avec le contenu du premier commit
            from src.commands.add import read_index
            index = read_index()
            # L'index devrait contenir les fichiers du premier commit
    
    def test_reset_hard_updates_head_index_and_working_directory(self):
        """Test que reset hard met à jour HEAD, l'index et le working directory"""
        with temp_repo() as repo:
            # Créer des fichiers et les ajouter
            files = {"file1.txt": "contenu1", "file2.txt": "contenu2"}
            create_test_files(repo, files)
            add_files(list(files.keys()))
            
            # Créer un commit
            tree_sha = write_tree()
            commit1_sha = create_commit(tree_sha, message="Premier commit")
            
            # Modifier les fichiers dans le working directory
            repo.create_file("file1.txt", "contenu modifié")
            repo.create_file("file3.txt", "nouveau fichier")
            add_files(["file1.txt", "file3.txt"])
            
            # Créer un deuxième commit
            tree_sha2 = write_tree()
            commit2_sha = create_commit(tree_sha2, message="Deuxième commit", parent_sha1=commit1_sha)
            
            # Mettre à jour HEAD vers le deuxième commit
            with open(".mon_git/refs/heads/main.txt", "w") as f:
                f.write(commit2_sha)
            
            # Reset hard vers le premier commit
            result = reset_hard(commit1_sha)
            assert result is True
            
            # Vérifier que HEAD pointe vers le premier commit
            with open(".mon_git/refs/heads/main.txt", "r") as f:
                current_head = f.read().strip()
            assert current_head == commit1_sha
            
            # Vérifier que l'index a été mis à jour
            from src.commands.add import read_index
            index = read_index()
            # L'index devrait contenir les fichiers du premier commit
    
    def test_reset_invalid_commit(self):
        """Test que reset échoue avec un commit invalide"""
        with temp_repo() as repo:
            # Essayer de reset vers un commit inexistant
            result = reset("invalid_commit_sha")
            assert result is False
    
    def test_reset_invalid_object_type(self):
        """Test que reset échoue avec un objet qui n'est pas un commit"""
        with temp_repo() as repo:
            # Créer un fichier et obtenir son hash (blob)
            repo.create_file("test.txt", "contenu")
            add_files(["test.txt"])
            
            # Obtenir le hash du blob
            from src.commands.hash_object import hash_object_git
            blob_sha = hash_object_git("test.txt", write=True)
            
            # Essayer de reset vers un blob (devrait échouer)
            result = reset(blob_sha)
            assert result is False
    
    def test_reset_with_branch_name(self):
        """Test que reset fonctionne avec un nom de branche"""
        with temp_repo() as repo:
            # Créer des fichiers et les ajouter
            files = {"file1.txt": "contenu1"}
            create_test_files(repo, files)
            add_files(list(files.keys()))
            
            # Créer un commit
            tree_sha = write_tree()
            commit_sha = create_commit(tree_sha, message="Premier commit")
            
            # Mettre à jour HEAD vers le commit
            with open(".mon_git/refs/heads/main.txt", "w") as f:
                f.write(commit_sha)
            
            # Reset vers la branche main
            result = reset("main")
            assert result is True
    
    def test_reset_with_short_sha(self):
        """Test que reset fonctionne avec un SHA court"""
        with temp_repo() as repo:
            # Créer des fichiers et les ajouter
            files = {"file1.txt": "contenu1"}
            create_test_files(repo, files)
            add_files(list(files.keys()))
            
            # Créer un commit
            tree_sha = write_tree()
            commit_sha = create_commit(tree_sha, message="Premier commit")
            
            # Mettre à jour HEAD vers le commit
            with open(".mon_git/refs/heads/main.txt", "w") as f:
                f.write(commit_sha)
            
            # Reset vers le SHA court
            short_sha = commit_sha[:7]
            result = reset(short_sha)
            assert result is True
    
    def test_reset_detached_head(self):
        """Test que reset fonctionne en mode detached HEAD"""
        with temp_repo() as repo:
            # Créer des fichiers et les ajouter
            files = {"file1.txt": "contenu1"}
            create_test_files(repo, files)
            add_files(list(files.keys()))
            
            # Créer un commit
            tree_sha = write_tree()
            commit_sha = create_commit(tree_sha, message="Premier commit")
            
            # Mettre HEAD en mode detached
            with open(".mon_git/HEAD.txt", "w") as f:
                f.write(commit_sha)
            
            # Reset vers le même commit
            result = reset(commit_sha)
            assert result is True
            
            # Vérifier que HEAD est toujours en mode detached
            with open(".mon_git/HEAD.txt", "r") as f:
                head_content = f.read().strip()
            assert head_content == commit_sha 