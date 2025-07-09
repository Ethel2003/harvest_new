# Tests API - Scripts de Test pour les Endpoints

Ce dossier contient des scripts de test complets pour tester les endpoints API des modèles **Groupe**, **Etape**, **Tag** et **Departement**.

## 📁 Fichiers disponibles

### Scripts de test individuels
- `test_groupe_api.py` - Tests pour le modèle Groupe
- `test_etape_api.py` - Tests pour le modèle Etape  
- `test_tag_api.py` - Tests pour le modèle Tag
- `test_departement_api.py` - Tests pour le modèle Departement

### Script principal
- `run_all_api_tests.py` - Exécute tous les tests en une seule fois

## 🚀 Prérequis

1. **Serveur Django démarré** sur `http://localhost:8000`
2. **Authentification configurée** avec un utilisateur existant
3. **Dépendances Python** installées (`requests`)

## 📋 Fonctionnalités testées

### Pour chaque modèle, les scripts testent :

#### 🔧 Opérations CRUD de base
- ✅ **CREATE** - Création d'un nouvel enregistrement
- ✅ **READ** - Lecture de la liste et d'un enregistrement spécifique
- ✅ **UPDATE** - Mise à jour d'un enregistrement
- ✅ **DELETE** - Suppression d'un enregistrement

#### 🔍 Fonctionnalités avancées
- ✅ **Recherche** - Recherche par texte dans les champs
- ✅ **Tri** - Tri par différents champs
- ✅ **Filtrage** - Filtrage par critères spécifiques
- ✅ **Pagination** - Gestion de la pagination des résultats

#### 🎯 Actions personnalisées (selon le modèle)
- **Groupe** : Ajout/retrait de membres
- **Etape** : Création multiple
- **Tag** : Filtrage par couleur
- **Departement** : Récupération des membres

## 🛠️ Utilisation

### Option 1 : Exécuter tous les tests
```bash
cd scriptsTests
python run_all_api_tests.py
```

### Option 2 : Exécuter un test spécifique
```bash
cd scriptsTests

# Test des groupes
python test_groupe_api.py

# Test des étapes
python test_etape_api.py

# Test des tags
python test_tag_api.py

# Test des départements
python test_departement_api.py
```

## 🔐 Configuration de l'authentification

Les scripts utilisent par défaut :
- **Email** : `utilisateur1@example.com`
- **Mot de passe** : `motdepasse`

Pour modifier ces paramètres, éditez la fonction `login()` dans chaque script :

```python
def login():
    login_data = {
        "email": "votre_email@example.com", 
        "password": "votre_mot_de_passe"
    }
    # ...
```

## 📊 Structure des tests

Chaque script suit cette structure :

1. **Authentification** - Obtention du token d'accès
2. **Test de création** - Création d'un enregistrement de test
3. **Test de lecture** - Récupération de la liste et de l'enregistrement créé
4. **Test de mise à jour** - Modification de l'enregistrement
5. **Tests de recherche/tri** - Fonctionnalités de filtrage
6. **Tests d'actions personnalisées** - Fonctionnalités spécifiques au modèle
7. **Test de suppression** - Nettoyage de l'enregistrement de test
8. **Tests de création multiple** - Tests d'import par lots

## 🎯 Endpoints testés

### Groupe (`/api/groupes/`)
- `GET /groupes/` - Liste des groupes
- `POST /groupes/` - Création d'un groupe
- `GET /groupes/{id}/` - Détails d'un groupe
- `PATCH /groupes/{id}/` - Mise à jour d'un groupe
- `DELETE /groupes/{id}/` - Suppression d'un groupe
- `POST /groupes/{id}/insert_membre/` - Ajouter un membre
- `POST /groupes/{id}/remove_membre/` - Retirer un membre

### Etape (`/api/etapes/`)
- `GET /etapes/` - Liste des étapes
- `POST /etapes/` - Création d'une étape
- `GET /etapes/{id}/` - Détails d'une étape
- `PATCH /etapes/{id}/` - Mise à jour d'une étape
- `DELETE /etapes/{id}/` - Suppression d'une étape
- `POST /etapes/store_multiple/` - Création multiple

### Tag (`/api/tags/`)
- `GET /tags/` - Liste des tags
- `POST /tags/` - Création d'un tag
- `GET /tags/{id}/` - Détails d'un tag
- `PATCH /tags/{id}/` - Mise à jour d'un tag
- `DELETE /tags/{id}/` - Suppression d'un tag
- `POST /tags/store_multiple/` - Création multiple

### Departement (`/api/departements/`)
- `GET /departements/` - Liste des départements
- `POST /departements/` - Création d'un département
- `GET /departements/{id}/` - Détails d'un département
- `PATCH /departements/{id}/` - Mise à jour d'un département
- `DELETE /departements/{id}/` - Suppression d'un département
- `GET /departements/{id}/membres/` - Membres du département
- `POST /departements/store_multiple/` - Création multiple

## 📝 Exemple de sortie

```
🚀 Démarrage des tests API pour le modèle Groupe
==================================================
✅ Authentification réussie

🔧 Test de création d'un groupe...
Status: 201
✅ Groupe créé avec succès
ID: 1

📋 Test de récupération de la liste des groupes...
Status: 200
✅ 5 groupes récupérés

👥 Test de récupération du groupe 1...
Status: 200
✅ Groupe récupéré avec succès
Nom: Groupe Test

✏️ Test de mise à jour du groupe 1...
Status: 200
✅ Groupe mis à jour avec succès

🔍 Test de recherche de groupes...
Status: 200
✅ 1 groupes trouvés pour 'Test'

📊 Test de tri des groupes...
Status: 200
✅ 5 groupes triés par nom

👤 Test d'ajout d'un membre au groupe 1...
Status: 200
✅ Membre ajouté au groupe avec succès

👤 Test de retrait d'un membre du groupe 1...
Status: 200
✅ Membre retiré du groupe avec succès

🗑️ Test de suppression du groupe 1...
Status: 200
✅ Groupe supprimé avec succès

==================================================
✅ Tests terminés !
```

## ⚠️ Notes importantes

1. **Données de test** : Les scripts créent des données de test qui sont supprimées à la fin
2. **Authentification** : Assurez-vous d'avoir un utilisateur valide dans la base de données
3. **Dépendances** : Les modèles peuvent avoir des relations (ex: Groupe nécessite un Critere)
4. **Serveur** : Le serveur Django doit être démarré avant d'exécuter les tests

## 🐛 Dépannage

### Erreur d'authentification
- Vérifiez que l'utilisateur existe dans la base de données
- Modifiez les credentials dans la fonction `login()`

### Erreur de connexion
- Vérifiez que le serveur Django est démarré sur `http://localhost:8000`
- Vérifiez que l'API est accessible

### Erreur de dépendance
- Certains modèles nécessitent des données préexistantes (ex: Critere pour Groupe)
- Créez d'abord les données requises dans l'admin Django

## 📈 Améliorations possibles

- Ajout de tests de validation des données
- Tests de gestion des erreurs
- Tests de performance
- Tests de sécurité (autorisations)
- Génération de rapports détaillés 