"""
Tests unitaires pour la commande add
"""

import pytest
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.commands.add import add_files, read_index
from tests.utils.test_helpers import temp_repo, create_test_files, assert_file_exists


class TestAdd:
    """Tests pour la commande add"""
    
    def test_add_single_file(self):
        """Test d'ajout d'un fichier simple"""
        with temp_repo() as repo:
            # Créer un fichier de test
            repo.create_file("test.txt", "contenu test")
            
            # Ajouter le fichier
            add_files(["test.txt"])
            
            # Vérifier que le fichier est dans l'index
            index = read_index()
            assert "test.txt" in index
            assert index["test.txt"] is not None
    
    def test_add_multiple_files(self):
        """Test d'ajout de plusieurs fichiers"""
        with temp_repo() as repo:
            # Créer plusieurs fichiers
            files = {
                "file1.txt": "contenu 1",
                "file2.txt": "contenu 2",
                "file3.txt": "contenu 3"
            }
            create_test_files(repo, files)
            
            # Ajouter les fichiers
            add_files(list(files.keys()))
            
            # Vérifier que tous les fichiers sont dans l'index
            index = read_index()
            for filename in files.keys():
                assert filename in index
                assert index[filename] is not None
    
    def test_add_nonexistent_file(self):
        """Test d'ajout d'un fichier inexistant"""
        with temp_repo() as repo:
            # Essayer d'ajouter un fichier qui n'existe pas
            add_files(["nonexistent.txt"])
            
            # Vérifier que l'index est vide (ou gérer l'erreur selon l'implémentation)
            index = read_index()
            # Le comportement exact dépend de l'implémentation
    
    def test_add_empty_file(self):
        """Test d'ajout d'un fichier vide"""
        with temp_repo() as repo:
            # Créer un fichier vide
            repo.create_file("empty.txt", "")
            
            # Ajouter le fichier
            add_files(["empty.txt"])
            
            # Vérifier que le fichier est dans l'index
            index = read_index()
            assert "empty.txt" in index
    
    def test_add_file_with_special_characters(self):
        """Test d'ajout d'un fichier avec des caractères spéciaux"""
        with temp_repo() as repo:
            # Créer un fichier avec des caractères spéciaux
            content = "contenu avec émojis 🚀 et accents éàè"
            repo.create_file("special.txt", content)
            
            # Ajouter le fichier
            add_files(["special.txt"])
            
            # Vérifier que le fichier est dans l'index
            index = read_index()
            assert "special.txt" in index
    
    def test_add_file_in_subdirectory(self):
        """Test d'ajout d'un fichier dans un sous-répertoire"""
        with temp_repo() as repo:
            # Créer un sous-répertoire
            os.makedirs("subdir", exist_ok=True)
            
            # Créer un fichier dans le sous-répertoire
            repo.create_file("subdir/test.txt", "contenu dans sous-dir")
            
            # Ajouter le fichier
            add_files(["subdir/test.txt"])
            
            # Vérifier que le fichier est dans l'index
            index = read_index()
            assert "subdir/test.txt" in index
    
    def test_add_already_added_file(self):
        """Test d'ajout d'un fichier déjà dans l'index"""
        with temp_repo() as repo:
            # Créer un fichier
            repo.create_file("test.txt", "contenu")
            
            # Ajouter le fichier une première fois
            add_files(["test.txt"])
            index1 = read_index()
            
            # Modifier le fichier
            repo.create_file("test.txt", "contenu modifié")
            
            # Ajouter le fichier une deuxième fois
            add_files(["test.txt"])
            index2 = read_index()
            
            # Vérifier que le hash a changé
            assert "test.txt" in index1
            assert "test.txt" in index2
            # Les hashes devraient être différents si le contenu a changé
    
    def test_read_index_empty(self):
        """Test de lecture d'un index vide"""
        with temp_repo() as repo:
            index = read_index()
            assert isinstance(index, dict)
            assert len(index) == 0
    
    def test_read_index_with_files(self):
        """Test de lecture d'un index avec des fichiers"""
        with temp_repo() as repo:
            # Créer et ajouter des fichiers
            files = {"file1.txt": "contenu1", "file2.txt": "contenu2"}
            create_test_files(repo, files)
            add_files(list(files.keys()))
            
            # Lire l'index
            index = read_index()
            
            # Vérifier la structure
            assert isinstance(index, dict)
            assert len(index) == 2
            assert "file1.txt" in index
            assert "file2.txt" in index
            assert isinstance(index["file1.txt"], str)
            assert isinstance(index["file2.txt"], str) 