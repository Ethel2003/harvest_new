# Scripts de Test CRUD - Integration et Etiquetage

Ce dossier contient des scripts de test pour vérifier les opérations CRUD (Create, Read, Update, Delete) des modèles `Integration` et `Etiquetage`.

## 📁 Fichiers Disponibles

### 1. `test_crud_integration_etiquetage.py`
**Script de test complet et automatisé**
- ✅ Tests CRUD complets pour Integration et Etiquetage
- ✅ Création automatique des données de test
- ✅ Tests d'opérations avancées (création multiple, recherche)
- ✅ Nettoyage automatique des données de test
- ✅ Gestion d'erreurs complète

### 2. `test_crud_simple.py`
**Script de test simple et rapide**
- ✅ Tests CRUD de base
- ✅ Interface interactive
- ✅ Configuration manuelle des IDs
- ✅ Tests rapides pour développement

### 3. `obtenir_ids.py`
**Script utilitaire pour obtenir les IDs**
- ✅ Affichage de tous les IDs existants
- ✅ Statistiques de la base de données
- ✅ Configuration recommandée pour les tests
- ✅ Visualisation des relations existantes

## 🚀 Utilisation

### Prérequis

1. **Serveur Django démarré**
   ```bash
   cd new_harvest_back
   python manage.py runserver
   ```

2. **Utilisateur admin créé**
   ```bash
   python manage.py createsuperuser
   # Email: admin@example.com
   # Password: admin123
   ```

3. **Données existantes** (optionnel)
   ```bash
   # Créer des données de test pour les filtres
   python scriptsTests/creer_donnees_test.py --create
   ```

### 1. Test Complet et Automatisé

```bash
# Lancer le test complet
python scriptsTests/test_crud_integration_etiquetage.py
```

**Ce que fait ce script :**
- 🔐 Authentification automatique
- 🔧 Création des données de test nécessaires
- 🧪 Tests CRUD complets pour Integration
- 🧪 Tests CRUD complets pour Etiquetage
- 🔄 Tests d'opérations avancées
- 🧹 Nettoyage automatique des données

### 2. Test Simple et Rapide

```bash
# Lancer le test simple
python scriptsTests/test_crud_simple.py
```

**Ce que fait ce script :**
- 📋 Affichage des instructions
- 🔐 Authentification
- 🧪 Tests de listage
- 🧪 Tests CRUD basiques
- ⚙️ Configuration manuelle des IDs

### 3. Obtenir les IDs Existants

```bash
# Afficher tous les IDs disponibles
python scriptsTests/obtenir_ids.py
```

**Ce que fait ce script :**
- 📊 Statistiques de la base
- 👥 Liste des membres avec IDs
- 📋 Liste des étapes avec IDs
- 🏷️ Liste des tags avec IDs
- 👥 Liste des groupes avec IDs
- 🔗 Relations existantes
- ⚙️ Configuration recommandée

## 📋 Opérations Testées

### Modèle Integration

| Opération | Endpoint | Méthode | Description |
|-----------|----------|---------|-------------|
| **CREATE** | `/api/integrations/` | POST | Créer une nouvelle intégration |
| **READ** | `/api/integrations/{id}/` | GET | Lire une intégration spécifique |
| **LIST** | `/api/integrations/` | GET | Lister toutes les intégrations |
| **UPDATE** | `/api/integrations/{id}/` | PATCH | Mettre à jour une intégration |
| **DELETE** | `/api/integrations/{id}/` | DELETE | Supprimer une intégration |
| **CREATE MULTIPLE** | `/api/integrations/store_multiple/` | POST | Créer plusieurs intégrations |

### Modèle Etiquetage

| Opération | Endpoint | Méthode | Description |
|-----------|----------|---------|-------------|
| **CREATE** | `/api/etiquetages/` | POST | Créer un nouvel étiquetage |
| **READ** | `/api/etiquetages/{id}/` | GET | Lire un étiquetage spécifique |
| **LIST** | `/api/etiquetages/` | GET | Lister tous les étiquetages |
| **UPDATE** | `/api/etiquetages/{id}/` | PATCH | Mettre à jour un étiquetage |
| **DELETE** | `/api/etiquetages/{id}/` | DELETE | Supprimer un étiquetage |
| **CREATE MULTIPLE** | `/api/etiquetages/store_multiple/` | POST | Créer plusieurs étiquetages |

## 🔧 Configuration

### Données de Test

Les scripts utilisent les données suivantes :

#### Integration
```python
{
    "membre": 1,                    # ID du membre
    "etape": 1,                     # ID de l'étape
    "created_at": "2024-01-01",     # Date de création
    "membership": False             # Statut d'adhésion
}
```

#### Etiquetage
```python
{
    "membre": 1,                    # ID du membre
    "tag": 1                        # ID du tag
}
```

### Modification des IDs

Pour utiliser des IDs spécifiques, modifiez les variables dans les scripts :

```python
# Dans test_crud_simple.py
membre_id = 1    # Remplacer par l'ID souhaité
etape_id = 1     # Remplacer par l'ID souhaité
tag_id = 1       # Remplacer par l'ID souhaité
```

## 📊 Exemples de Sortie

### Test Complet Réussi
```
🧪 TESTS CRUD - INTEGRATION ET ETIQUETAGE
============================================================
✅ Authentification réussie

🔧 Préparation des données de test...
  ✓ Membre créé: Test Membre (ID: 1)
  ✓ Étape créée: Étape Test 1 (ID: 1)
  ✓ Tag créé: Tag Test 1 (ID: 1)
✅ Données de test préparées

============================================================
🧪 TESTS CRUD - MODÈLE INTEGRATION
============================================================

1️⃣ Test CREATE - Créer une intégration
   Status: 201
   ✅ Intégration créée avec succès (ID: 1)
   Données: {'id': 1, 'membre': 1, 'etape': 1, ...}

2️⃣ Test READ - Lire l'intégration
   Status: 200
   ✅ Intégration récupérée avec succès

[... autres tests ...]

✅ Tests CRUD Integration terminés avec succès!
```

### Obtenir les IDs
```
🔍 OBTENIR LES IDs DE LA BASE DE DONNÉES
============================================================

📊 STATISTIQUES DE LA BASE DE DONNÉES:
--------------------------------------------------
Membres: 5
Étapes: 3
Tags: 4
Groupes: 2
Intégrations: 8
Étiquetages: 12

👥 MEMBRES DISPONIBLES:
--------------------------------------------------
ID:   1 | Jean Dupont | jean.dupont@test.com
ID:   2 | Marie Martin | marie.martin@test.com
ID:   3 | Pierre Bernard | pierre.bernard@test.com

⚙️ CONFIGURATION POUR LES TESTS:
--------------------------------------------------
Configuration recommandée pour les tests:
membre_id = 1  # Jean Dupont
etape_id = 1   # Accueil
tag_id = 1     # Actif
```

## 🐛 Dépannage

### Erreurs Courantes

#### 1. Erreur d'authentification
```
❌ Erreur de connexion: 422
```
**Solution :** Vérifiez que l'utilisateur admin existe avec les bonnes credentials.

#### 2. Erreur de données manquantes
```
❌ Impossible de créer l'intégration
```
**Solution :** Utilisez `obtenir_ids.py` pour vérifier les IDs existants.

#### 3. Erreur de serveur non démarré
```
❌ Erreur: Connection refused
```
**Solution :** Démarrez le serveur Django avec `python manage.py runserver`.

### Vérification des Données

```bash
# Vérifier les données existantes
python scriptsTests/obtenir_ids.py

# Créer des données de test si nécessaire
python scriptsTests/creer_donnees_test.py --create
```

## 🔄 Workflow de Test Recommandé

1. **Préparation**
   ```bash
   cd new_harvest_back
   python manage.py runserver
   ```

2. **Vérification des données**
   ```bash
   python scriptsTests/obtenir_ids.py
   ```

3. **Test complet**
   ```bash
   python scriptsTests/test_crud_integration_etiquetage.py
   ```

4. **Test rapide (si nécessaire)**
   ```bash
   python scriptsTests/test_crud_simple.py
   ```

## 📝 Notes Importantes

- **Authentification** : Tous les endpoints nécessitent un token d'authentification
- **Données de test** : Les scripts créent et nettoient automatiquement les données de test
- **IDs** : Utilisez `obtenir_ids.py` pour connaître les IDs existants
- **Erreurs** : Les scripts affichent des messages d'erreur détaillés
- **Nettoyage** : Les données de test sont automatiquement supprimées après les tests

## 🎯 Cas d'Usage

### Développement
- Tests rapides pendant le développement
- Vérification des endpoints après modifications
- Validation des nouvelles fonctionnalités

### Intégration Continue
- Tests automatisés dans les pipelines CI/CD
- Validation de la qualité du code
- Détection de régressions

### Maintenance
- Vérification du bon fonctionnement de l'API
- Tests après mises à jour
- Diagnostic des problèmes 