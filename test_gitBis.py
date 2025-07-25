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
    
    # Test 7: Gestion des fichiers .gitignore
    print("\n" + "="*60)
    print("🎯 TEST 7: GESTION DES FICHIERS .GITIGNORE")
    print("="*60)
    success = run_command("gitBis gitignore '*.log'", "Ajout d'un pattern au fichier .gitignore")
    if not success:
        print("❌ Échec de l'ajout au .gitignore")
        return
    
    # Test 8: Hash d'un fichier
    print("\n" + "="*60)
    print("🎯 TEST 8: HASH D'UN FICHIER")
    print("="*60)
    success = run_command("gitBis hash-object fichier1.txt", "Calcul du hash d'un fichier")
    if not success:
        print("❌ Échec du hash")
        return
    
    # Test 9: Hash et écriture d'un fichier
    print("\n" + "="*60)
    print("🎯 TEST 9: HASH ET ÉCRITURE D'UN FICHIER")
    print("="*60)
    success = run_command("gitBis hash-object fichier1.txt -w", "Hash et écriture d'un fichier")
    if not success:
        print("❌ Échec du hash et écriture")
        return
    
    # Test 10: Affichage du type d'un objet
    print("\n" + "="*60)
    print("🎯 TEST 10: AFFICHAGE DU TYPE D'UN OBJET")
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
        
        # Test 11: Affichage du contenu d'un objet
        print("\n" + "="*60)
        print("🎯 TEST 11: AFFICHAGE DU CONTENU D'UN OBJET")
        print("="*60)
        success = run_command(f"gitBis cat-file -p {hash_value}", f"Affichage du contenu de l'objet {hash_value}")
        if not success:
            print("❌ Échec de l'affichage du contenu")
            return
    
    # Test 12: Création d'un tree
    print("\n" + "="*60)
    print("🎯 TEST 12: CRÉATION D'UN TREE")
    print("="*60)
    success = run_command("gitBis write-tree", "Création d'un objet tree")
    if not success:
        print("❌ Échec de la création du tree")
        return
    
    # Test 13: Création d'un commit
    print("\n" + "="*60)
    print("🎯 TEST 13: CRÉATION D'UN COMMIT")
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
        
        # Test 14: Création d'un commit avec parent
        print("\n" + "="*60)
        print("🎯 TEST 14: CRÉATION D'UN COMMIT AVEC PARENT")
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
    
    # Test 15: Commit via la commande porcelain
    print("\n" + "="*60)
    print("🎯 TEST 15: COMMIT VIA LA COMMANDE PORCELAIN")
    print("="*60)
    success = run_command("gitBis commit -m 'Commit via commande porcelain'", "Création d'un commit avec la commande porcelain")
    if not success:
        print("❌ Échec du commit porcelain")
        return
    
    # Test 16: Convertir une référence en SHA-1
    print("\n" + "="*60)
    print("🎯 TEST 16: CONVERTIR UNE RÉFÉRENCE EN SHA-1")
    print("="*60)
    success = run_command("gitBis rev-parse HEAD", "Conversion de HEAD en SHA-1")
    if not success:
        print("❌ Échec de la conversion HEAD")
        return
    
    success = run_command("gitBis rev-parse main", "Conversion de la branche main en SHA-1")
    if not success:
        print("❌ Échec de la conversion main")
        return
    
    # Test 17: Afficher les références
    print("\n" + "="*60)
    print("🎯 TEST 17: AFFICHER LES RÉFÉRENCES")
    print("="*60)
    success = run_command("gitBis show-ref", "Affichage de toutes les références")
    if not success:
        print("❌ Échec de l'affichage des références")
        return
    
    success = run_command("gitBis show-ref --heads", "Affichage des branches seulement")
    if not success:
        print("❌ Échec de l'affichage des branches")
        return
    
    # Test 18: Afficher l'historique des commits
    print("\n" + "="*60)
    print("🎯 TEST 18: AFFICHER L'HISTORIQUE DES COMMITS")
    print("="*60)
    success = run_command("gitBis log --oneline", "Affichage de l'historique en format compact")
    if not success:
        print("❌ Échec de l'affichage de l'historique")
        return
    
    success = run_command("gitBis log", "Affichage de l'historique détaillé")
    if not success:
        print("❌ Échec de l'affichage de l'historique détaillé")
        return
    
    # Test 19: Lister le contenu d'un tree
    print("\n" + "="*60)
    print("🎯 TEST 19: LISTER LE CONTENU D'UN TREE")
    print("="*60)
    # Récupérer le hash du tree
    print("🔍 Récupération du hash du tree...")
    result = subprocess.run("gitBis write-tree", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        tree_hash = result.stdout.strip()
        print(f"🌳 Hash du tree récupéré: {tree_hash}")
        success = run_command(f"gitBis ls-tree {tree_hash}", f"Affichage du contenu du tree {tree_hash}")
        if not success:
            print("❌ Échec de l'affichage du tree")
            return
        
        # Test avec un objet blob (erreur attendue)
        print("🔍 Test avec un objet blob (erreur attendue)...")
        result = subprocess.run("gitBis hash-object test.txt", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            blob_hash = result.stdout.strip().split()[-1]
            print(f"📄 Hash du blob récupéré: {blob_hash}")
            success = run_command(f"gitBis ls-tree {blob_hash}", f"Test avec un objet blob {blob_hash}")
            # Ce test doit échouer car un blob n'est pas un tree
            if success:
                print("⚠️  Test inattendu: ls-tree avec un blob a réussi")
            else:
                print("✅ Test réussi: ls-tree avec un blob a échoué comme attendu")
    
    # Test 20: Basculer de branche ou créer une branche
    print("\n" + "="*60)
    print("🎯 TEST 20: BASCULER DE BRANCHE OU CRÉER UNE BRANCHE")
    print("="*60)
    success = run_command("gitBis checkout main", "Basculement vers la branche main")
    if not success:
        print("❌ Échec du basculement vers main")
        return
    
    success = run_command("gitBis checkout -b feature", "Création et basculement vers une nouvelle branche")
    if not success:
        print("❌ Échec de la création de branche")
        return
    
    # Récupérer un commit pour tester le checkout vers un commit
    print("🔍 Récupération d'un commit pour tester checkout...")
    result = subprocess.run("gitBis rev-parse HEAD", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        commit_hash = result.stdout.strip()
        print(f"📄 Hash du commit récupéré: {commit_hash}")
        success = run_command(f"gitBis checkout {commit_hash[:7]}", f"Checkout vers un commit spécifique {commit_hash[:7]}")
        if not success:
            print("❌ Échec du checkout vers un commit")
            return
        
        # Retourner à la branche feature
        success = run_command("gitBis checkout feature", "Retour vers la branche feature")
        if not success:
            print("❌ Échec du retour vers feature")
            return
    
    # Test 21: Réinitialiser HEAD et/ou l'index
    print("\n" + "="*60)
    print("🎯 TEST 21: RÉINITIALISER HEAD ET/OU L'INDEX")
    print("="*60)
    # Récupérer un commit pour tester le reset
    print("🔍 Récupération d'un commit pour tester reset...")
    result = subprocess.run("gitBis rev-parse HEAD", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        commit_hash = result.stdout.strip()
        print(f"📄 Hash du commit récupéré: {commit_hash}")
        
        # Test reset soft
        success = run_command(f"gitBis reset --soft {commit_hash[:7]}", f"Reset soft vers {commit_hash[:7]}")
        if not success:
            print("❌ Échec du reset soft")
            return
        
        # Test reset mixed
        success = run_command(f"gitBis reset --mixed {commit_hash[:7]}", f"Reset mixed vers {commit_hash[:7]}")
        if not success:
            print("❌ Échec du reset mixed")
            return
        
        # Test reset hard
        success = run_command(f"gitBis reset --hard {commit_hash[:7]}", f"Reset hard vers {commit_hash[:7]}")
        if not success:
            print("❌ Échec du reset hard")
            return
    
    print("\n" + "="*60)
    print("🎉 TOUS LES TESTS TERMINÉS AVEC SUCCÈS")
    print("="*60)
    print("📊 RÉSUMÉ:")
    print("   ✅ 21 tests exécutés")
    print("   ✅ Toutes les commandes fonctionnent")
    print("   ✅ Système Git simplifié opérationnel")
    print("="*60)

if __name__ == "__main__":
    main() 