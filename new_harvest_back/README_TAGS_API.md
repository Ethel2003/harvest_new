# API Tags - Documentation Complète

## Vue d'ensemble

L'API Tags gère toutes les opérations liées aux tags de la plateforme communautaire. Elle fournit des fonctionnalités CRUD complètes ainsi que des endpoints spécialisés pour récupérer la totalité des tags avec des fonctionnalités avancées.

## Architecture

### ViewSet responsable
```python
class TagViewSet(BaseViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    search_fields = ['name']
    ordering_fields = ['name']
```

### Modèle Tag
```python
class Tag(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
```

## Endpoints Principaux

### 1. Endpoints CRUD Standards

#### **Liste des tags (avec pagination)**
```
GET /api/tags/
```

**Méthode appelée** : `BaseViewSet.list()`

**Fonctionnalités incluses** :
- ✅ Recherche dans `['name']`
- ✅ Tri par `['name']`
- ✅ Pagination automatique

**Paramètres de requête supportés** :
```
GET /api/tags/?search=tag1&ordering=name&page=1
```

#### **Créer un tag**
```
POST /api/tags/
```

**Corps de la requête** :
```json
{
    "name": "Nouveau Tag"
}
```

#### **Récupérer un tag spécifique**
```
GET /api/tags/{id}/
```

#### **Mettre à jour un tag**
```
PUT /api/tags/{id}/
PATCH /api/tags/{id}/
```

#### **Supprimer un tag**
```
DELETE /api/tags/{id}/
```

### 2. Endpoints Spécialisés

#### **A. Récupérer tous les tags (sans pagination)**
```
GET /api/tags/tous_les_tags/
```

**Description** : Récupère la totalité des tags sans pagination, idéal pour les listes déroulantes et les filtres.

**Paramètres de requête optionnels** :
- `search` : Recherche dans le nom des tags
- `ordering` : Tri (`name`, `-name`)
- `avec_membres` : `true/false` pour inclure le nombre de membres par tag

**Exemples d'utilisation** :
```bash
# Tous les tags
GET /api/tags/tous_les_tags/

# Recherche
GET /api/tags/tous_les_tags/?search=jeune

# Tri décroissant
GET /api/tags/tous_les_tags/?ordering=-name

# Avec nombre de membres
GET /api/tags/tous_les_tags/?avec_membres=true
```

**Réponse** :
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Jeune",
            "nombre_membres": 15  // Si avec_membres=true
        }
    ],
    "total": 25,
    "filtres_appliques": {
        "search": "",
        "ordering": "name",
        "avec_membres": false
    }
}
```

#### **B. Statistiques des tags**
```
GET /api/tags/statistiques/
```

**Description** : Fournit des statistiques détaillées sur l'utilisation des tags.

**Réponse** :
```json
{
    "success": true,
    "data": {
        "total_tags": 50,
        "tags_populaires": [
            {
                "id": 1,
                "name": "Jeune",
                "nombre_membres": 25
            }
        ],
        "tags_non_utilises": 10,
        "repartition": {
            "0_membre": 10,
            "1_5_membres": 20,
            "6_10_membres": 15,
            "plus_de_10_membres": 5
        }
    }
}
```

#### **C. Tags avec nombre de membres**
```
GET /api/tags/avec_membres/
```

**Description** : Récupère tous les tags avec le nombre de membres associés et des filtres avancés.

**Paramètres de requête optionnels** :
- `min_membres` : Nombre minimum de membres (filtre)
- `max_membres` : Nombre maximum de membres (filtre)
- `ordering` : Tri (`nombre_membres`, `-nombre_membres`, `name`, `-name`)

**Exemples d'utilisation** :
```bash
# Tous les tags avec membres
GET /api/tags/avec_membres/

# Tags avec au moins 5 membres
GET /api/tags/avec_membres/?min_membres=5

# Tags populaires (tri par nombre de membres décroissant)
GET /api/tags/avec_membres/?ordering=-nombre_membres

# Tags avec entre 1 et 10 membres
GET /api/tags/avec_membres/?min_membres=1&max_membres=10
```

**Réponse** :
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Jeune",
            "nombre_membres": 25
        }
    ],
    "total": 40,
    "filtres_appliques": {
        "min_membres": "1",
        "max_membres": null,
        "ordering": "nombre_membres"
    }
}
```

#### **D. Créer plusieurs tags**
```
POST /api/tags/creer_multiple/
```

**Description** : Crée plusieurs tags en une seule requête, évite les doublons.

**Corps de la requête** :
```json
{
    "tags": [
        "Tag 1",
        "Tag 2",
        "Tag 3"
    ]
}
```

**Réponse** :
```json
{
    "success": true,
    "message": "3 tags créés avec succès",
    "data": {
        "tags_crees": [
            {
                "id": 51,
                "name": "Tag 1"
            }
        ],
        "tags_existants": 0,
        "total_traites": 3
    }
}
```

## Cas d'Usage Recommandés

### 1. **Listes déroulantes et filtres**
```bash
GET /api/tags/tous_les_tags/
```
- **Utilisation** : Pour les interfaces utilisateur nécessitant tous les tags
- **Avantage** : Pas de pagination, réponse rapide

### 2. **Tableaux de bord et statistiques**
```bash
GET /api/tags/statistiques/
```
- **Utilisation** : Pour afficher des métriques sur l'utilisation des tags
- **Avantage** : Données agrégées optimisées

### 3. **Gestion des tags populaires**
```bash
GET /api/tags/avec_membres/?ordering=-nombre_membres&min_membres=1
```
- **Utilisation** : Pour identifier les tags les plus utilisés
- **Avantage** : Filtrage et tri avancés

### 4. **Import en masse de tags**
```bash
POST /api/tags/creer_multiple/
```
- **Utilisation** : Pour importer des listes de tags depuis des fichiers
- **Avantage** : Gestion des doublons automatique

## Authentification

Tous les endpoints nécessitent une **authentification par token** :
```bash
Authorization: Token votre_token_ici
Content-Type: application/json
```

## Gestion d'Erreurs

### Codes de statut HTTP

- **200** : Succès
- **201** : Créé avec succès
- **400** : Requête invalide
- **401** : Non authentifié
- **403** : Non autorisé
- **404** : Ressource non trouvée
- **500** : Erreur serveur

### Format des erreurs
```json
{
    "success": false,
    "error": "Message d'erreur détaillé"
}
```

## Performance

### Optimisations implémentées

1. **Requêtes optimisées** : Utilisation d'annotations Django pour éviter les requêtes N+1
2. **Filtrage côté base de données** : Tous les filtres sont appliqués au niveau SQL
3. **Pagination intelligente** : Endpoints avec et sans pagination selon les besoins
4. **Cache des requêtes** : Possibilité d'ajouter du cache Redis pour les statistiques

### Recommandations d'utilisation

- **Pour les interfaces utilisateur** : Utilisez `/tous_les_tags/` sans pagination
- **Pour les analyses** : Utilisez `/statistiques/` pour les métriques
- **Pour les filtres avancés** : Utilisez `/avec_membres/` avec les paramètres appropriés

## Tests

Un script de test complet est disponible :
```bash
python scriptsTests/test_tags_endpoints.py
```

Ce script teste tous les endpoints et mesure les performances.

## Migration et Compatibilité

### Endpoints existants
- ✅ Tous les endpoints CRUD standards restent fonctionnels
- ✅ Aucune breaking change

### Nouveaux endpoints
- 🆕 `/tous_les_tags/` : Nouveau endpoint pour récupérer tous les tags
- 🆕 `/statistiques/` : Nouveau endpoint pour les statistiques
- 🆕 `/avec_membres/` : Nouveau endpoint avec filtres avancés
- 🆕 `/creer_multiple/` : Nouveau endpoint pour création en masse

## Support et Maintenance

Pour toute question ou problème :
1. Consultez les logs Django pour les erreurs détaillées
2. Utilisez le script de test pour diagnostiquer les problèmes
3. Vérifiez l'authentification et les permissions

---

**Version** : 1.0  
**Dernière mise à jour** : Décembre 2024  
**Auteur** : Équipe de développement Harvest 