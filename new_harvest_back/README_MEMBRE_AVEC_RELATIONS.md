# Endpoint MEMBRE_AVEC_RELATIONS

## Description

L'endpoint `membre_avec_relations` permet de récupérer un membre spécifique avec toutes ses relations importantes : tags, étape actuelle, groupe d'appartenance et département d'appartenance.

## Route

```
GET /api/membres/{id}/membre_avec_relations/
```

## Paramètres

| Paramètre | Type | Description | Requis |
|-----------|------|-------------|--------|
| `id` | Integer | ID du membre à récupérer | ✅ |

## Authentification

**Requis** : Token d'authentification dans le header `Authorization`

```
Authorization: Token <votre_token>
```

## Réponse

### Structure de la réponse

```json
{
  "success": true,
  "data": {
    "membre": {
      "id": 1,
      "nom": "Doe",
      "prenom": "John",
      "email": "john.doe@example.com",
      "telephone": "+1234567890",
      "adresse": "123 Rue Example",
      "ville": "Paris",
      "profession": "Développeur",
      "nationalite": "Française",
      "genre": "M",
      "date_naissance": "1990-01-01",
      "situation_matrimoniale": "Célibataire",
      "statut": "Actif",
      "color": "#3498db",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    },
    "relations": {
      "tags": [
        {
          "id": 1,
          "name": "Nouveau",
          "date_association": "2024-01-01T00:00:00Z"
        }
      ],
      "etape_actuelle": {
        "id": 1,
        "libelle": "Accueil",
        "description": "Étape d'accueil des nouveaux membres",
        "date_association": "2024-01-01T00:00:00Z"
      },
      "groupe_actuel": {
        "id": 1,
        "nom": "Groupe Alpha",
        "description": "Groupe principal",
        "date_inscription": "2024-01-01T00:00:00Z",
        "date_sortie": null
      },
      "departement_actuel": {
        "id": 1,
        "nom": "Technique",
        "mission": "Gestion technique",
        "color": "#e74c3c",
        "date_inscription": "2024-01-01T00:00:00Z",
        "date_sortie": null
      }
    },
    "statistiques": {
      "nombre_tags": 1,
      "a_une_etape": true,
      "a_un_groupe": true,
      "a_un_departement": true
    }
  }
}
```

### Codes de statut

| Code | Description |
|------|-------------|
| `200` | Succès - Membre récupéré avec ses relations |
| `401` | Non autorisé - Token manquant ou invalide |
| `404` | Non trouvé - Membre inexistant |
| `500` | Erreur serveur - Erreur interne |

## Détails des relations

### Tags

Récupère tous les tags associés au membre via la table `Etiquetage`.

```json
"tags": [
  {
    "id": 1,
    "name": "Nom du tag",
    "date_association": "2024-01-01T00:00:00Z"
  }
]
```

### Étape actuelle

Récupère l'étape la plus récente du membre via la table `Integration`.

```json
"etape_actuelle": {
  "id": 1,
  "libelle": "Nom de l'étape",
  "description": "Description de l'étape",
  "date_association": "2024-01-01T00:00:00Z"
}
```

**Note** : Si le membre n'a pas d'étape, cette valeur sera `null`.

### Groupe actuel

Récupère le groupe actif du membre via la table `Regroupements`.

```json
"groupe_actuel": {
  "id": 1,
  "nom": "Nom du groupe",
  "description": "Description du groupe",
  "date_inscription": "2024-01-01T00:00:00Z",
  "date_sortie": null
}
```

**Note** : Si le membre n'a pas de groupe actif, cette valeur sera `null`.

### Département actuel

Récupère le département actif du membre via la table `Serviteurs`.

```json
"departement_actuel": {
  "id": 1,
  "nom": "Nom du département",
  "mission": "Mission du département",
  "color": "#e74c3c",
  "date_inscription": "2024-01-01T00:00:00Z",
  "date_sortie": null
}
```

**Note** : Si le membre n'a pas de département actif, cette valeur sera `null`.

## Statistiques

Résumé des relations du membre :

```json
"statistiques": {
  "nombre_tags": 3,
  "a_une_etape": true,
  "a_un_groupe": true,
  "a_un_departement": false
}
```

## Exemples d'utilisation

### cURL

```bash
curl -X GET \
  "http://localhost:8000/api/membres/1/membre_avec_relations/" \
  -H "Authorization: Token votre_token_ici" \
  -H "Content-Type: application/json"
```

### JavaScript (Fetch)

```javascript
const response = await fetch('/api/membres/1/membre_avec_relations/', {
  method: 'GET',
  headers: {
    'Authorization': 'Token votre_token_ici',
    'Content-Type': 'application/json'
  }
});

const data = await response.json();
console.log(data);
```

### Python (requests)

```python
import requests

headers = {
    'Authorization': 'Token votre_token_ici',
    'Content-Type': 'application/json'
}

response = requests.get(
    'http://localhost:8000/api/membres/1/membre_avec_relations/',
    headers=headers
)

data = response.json()
print(data)
```

## Gestion des erreurs

### Erreur 404 - Membre inexistant

```json
{
  "detail": "Not found."
}
```

### Erreur 401 - Non autorisé

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Erreur 500 - Erreur serveur

```json
{
  "success": false,
  "error": "Erreur lors de la récupération du membre avec ses relations: <détail de l'erreur>"
}
```

## Optimisations

L'endpoint utilise les optimisations suivantes :

- **select_related()** : Pour éviter les requêtes N+1 sur les relations
- **order_by('-created_at').first()** : Pour récupérer l'étape la plus récente
- **filter(actif=True)** : Pour récupérer uniquement les relations actives
- **Gestion d'erreurs** : Chaque relation est récupérée dans un try/catch séparé

## Tests

Un script de test complet est disponible : `scriptsTests/test_membre_avec_relations.py`

Pour exécuter les tests :

```bash
cd new_harvest_back
python scriptsTests/test_membre_avec_relations.py
```

## Cas d'usage

1. **Profil détaillé** : Affichage du profil complet d'un membre
2. **Tableau de bord** : Vue d'ensemble des relations d'un membre
3. **Validation** : Vérification des associations avant modifications
4. **Reporting** : Génération de rapports sur les membres et leurs relations

## Notes importantes

- L'endpoint récupère uniquement les relations **actives** pour les groupes et départements
- L'étape récupérée est la **plus récente** (basée sur `created_at`)
- Tous les tags sont récupérés (pas de limitation)
- Les erreurs de récupération des relations sont loggées mais n'empêchent pas le retour des autres données 