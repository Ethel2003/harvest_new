# Endpoints de Filtrage des Membres

Ce document décrit les nouveaux endpoints de filtrage implémentés pour le modèle Membre dans l'API Harvest.

## Vue d'ensemble

Les endpoints de filtrage permettent de récupérer des membres en fonction de leurs relations avec :
- **Groupes** (via le modèle `Regroupements`)
- **Étapes** (via le modèle `Integration`)
- **Tags** (via le modèle `Etiquetage`)

## Endpoints Disponibles

### 1. Filtrage par Groupes

**Endpoint :** `GET /api/membres/par_groupes/`

**Description :** Récupère les membres qui appartiennent aux groupes spécifiés (regroupements actifs uniquement).

**Paramètres de requête :**
- `groupes[]` : Liste des IDs des groupes (peut être multiple)

**Exemple d'utilisation :**
```bash
# Récupérer les membres des groupes 1 et 2
GET /api/membres/par_groupes/?groupes[]=1&groupes[]=2

# Récupérer les membres du groupe 5 uniquement
GET /api/membres/par_groupes/?groupes[]=5
```

**Réponse :**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nom": "Dupont",
      "prenom": "Jean",
      "email": "jean.dupont@example.com",
      // ... autres champs du membre
    }
  ],
  "filtres_appliques": {
    "groupes": ["1", "2"],
    "nombre_membres": 15
  }
}
```

### 2. Filtrage par Étapes

**Endpoint :** `GET /api/membres/par_etapes/`

**Description :** Récupère les membres qui sont dans les étapes spécifiées.

**Paramètres de requête :**
- `etapes[]` : Liste des IDs des étapes (peut être multiple)

**Exemple d'utilisation :**
```bash
# Récupérer les membres des étapes 1 et 3
GET /api/membres/par_etapes/?etapes[]=1&etapes[]=3

# Récupérer les membres de l'étape 2 uniquement
GET /api/membres/par_etapes/?etapes[]=2
```

**Réponse :**
```json
{
  "success": true,
  "data": [
    {
      "id": 2,
      "nom": "Martin",
      "prenom": "Marie",
      "email": "marie.martin@example.com",
      // ... autres champs du membre
    }
  ],
  "filtres_appliques": {
    "etapes": ["1", "3"],
    "nombre_membres": 8
  }
}
```

### 3. Filtrage par Tags

**Endpoint :** `GET /api/membres/par_tags/`

**Description :** Récupère les membres qui ont les tags spécifiés.

**Paramètres de requête :**
- `tags[]` : Liste des IDs des tags (peut être multiple)

**Exemple d'utilisation :**
```bash
# Récupérer les membres avec les tags 1 et 4
GET /api/membres/par_tags/?tags[]=1&tags[]=4

# Récupérer les membres avec le tag 3 uniquement
GET /api/membres/par_tags/?tags[]=3
```

**Réponse :**
```json
{
  "success": true,
  "data": [
    {
      "id": 3,
      "nom": "Bernard",
      "prenom": "Sophie",
      "email": "sophie.bernard@example.com",
      // ... autres champs du membre
    }
  ],
  "filtres_appliques": {
    "tags": ["1", "4"],
    "nombre_membres": 12
  }
}
```

### 4. Filtrage Combiné

**Endpoint :** `GET /api/membres/filtres_combines/`

**Description :** Récupère les membres qui correspondent à une combinaison de filtres (groupes, étapes, tags).

**Paramètres de requête :**
- `groupes[]` : Liste des IDs des groupes (optionnel)
- `etapes[]` : Liste des IDs des étapes (optionnel)
- `tags[]` : Liste des IDs des tags (optionnel)

**Exemple d'utilisation :**
```bash
# Filtrage combiné : membres du groupe 1, étape 2, avec le tag 3
GET /api/membres/filtres_combines/?groupes[]=1&etapes[]=2&tags[]=3

# Filtrage partiel : membres du groupe 1 avec le tag 2
GET /api/membres/filtres_combines/?groupes[]=1&tags[]=2

# Filtrage par étapes et tags uniquement
GET /api/membres/filtres_combines/?etapes[]=1&tags[]=1
```

**Réponse :**
```json
{
  "success": true,
  "data": [
    {
      "id": 4,
      "nom": "Petit",
      "prenom": "Pierre",
      "email": "pierre.petit@example.com",
      // ... autres champs du membre
    }
  ],
  "filtres_appliques": {
    "groupes": ["1"],
    "etapes": ["2"],
    "tags": ["3"],
    "nombre_membres": 3
  }
}
```

### 5. Endpoint Principal avec Filtres

**Endpoint :** `GET /api/membres/`

**Description :** L'endpoint principal de liste des membres supporte maintenant les filtres directement.

**Paramètres de requête :**
- `groupes[]` : Liste des IDs des groupes (optionnel)
- `etapes[]` : Liste des IDs des étapes (optionnel)
- `tags[]` : Liste des IDs des tags (optionnel)
- `search` : Recherche textuelle (optionnel)
- `ordering` : Tri (optionnel)

**Exemple d'utilisation :**
```bash
# Filtrage combiné via l'endpoint principal
GET /api/membres/?groupes[]=1&etapes[]=1&tags[]=1

# Avec recherche et tri
GET /api/membres/?groupes[]=1&search=jean&ordering=nom
```

## Gestion des Erreurs

### Erreur 400 - Paramètres manquants

Si aucun paramètre de filtrage n'est fourni pour les endpoints spécifiques :

```json
{
  "success": false,
  "error": "Aucun groupe spécifié. Utilisez le paramètre groupes[]"
}
```

### Erreur 500 - Erreur serveur

En cas d'erreur interne :

```json
{
  "success": false,
  "error": "Erreur lors du filtrage par groupes: [détails de l'erreur]"
}
```

## Modèles de Données Utilisés

### Regroupements (Membre ↔ Groupe)
```python
class Regroupements(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='regroupements')
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='regroupements')
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_sortie = models.DateTimeField(null=True, blank=True)
    actif = models.BooleanField(default=True)
```

### Integration (Membre ↔ Etape)
```python
class Integration(models.Model):
    etape = models.ForeignKey(Etape, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    created_at = models.DateField()
    membership = models.BooleanField(default=False)
```

### Etiquetage (Membre ↔ Tag)
```python
class Etiquetage(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
```

## Notes Importantes

1. **Regroupements actifs uniquement** : Le filtrage par groupes ne prend en compte que les regroupements avec `actif=True`.

2. **Distinct** : Tous les endpoints utilisent `.distinct()` pour éviter les doublons en cas de relations multiples.

3. **Pagination** : Tous les endpoints supportent la pagination standard de Django REST Framework.

4. **Authentification** : Tous les endpoints nécessitent une authentification par token.

5. **Performance** : Les requêtes sont optimisées avec des `select_related` et `prefetch_related` automatiques.

## Tests

Un script de test est disponible dans `scriptsTests/test_filtres_membres.py` pour vérifier le bon fonctionnement des endpoints.

Pour lancer les tests :
```bash
cd new_harvest_back
python scriptsTests/test_filtres_membres.py
```

## Exemples d'Intégration Frontend

### JavaScript/TypeScript
```javascript
// Filtrage par groupes
const getMembresParGroupes = async (groupesIds) => {
  const params = groupesIds.map(id => `groupes[]=${id}`).join('&');
  const response = await fetch(`/api/membres/par_groupes/?${params}`, {
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    }
  });
  return response.json();
};

// Filtrage combiné
const getMembresFiltres = async (filtres) => {
  const params = new URLSearchParams();
  if (filtres.groupes) filtres.groupes.forEach(id => params.append('groupes[]', id));
  if (filtres.etapes) filtres.etapes.forEach(id => params.append('etapes[]', id));
  if (filtres.tags) filtres.tags.forEach(id => params.append('tags[]', id));
  
  const response = await fetch(`/api/membres/filtres_combines/?${params}`, {
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    }
  });
  return response.json();
};
```

### Python (requests)
```python
import requests

# Configuration
BASE_URL = "http://localhost:8000/api"
headers = {'Authorization': f'Token {token}'}

# Filtrage par étapes
response = requests.get(
    f"{BASE_URL}/membres/par_etapes/",
    params={'etapes[]': [1, 2, 3]},
    headers=headers
)
membres = response.json()['data']

# Filtrage combiné
response = requests.get(
    f"{BASE_URL}/membres/filtres_combines/",
    params={
        'groupes[]': [1],
        'etapes[]': [2],
        'tags[]': [3, 4]
    },
    headers=headers
)
membres_filtres = response.json()['data']
``` 