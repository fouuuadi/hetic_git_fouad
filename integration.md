# Plan d'intégration des commandes Git

fichier realiser par fouad 

## 📊 ÉTAT D'AVANCEMENT - COMMANDES INTÉGRÉES ET TESTÉES ✅

**8 commandes sur 17 intégrées et fonctionnelles :**

1. ✅ **Initialiser un dépôt** - `gitBis init`
2. ✅ **Ajouter un fichier au staging** - `gitBis add`
3. ✅ **Vérifier l'état du dépôt** - `gitBis status`
4. ✅ **Créer un blob et calculer son SHA-1** - `gitBis hash-object`
5. ✅ **Afficher un objet Git** - `gitBis cat-file`
6. ✅ **Générer un arbre (tree) depuis l'index** - `gitBis write-tree`
7. ✅ **Créer un commit** - `gitBis commit-tree`
8. ✅ **Lister les fichiers suivis** - `gitBis ls-files`

**Tests validés :** Toutes les commandes ont été testées individuellement et fonctionnent parfaitement.
**Progression :** 47% des commandes du plan d'intégration sont opérationnelles.

---

Ce document liste, étape par étape, les commandes Git à intégrer successivement pour comprendre et tester les différentes fonctionnalités de Git.

1. **Initialiser un dépôt**

   ```bash
   git init [<dir>]
   ```

2. **Ajouter un fichier au staging**

   ```bash
   git add <file>
   ```

3. **Vérifier l’état du dépôt**

   ```bash
   git status
   ```

4. **Ignorer des fichiers**

   ```bash
   # Créez un fichier .gitignore puis ajoutez un pattern
   echo "*.log" > .gitignore
   git add .gitignore
   ```

5. **Créer un blob et calculer son SHA-1**

   ```bash
   git hash-object <file>
   git hash-object -w <file>
   ```

6. **Afficher un objet Git**

   ```bash
   git cat-file -t <oid>
   git cat-file -p <oid>
   ```

7. **Générer un arbre (tree) depuis l’index**

   ```bash
   git write-tree
   ```

8. **Créer un commit**

   ```bash
   git commit-tree <tree_sha> -m "Message"
   ```

9. **Commit via la commande porcelain**

   ```bash
   git commit -m "Message"
   ```

10. **Lister les fichiers suivis**

    ```bash
    git ls-files
    ```

11. **Convertir une référence en SHA-1**

    ```bash
    git rev-parse <ref>
    ```

12. **Afficher les références**

    ```bash
    git show-ref
    ```

13. **Afficher l’historique des commits**

    ```bash
    git log --oneline
    ```

14. **Lister le contenu d’un tree**

    ```bash
    git ls-tree <tree_sha>
    ```

15. **Basculer de branche ou créer une branche**

    ```bash
    git checkout [-b] <branch|sha>
    ```

16. **Réinitialiser HEAD et/ou l’index**

    ```bash
    git reset [--soft|--mixed|--hard] <sha>
    ```

17. **Fusionner une branche**

    ```bash
    git merge <branch>
    ```

---

*Fin du plan d’intégration.*
