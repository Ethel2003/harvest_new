# Guide d'Implémentation - Endpoints de Filtrage des Membres

Ce guide explique comment les nouveaux endpoints de filtrage ont été implémentés et comment les utiliser.

## 🎯 Objectif

Implémenter les endpoints de filtrage des membres selon les spécifications :
- `GET /api/membres/?groupes[]=1&groupes[]=2` : Filtrage par groupes
- `GET /api/membres/?etapes[]=1&etapes[]=2` : Filtrage par étapes  
- `GET /api/membres/?tags[]=1&tags[]=2` : Filtrage par tags
- `GET /api/membres/?groupes[]=1&etapes[]=1&tags[]=1` : Filtrage combiné

## 🏗️ Architecture Implémentée

### 1. Modification du MembreViewSet

**Fichier :** `core/views.py`

#### A. Surcharge de `get_queryset()`
```python
def get_queryset(self):
    """
    Surcharge de get_queryset pour supporter les filtres par groupes, étapes et tags
    """
    queryset = super().get_queryset()
    
    # Récupération des paramètres de filtrage
    groupes = self.request.query_params.getlist('groupes[]')
    etapes = self.request.query_params.getlist('etapes[]')
    tags = self.request.query_params.getlist('tags[]')
    
    # Filtrage par groupes (via le modèle Regroupements)
    if groupes:
        queryset = queryset.filter(regroupements__groupe_id__in=groupes, regroupements__actif=True).distinct()
    
    # Filtrage par étapes (via le modèle Integration)
    if etapes:
        queryset = queryset.filter(integration__etape_id__in=etapes).distinct()
    
    # Filtrage par tags (via le modèle Etiquetage)
    if tags:
        queryset = queryset.filter(etiquetage__tag_id__in=tags).distinct()
    
    return queryset
```

#### B. Endpoints Spécifiques
Quatre nouveaux endpoints ont été ajoutés :

1. **`par_groupes`** : Filtrage dédié par groupes
2. **`par_etapes`** : Filtrage dédié par étapes
3. **`par_tags`** : Filtrage dédié par tags
4. **`filtres_combines`** : Filtrage combiné flexible

### 2. Modèles de Relations Utilisés

- **Regroupements** : Relation many-to-many entre Membres et Groupes
- **Integration** : Relation many-to-many entre Membres et Étapes
- **Etiquetage** : Relation many-to-many entre Membres et Tags

## 🚀 Utilisation

### 1. Préparation de l'Environnement

```bash
# Aller dans le répertoire du projet
cd new_harvest_back

# Activer l'environnement virtuel (si applicable)
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur (si nécessaire)
python manage.py createsuperuser
```

### 2. Création de Données de Test

```bash
# Créer des données de test
python scriptsTests/creer_donnees_test.py --create

# Ou nettoyer puis créer
python scriptsTests/creer_donnees_test.py --clean --create
```

### 3. Démarrage du Serveur

```bash
# Démarrer le serveur de développement
python manage.py runserver
```

### 4. Test des Endpoints

#### A. Authentification
```bash
# Obtenir un token d'authentification
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}'
```

#### B. Tests des Endpoints

```bash
# Token obtenu précédemment
TOKEN="votre_token_ici"

# 1. Filtrage par groupes
curl -X GET "http://localhost:8000/api/membres/par_groupes/?groupes[]=1&groupes[]=2" \
  -H "Authorization: Token $TOKEN"

# 2. Filtrage par étapes
curl -X GET "http://localhost:8000/api/membres/par_etapes/?etapes[]=1&etapes[]=2" \
  -H "Authorization: Token $TOKEN"

# 3. Filtrage par tags
curl -X GET "http://localhost:8000/api/membres/par_tags/?tags[]=1&tags[]=2" \
  -H "Authorization: Token $TOKEN"

# 4. Filtrage combiné
curl -X GET "http://localhost:8000/api/membres/filtres_combines/?groupes[]=1&etapes[]=1&tags[]=1" \
  -H "Authorization: Token $TOKEN"

# 5. Endpoint principal avec filtres
curl -X GET "http://localhost:8000/api/membres/?groupes[]=1&etapes[]=1&tags[]=1" \
  -H "Authorization: Token $TOKEN"
```

### 5. Tests Automatisés

```bash
# Lancer les tests automatisés
python scriptsTests/test_filtres_membres.py
```

## 📋 Endpoints Disponibles

### Endpoint Principal avec Filtres
- **URL :** `GET /api/membres/`
- **Paramètres :** `groupes[]`, `etapes[]`, `tags[]`
- **Description :** Endpoint principal supportant tous les filtres

### Endpoints Spécifiques

#### 1. Filtrage par Groupes
- **URL :** `GET /api/membres/par_groupes/`
- **Paramètres :** `groupes[]` (obligatoire)
- **Exemple :** `?groupes[]=1&groupes[]=2`

#### 2. Filtrage par Étapes
- **URL :** `GET /api/membres/par_etapes/`
- **Paramètres :** `etapes[]` (obligatoire)
- **Exemple :** `?etapes[]=1&etapes[]=3`

#### 3. Filtrage par Tags
- **URL :** `GET /api/membres/par_tags/`
- **Paramètres :** `tags[]` (obligatoire)
- **Exemple :** `?tags[]=1&tags[]=4`

#### 4. Filtrage Combiné
- **URL :** `GET /api/membres/filtres_combines/`
- **Paramètres :** `groupes[]`, `etapes[]`, `tags[]` (au moins un obligatoire)
- **Exemple :** `?groupes[]=1&etapes[]=2&tags[]=3`

## 🔧 Fonctionnalités Implémentées

### 1. Gestion des Erreurs
- Validation des paramètres requis
- Messages d'erreur explicites
- Gestion des exceptions

### 2. Performance
- Utilisation de `.distinct()` pour éviter les doublons
- Filtrage sur les regroupements actifs uniquement
- Requêtes optimisées

### 3. Pagination
- Support de la pagination standard DRF
- Paramètres `page` et `page_size`

### 4. Réponses Structurées
```json
{
  "success": true,
  "data": [...],
  "filtres_appliques": {
    "groupes": ["1", "2"],
    "etapes": ["1"],
    "tags": ["3"],
    "nombre_membres": 5
  }
}
```

## 🧪 Tests et Validation

### 1. Tests Manuels
- Utilisation de curl ou Postman
- Vérification des réponses JSON
- Test des cas d'erreur

### 2. Tests Automatisés
- Script `test_filtres_membres.py`
- Tests de tous les endpoints
- Validation des données retournées

### 3. Données de Test
- Script `creer_donnees_test.py`
- Données cohérentes pour les tests
- Relations multiples pour tester les filtres

## 📊 Exemples de Réponses

### Succès
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nom": "Dupont",
      "prenom": "Jean",
      "email": "jean.dupont@test.com",
      "telephone": "0123456789",
      "genre": "masculin",
      "statut": "membre"
    }
  ],
  "filtres_appliques": {
    "groupes": ["1", "2"],
    "nombre_membres": 1
  }
}
```

### Erreur
```json
{
  "success": false,
  "error": "Aucun groupe spécifié. Utilisez le paramètre groupes[]"
}
```

## 🔍 Débogage

### 1. Logs Django
```bash
# Activer les logs SQL
python manage.py runserver --verbosity=2
```

### 2. Vérification des Données
```python
# Dans le shell Django
python manage.py shell

from core.models import *
print(f"Membres: {Membre.objects.count()}")
print(f"Regroupements: {Regroupements.objects.count()}")
print(f"Intégrations: {Integration.objects.count()}")
print(f"Étiquetages: {Etiquetage.objects.count()}")
```

### 3. Test des Requêtes
```python
# Tester les filtres directement
membres_groupes = Membre.objects.filter(
    regroupements__groupe_id__in=[1, 2],
    regroupements__actif=True
).distinct()
print(f"Membres dans les groupes 1 et 2: {membres_groupes.count()}")
```

## 🚀 Intégration Frontend

### JavaScript/TypeScript
```javascript
// Fonction utilitaire pour les filtres
const getMembresFiltres = async (filtres) => {
  const params = new URLSearchParams();
  
  if (filtres.groupes) {
    filtres.groupes.forEach(id => params.append('groupes[]', id));
  }
  if (filtres.etapes) {
    filtres.etapes.forEach(id => params.append('etapes[]', id));
  }
  if (filtres.tags) {
    filtres.tags.forEach(id => params.append('tags[]', id));
  }
  
  const response = await fetch(`/api/membres/filtres_combines/?${params}`, {
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  return response.json();
};

// Utilisation
const resultat = await getMembresFiltres({
  groupes: [1, 2],
  etapes: [1],
  tags: [3]
});
```

## 📝 Notes Importantes

1. **Authentification** : Tous les endpoints nécessitent un token d'authentification
2. **Regroupements actifs** : Seuls les regroupements avec `actif=True` sont pris en compte
3. **Distinct** : Les doublons sont automatiquement éliminés
4. **Performance** : Les requêtes sont optimisées pour de grandes quantités de données
5. **Extensibilité** : L'architecture permet d'ajouter facilement de nouveaux filtres

## 🔄 Maintenance

### Ajout de Nouveaux Filtres
1. Modifier `get_queryset()` dans `MembreViewSet`
2. Ajouter les paramètres de requête
3. Implémenter la logique de filtrage
4. Ajouter les tests correspondants

### Mise à Jour des Modèles
1. Vérifier la cohérence des relations
2. Mettre à jour les filtres si nécessaire
3. Tester avec les nouvelles données

## 📚 Documentation Complémentaire

- `README_ENDPOINTS_FILTRAGE.md` : Documentation détaillée des endpoints
- `scriptsTests/test_filtres_membres.py` : Tests automatisés
- `scriptsTests/creer_donnees_test.py` : Gestion des données de test 