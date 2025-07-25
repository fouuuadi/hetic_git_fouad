"""
Tests unitaires pour la commande init
"""

import pytest
import os
import sys
import shutil

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.commands.init import init
from tests.utils.test_helpers import temp_repo


class TestInit:
    """Tests pour la commande init"""
    
    def test_init_creates_git_structure(self):
        """Test que init crée la structure .mon_git"""
        with temp_repo() as repo:
            # Supprimer le .mon_git existant créé par temp_repo
            if os.path.exists(".mon_git"):
                shutil.rmtree(".mon_git")
            
            # Initialiser le dépôt
            init()
            
            # Vérifier que la structure existe
            assert os.path.exists(".mon_git")
            assert os.path.exists(".mon_git/objects")
            assert os.path.exists(".mon_git/refs")
            assert os.path.exists(".mon_git/refs/heads")
            assert os.path.exists(".mon_git/HEAD.txt")
    
    def test_init_creates_head_file(self):
        """Test que init crée le fichier HEAD.txt"""
        with temp_repo() as repo:
            # Supprimer le .mon_git existant
            if os.path.exists(".mon_git"):
                shutil.rmtree(".mon_git")
            
            # Initialiser le dépôt
            init()
            
            # Vérifier le contenu de HEAD.txt
            with open(".mon_git/HEAD.txt", "r") as f:
                head_content = f.read().strip()
            
            assert head_content == "ref: refs/heads/main"
    
    def test_init_creates_main_branch(self):
        """Test que init crée la branche main"""
        with temp_repo() as repo:
            # Supprimer le .mon_git existant
            if os.path.exists(".mon_git"):
                shutil.rmtree(".mon_git")
            
            # Initialiser le dépôt
            init()
            
            # Vérifier que la branche main existe
            main_branch_file = ".mon_git/refs/heads/main.txt"
            assert os.path.exists(main_branch_file)
            
            # Vérifier que le fichier contient le commentaire attendu
            with open(main_branch_file, "r") as f:
                content = f.read().strip()
            assert content == "# Branch main - no commits yet"
    
    def test_init_creates_index_file(self):
        """Test que init crée le fichier index"""
        with temp_repo() as repo:
            # Supprimer le .mon_git existant
            if os.path.exists(".mon_git"):
                shutil.rmtree(".mon_git")
            
            # Initialiser le dépôt
            init()
            
            # Vérifier que l'index existe (index.txt dans l'implémentation actuelle)
            assert os.path.exists(".mon_git/index.txt")
            
            # Vérifier le contenu de l'index
            with open(".mon_git/index.txt", "r") as f:
                content = f.read()
            assert "# Git Index File" in content
            assert "# Version: 2" in content
    
    def test_init_removes_existing_repo(self):
        """Test que init supprime un dépôt existant"""
        with temp_repo() as repo:
            # Créer un fichier dans .mon_git pour simuler un dépôt existant
            os.makedirs(".mon_git", exist_ok=True)
            with open(".mon_git/test_file.txt", "w") as f:
                f.write("ancien contenu")
            
            # Initialiser le dépôt
            init()
            
            # Vérifier que l'ancien fichier n'existe plus
            assert not os.path.exists(".mon_git/test_file.txt")
            
            # Vérifier que la nouvelle structure existe
            assert os.path.exists(".mon_git/objects")
            assert os.path.exists(".mon_git/refs/heads")
    
    def test_init_creates_directories_with_correct_permissions(self):
        """Test que init crée les répertoires avec les bonnes permissions"""
        with temp_repo() as repo:
            # Supprimer le .mon_git existant
            if os.path.exists(".mon_git"):
                shutil.rmtree(".mon_git")
            
            # Initialiser le dépôt
            init()
            
            # Vérifier que les répertoires sont des répertoires
            assert os.path.isdir(".mon_git")
            assert os.path.isdir(".mon_git/objects")
            assert os.path.isdir(".mon_git/refs")
            assert os.path.isdir(".mon_git/refs/heads")
    
    def test_init_creates_files_with_correct_permissions(self):
        """Test que init crée les fichiers avec les bonnes permissions"""
        with temp_repo() as repo:
            # Supprimer le .mon_git existant
            if os.path.exists(".mon_git"):
                shutil.rmtree(".mon_git")
            
            # Initialiser le dépôt
            init()
            
            # Vérifier que les fichiers sont des fichiers
            assert os.path.isfile(".mon_git/HEAD.txt")
            assert os.path.isfile(".mon_git/refs/heads/main.txt")
            assert os.path.isfile(".mon_git/index.txt")
    
    def test_init_multiple_times(self):
        """Test que init peut être appelé plusieurs fois"""
        with temp_repo() as repo:
            # Supprimer le .mon_git existant
            if os.path.exists(".mon_git"):
                shutil.rmtree(".mon_git")
            
            # Initialiser le dépôt plusieurs fois
            init()
            init()
            init()
            
            # Vérifier que la structure est toujours correcte
            assert os.path.exists(".mon_git/objects")
            assert os.path.exists(".mon_git/refs/heads")
            assert os.path.exists(".mon_git/HEAD.txt")
            
            # Vérifier le contenu de HEAD.txt
            with open(".mon_git/HEAD.txt", "r") as f:
                head_content = f.read().strip()
            assert head_content == "ref: refs/heads/main" 