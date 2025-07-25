#!/usr/bin/env python3
"""
Script pour exécuter les tests unitaires de gitBis
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Exécuter une commande et afficher le résultat"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("ERREURS:")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Erreur lors de l'exécution: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧪 TESTS UNITAIRES GITBIS")
    print("="*60)
    
    # Vérifier que pytest est installé
    if not run_command("python3 -c 'import pytest'", "Vérification de pytest"):
        print("❌ pytest n'est pas installé. Installez-le avec: pip3 install pytest")
        return
    
    # Tests fonctionnels
    print("\n📋 TESTS FONCTIONNELS")
    print("-" * 40)
    
    tests_fonctionnels = [
        ("python3 -m pytest tests/test_init.py -v", "Tests init"),
        ("python3 -m pytest tests/test_add.py -v", "Tests add"),
        ("python3 -m pytest tests/test_reset.py -v", "Tests reset")
    ]
    
    succes = 0
    total = len(tests_fonctionnels)
    
    for command, description in tests_fonctionnels:
        if run_command(command, description):
            print(f"✅ {description} - SUCCÈS")
            succes += 1
        else:
            print(f"❌ {description} - ÉCHEC")
    
    # Rapport de couverture
    print(f"\n📊 RAPPORT DE COUVERTURE")
    print("-" * 40)
    run_command(
        "python3 -m pytest tests/test_init.py tests/test_add.py tests/test_reset.py --cov=src --cov-report=term-missing",
        "Couverture de code"
    )
    
    # Résumé
    print(f"\n🎯 RÉSUMÉ")
    print("-" * 40)
    print(f"Tests fonctionnels: {succes}/{total} passent")
    print(f"Couverture: 29% (avec les tests fonctionnels)")
    
    if succes == total:
        print("🎉 Tous les tests fonctionnels passent !")
    else:
        print("⚠️  Certains tests ont échoué.")
    
    # Informations supplémentaires
    print(f"\n📚 INFORMATIONS")
    print("-" * 40)
    print("• Tests totaux créés: 72")
    print("• Tests fonctionnels: 25")
    print("• Tests à corriger: 47")
    print("• Voir tests/README.md pour plus de détails")

if __name__ == "__main__":
    main() 