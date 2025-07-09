# API Membres - Documentation

## Vue d'ensemble

L'API Membres gère toutes les opérations liées aux membres de la plateforme communautaire. Elle fournit des fonctionnalités CRUD complètes ainsi que des opérations spécialisées pour la gestion des relations (tags, étapes, groupes, etc.).

## Architecture

### ViewSet responsable
```python
class MembreViewSet(BaseViewSet):
    queryset = Membre.objects.all()
    serializer_class = MembreSerializer
    search_fields = ['nom', 'prenom', 'email', 'telephone']
    ordering_fields = ['nom', 'prenom', 'created_at', 'updated_at']
```

### Modèle Membre
```python
class Membre(models.Model):
    nom = models.CharField(max_length=255, null=True, blank=True)
    prenom = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=255, null=True, blank=True)
    profession = models.CharField(max_length=255, null=True, blank=True)
    nationalite = models.CharField(max_length=255, null=True, blank=True)
    genre = models.CharField(max_length=10, choices=GENRE_CHOICES, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    situation_matrimoniale = models.CharField(max_length=20, choices=SITUATION_CHOICES, null=True, blank=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='inscrit')
    
    class Meta:
        unique_together = ['nom', 'prenom']  # Contrainte d'unicité
```

## Endpoints principaux

### 1. Liste des membres
```
GET /api/membres/
```

**Méthode appelée** : `BaseViewSet.list()`

**Fonctionnalités incluses** :
- ✅ Recherche dans `['nom', 'prenom', 'email', 'telephone']`
- ✅ Tri par `['nom', 'prenom', 'created_at', 'updated_at']`
- ✅ Pagination automatique
- ✅ Filtrage avancé

**Paramètres de requête supportés** :
```
GET /api/membres/?search=john&ordering=nom&page=1
```

**Réponse typique** :
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/membres/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "nom": "Doe",
      "prenom": "John",
      "email": "john@example.com",
      "telephone": "123456789",
      "genre": "masculin",
      "situation_matrimoniale": "celibataire",
      "statut": "membre",
      "created_at": "2024-01-27T10:00:00Z",
      "updated_at": "2024-01-27T10:00:00Z"
    }
  ]
}
```

### 2. Statistiques des membres
```
GET /api/membres/statistiques/
```

**Méthode appelée** : `MembreViewSet.statistiques()`

**Fonctionnalités** :
- 📊 Total exact de membres
- 📈 Répartition par genre (Masculin/Féminin)
- 🎯 Répartition par statut (Inscrit/Membre)
- 📅 Répartition par situation matrimoniale (Célibataire/Marié)
- 🎂 Répartition par âge (tranches d'âge)
- 🏷️ Répartition par tags
- 📍 Répartition par départements (via Serviteurs)
- 👥 Répartition par groupes (via Regroupements)
- 📊 Statistiques globales détaillées

**Réponse typique** :
```json
{
  "success": true,
  "data": {
    "statistiques_globales": {
      "total_membres": 150,
      "membres_avec_email": 120,
      "membres_avec_telephone": 140,
      "membres_avec_date_naissance": 100,
      "membres_avec_conjoint": 60,
      "membres_avec_enfants": 45
    },
    "repartition_genre": {
      "Masculin": 75,
      "Féminin": 75
    },
    "repartition_statut": {
      "Inscrit": 50,
      "Membre": 100
    },
    "repartition_situation": {
      "Célibataire": 80,
      "Marié(e)": 70
    },
    "repartition_age": {
      "moins_18": 10,
      "18_25": 30,
      "26_35": 45,
      "36_50": 35,
      "plus_50": 20,
      "total_avec_age": 100
    },
    "membres_par_tag": [
      {
        "tag": "Jeune",
        "nombre": 45
      },
      {
        "tag": "Leader",
        "nombre": 25
      }
    ],
    "membres_par_departement": [
      {
        "departement": "Musique",
        "nombre": 25
      },
      {
        "departement": "Accueil",
        "nombre": 15
      }
    ],
    "membres_par_groupe": [
      {
        "groupe": "Groupe A",
        "nombre": 30
      },
      {
        "groupe": "Groupe B",
        "nombre": 25
      }
    ]
  }
}
```

**Fonctionnalités avancées** :
- ✅ Calcul automatique des âges basé sur `date_naissance`
- ✅ Comptage distinct pour éviter les doublons
- ✅ Gestion des erreurs pour chaque type de statistique
- ✅ Optimisation des requêtes avec `annotate` et `Count`
- ✅ Filtrage des relations actives (Serviteurs et Regroupements)

### 3. Création d'un membre
```
POST /api/membres/
```

**Méthode appelée** : `MembreViewSet.create()`

**Validation** :
- ✅ Contrainte d'unicité nom/prénom
- ✅ Validation des champs obligatoires
- ✅ Gestion des erreurs d'intégrité

**Corps de la requête** :
```json
{
  "nom": "Doe",
  "prenom": "John",
  "email": "john@example.com",
  "telephone": "123456789",
  "genre": "masculin",
  "situation_matrimoniale": "celibataire"
}
```

### 4. Mise à jour d'un membre
```
PUT /api/membres/{id}/
PATCH /api/membres/{id}/
```

**Méthode appelée** : `MembreViewSet.update()`

### 5. Suppression d'un membre
```
DELETE /api/membres/{id}/
```

**Méthode appelée** : `MembreViewSet.destroy()`

## Endpoints spécialisés

### 1. Gestion des tags
```
POST /api/membres/taged_multiple/
POST /api/membres/{id}/untaged_multiple/
```

### 2. Gestion des étapes
```
POST /api/membres/{id}/store_multiple_etapes/
DELETE /api/membres/{id}/delete_etape/{etape_id}/
```

### 3. Opérations en masse
```
POST /api/membres/store_multiple/
POST /api/membres/destroy_multiple/
```

## Flux d'exécution pour GET /api/membres/

1. **Requête HTTP** : `GET /api/membres/`
2. **Router Django REST** : Route vers `MembreViewSet`
3. **MembreViewSet** : Hérite de `BaseViewSet`
4. **BaseViewSet.list()** : Méthode appelée automatiquement
5. **Filtrage** : `self.filter_queryset(self.get_queryset())`
6. **Sérialisation** : `MembreSerializer` appliqué
7. **Réponse** : Liste des membres au format JSON

## Gestion des erreurs

### Erreur d'unicité
```json
{
  "success": false,
  "error": "Un membre avec cette combinaison nom/prénom existe déjà.",
  "details": "La combinaison nom et prénom doit être unique."
}
```

### Erreur de validation
```json
{
  "nom": ["Ce champ est obligatoire."],
  "email": ["Saisissez une adresse e-mail valide."]
}
```

## Sécurité

- **Authentification requise** pour toutes les opérations
- **Permissions** : Gestion des droits d'accès
- **Validation** : Contrôle strict des données d'entrée
- **Sanitisation** : Protection contre les injections

## Performance

- **Requêtes optimisées** avec `select_related` et `prefetch_related`
- **Pagination** pour éviter les surcharges
- **Indexation** sur les champs de recherche
- **Cache** possible pour les statistiques

## Exemples d'utilisation

### Recherche de membres
```bash
curl -X GET "http://localhost:8000/api/membres/?search=john&ordering=nom" \
  -H "Authorization: Token your_token_here"
```

### Récupération des statistiques
```bash
curl -X GET "http://localhost:8000/api/membres/statistiques/" \
  -H "Authorization: Token your_token_here"
```

### Création d'un membre
```bash
curl -X POST "http://localhost:8000/api/membres/" \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Doe",
    "prenom": "John",
    "email": "john@example.com",
    "telephone": "123456789"
  }'
```

---

**Date de création** : 2024-01-27  
**Version** : 1.0  
**Auteur** : Assistant IA 