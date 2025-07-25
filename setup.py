#!/usr/bin/env python3
"""
Script de configuration pour gitBis
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Exécuter une commande et afficher le résultat"""
    print(f"🚀 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCÈS")
            return True
        else:
            print(f"❌ {description} - ÉCHEC")
            if result.stderr:
                print(f"Erreur: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - ERREUR: {e}")
        return False

def check_python_version():
    """Vérifier la version de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9 ou supérieur est requis")
        print(f"Version actuelle: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def install_dependencies():
    """Installer les dépendances"""
    dependencies = [
        ("pytest>=8.0.0", "pytest"),
        ("pytest-cov>=6.0.0", "pytest-cov")
    ]
    
    for dep, name in dependencies:
        if not run_command(f"pip3 install {dep}", f"Installation de {name}"):
            return False
    return True

def make_executable():
    """Rendre gitBis.py exécutable"""
    if os.path.exists("gitBis.py"):
        try:
            os.chmod("gitBis.py", 0o755)
            print("✅ gitBis.py rendu exécutable")
            return True
        except Exception as e:
            print(f"❌ Erreur lors du changement de permissions: {e}")
            return False
    else:
        print("❌ gitBis.py non trouvé")
        return False

def create_alias():
    """Créer un alias pour gitBis"""
    shell_rc = ""
    if os.path.exists(os.path.expanduser("~/.zshrc")):
        shell_rc = "~/.zshrc"
    elif os.path.exists(os.path.expanduser("~/.bashrc")):
        shell_rc = "~/.bashrc"
    elif os.path.exists(os.path.expanduser("~/.bash_profile")):
        shell_rc = "~/.bash_profile"
    
    if shell_rc:
        alias_line = 'alias gitBis="python3 gitBis.py"'
        rc_path = os.path.expanduser(shell_rc)
        
        # Vérifier si l'alias existe déjà
        try:
            with open(rc_path, 'r') as f:
                content = f.read()
                if alias_line in content:
                    print(f"✅ Alias gitBis déjà présent dans {shell_rc}")
                    return True
        except:
            pass
        
        # Ajouter l'alias
        try:
            with open(rc_path, 'a') as f:
                f.write(f"\n# Alias pour gitBis\n{alias_line}\n")
            print(f"✅ Alias gitBis ajouté à {shell_rc}")
            print(f"💡 Exécutez 'source {shell_rc}' pour l'activer")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout de l'alias: {e}")
            return False
    else:
        print("⚠️  Aucun fichier de configuration shell trouvé")
        print("💡 Ajoutez manuellement: alias gitBis='python3 gitBis.py'")
        return True

def test_installation():
    """Tester l'installation"""
    print("\n🧪 Test de l'installation...")
    
    # Test de base
    if not run_command("python3 gitBis.py --help", "Test de gitBis --help"):
        return False
    
    # Test d'initialisation
    if os.path.exists(".mon_git"):
        shutil.rmtree(".mon_git")
    
    if not run_command("python3 gitBis.py init", "Test de gitBis init"):
        return False
    
    # Test des tests unitaires
    if not run_command("python3 -m pytest tests/test_init.py -v", "Test des tests unitaires"):
        return False
    
    return True

def main():
    """Fonction principale"""
    print("🔧 CONFIGURATION DE GITBIS")
    print("=" * 50)
    
    # Vérifier Python
    if not check_python_version():
        sys.exit(1)
    
    # Installer les dépendances
    print("\n📦 Installation des dépendances...")
    if not install_dependencies():
        print("❌ Échec de l'installation des dépendances")
        sys.exit(1)
    
    # Rendre exécutable
    print("\n🔧 Configuration des permissions...")
    if not make_executable():
        print("⚠️  gitBis.py n'est pas exécutable")
    
    # Créer l'alias
    print("\n🔗 Configuration de l'alias...")
    create_alias()
    
    # Tester l'installation
    print("\n🧪 Test de l'installation...")
    if test_installation():
        print("\n🎉 Installation terminée avec succès !")
        print("\n📚 Utilisation:")
        print("  python3 gitBis.py --help          # Aide")
        print("  python3 gitBis.py init            # Initialiser un dépôt")
        print("  python3 run_tests.py              # Lancer les tests")
        print("  python3 test_gitBis.py            # Tests d'intégration")
    else:
        print("\n❌ Installation échouée")
        sys.exit(1)

if __name__ == "__main__":
    main() 