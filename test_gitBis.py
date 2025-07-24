#!/usr/bin/env python3
"""
Script de test pour gitBis
Teste toutes les commandes principales du système Git simplifié
"""

import subprocess
import os
import time

def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"\n{'='*60}")
    print(f"🔧 COMMANDE: {command}")
    print(f"📝 DESCRIPTION: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        print("📤 SORTIE:")
        if result.stdout:
            print("✅ STDOUT:")
            print(result.stdout)
        else:
            print("ℹ️  Aucune sortie standard")
            
        if result.stderr:
            print("⚠️  STDERR:")
            print(result.stderr)
        
        print(f"🔢 CODE DE RETOUR: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ SUCCÈS")
        else:
            print("❌ ÉCHEC")
        
        return result.returncode == 0
    except Exception as e:
        print(f"💥 ERREUR LORS DE L'EXÉCUTION: {e}")
        print(f"Erreur lors de l'exécution: {e}")
        return False

def main():
    print("🚀 DÉMARRAGE DES TESTS GITBIS")
    print("="*60)
    
    # Test 1: Initialisation du dépôt
    print("\n" + "="*60)
    print("🎯 TEST 1: INITIALISATION DU DÉPÔT")
    print("="*60)
    success = run_command("gitBis init", "Initialisation d'un nouveau dépôt Git")
    if not success:
        print("❌ Échec de l'initialisation")
        return
    
    # Test 2: Création de fichiers de test
    print("\n" + "="*60)
    print("🎯 TEST 2: CRÉATION DE FICHIERS DE TEST")
    print("="*60)
    print("📁 Création de fichiers de test...")
    with open("fichier1.txt", "w") as f:
        f.write("Contenu du fichier 1\n")
    with open("fichier2.txt", "w") as f:
        f.write("Contenu du fichier 2\n")
    print("✅ Fichiers de test créés:")
    print("   - fichier1.txt")
    print("   - fichier2.txt")
    
    # Test 3: Ajout de fichiers à l'index
    print("\n" + "="*60)
    print("🎯 TEST 3: AJOUT DE FICHIERS À L'INDEX")
    print("="*60)
    success = run_command("gitBis add fichier1.txt fichier2.txt", "Ajout de fichiers à l'index")
    if not success:
        print("❌ Échec de l'ajout de fichiers")
        return
    
    # Test 4: Liste des fichiers dans l'index
    print("\n" + "="*60)
    print("🎯 TEST 4: LISTE DES FICHIERS DANS L'INDEX")
    print("="*60)
    success = run_command("gitBis ls-files", "Liste des fichiers dans l'index")
    if not success:
        print("❌ Échec de la liste des fichiers")
        return
    
    # Test 5: Liste des fichiers avec hashes
    print("\n" + "="*60)
    print("🎯 TEST 5: LISTE DES FICHIERS AVEC HASHES")
    print("="*60)
    success = run_command("gitBis ls-files -v", "Liste des fichiers avec hashes")
    if not success:
        print("❌ Échec de la liste des fichiers avec hashes")
        return
    
    # Test 6: Statut du dépôt
    print("\n" + "="*60)
    print("🎯 TEST 6: STATUT DU DÉPÔT")
    print("="*60)
    success = run_command("gitBis status", "Statut du dépôt")
    if not success:
        print("❌ Échec du statut")
        return
    
    # Test 7: Hash d'un fichier
    print("\n" + "="*60)
    print("🎯 TEST 7: HASH D'UN FICHIER")
    print("="*60)
    success = run_command("gitBis hash-object fichier1.txt", "Calcul du hash d'un fichier")
    if not success:
        print("❌ Échec du hash")
        return
    
    # Test 8: Hash et écriture d'un fichier
    print("\n" + "="*60)
    print("🎯 TEST 8: HASH ET ÉCRITURE D'UN FICHIER")
    print("="*60)
    success = run_command("gitBis hash-object fichier1.txt -w", "Hash et écriture d'un fichier")
    if not success:
        print("❌ Échec du hash et écriture")
        return
    
    # Test 9: Affichage du type d'un objet
    print("\n" + "="*60)
    print("🎯 TEST 9: AFFICHAGE DU TYPE D'UN OBJET")
    print("="*60)
    # On récupère d'abord le hash du fichier
    print("🔍 Récupération du hash du fichier...")
    result = subprocess.run("gitBis hash-object fichier1.txt", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        # Extraire seulement le hash (dernière ligne, après le dernier espace)
        output_lines = result.stdout.strip().split('\n')
        hash_value = output_lines[-1].split()[-1]  # Prend le dernier mot de la dernière ligne
        print(f"🔑 Hash récupéré: {hash_value}")
        success = run_command(f"gitBis cat-file -t {hash_value}", f"Affichage du type de l'objet {hash_value}")
        if not success:
            print("❌ Échec de l'affichage du type")
            return
        
        # Test 10: Affichage du contenu d'un objet
        print("\n" + "="*60)
        print("🎯 TEST 10: AFFICHAGE DU CONTENU D'UN OBJET")
        print("="*60)
        success = run_command(f"gitBis cat-file -p {hash_value}", f"Affichage du contenu de l'objet {hash_value}")
        if not success:
            print("❌ Échec de l'affichage du contenu")
            return
    
    # Test 11: Création d'un tree
    print("\n" + "="*60)
    print("🎯 TEST 11: CRÉATION D'UN TREE")
    print("="*60)
    success = run_command("gitBis write-tree", "Création d'un objet tree")
    if not success:
        print("❌ Échec de la création du tree")
        return
    
    # Test 12: Création d'un commit
    print("\n" + "="*60)
    print("🎯 TEST 12: CRÉATION D'UN COMMIT")
    print("="*60)
    # On récupère d'abord le hash du tree
    print("🔍 Récupération du hash du tree...")
    result = subprocess.run("gitBis write-tree", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        tree_hash = result.stdout.strip()
        print(f"🌳 Hash du tree récupéré: {tree_hash}")
        success = run_command(f"gitBis commit-tree {tree_hash} -m 'Premier commit'", f"Création d'un commit avec le tree {tree_hash}")
        if not success:
            print("❌ Échec de la création du commit")
            return
        
        # Test 13: Création d'un commit avec parent
        print("\n" + "="*60)
        print("🎯 TEST 13: CRÉATION D'UN COMMIT AVEC PARENT")
        print("="*60)
        print("🔍 Récupération du hash du commit parent...")
        result = subprocess.run(f"gitBis commit-tree {tree_hash} -m 'Premier commit'", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            parent_hash = result.stdout.strip()
            print(f"👨‍👦 Hash du commit parent récupéré: {parent_hash}")
            success = run_command(f"gitBis commit-tree {tree_hash} -m 'Deuxième commit' -p {parent_hash}", f"Création d'un commit avec parent {parent_hash}")
            if not success:
                print("❌ Échec de la création du commit avec parent")
                return
    
    # Test 14: Réinitialisation (pour tester la suppression)
    print("\n" + "="*60)
    print("🎯 TEST 14: RÉINITIALISATION DU DÉPÔT")
    print("="*60)
    success = run_command("gitBis init", "Réinitialisation du dépôt (suppression de l'ancien)")
    if not success:
        print("❌ Échec de la réinitialisation")
        return
    
    print("\n" + "="*60)
    print("🎉 TOUS LES TESTS TERMINÉS AVEC SUCCÈS")
    print("="*60)
    print("📊 RÉSUMÉ:")
    print("   ✅ 14 tests exécutés")
    print("   ✅ Toutes les commandes fonctionnent")
    print("   ✅ Système Git simplifié opérationnel")
    print("="*60)

if __name__ == "__main__":
    main() 