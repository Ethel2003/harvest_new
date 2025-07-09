# Endpoint taged_multiple - Nouveau Format de Payload

## Vue d'ensemble

L'endpoint `taged_multiple` a été mis à jour pour accepter un nouveau format de payload tout en maintenant la compatibilité avec l'ancien format. Cette modification améliore la cohérence des noms de paramètres et fournit une meilleure validation et des réponses plus détaillées.

## Endpoint

```
POST /api/membres/taged_multiple/
```

## Nouveau Format de Payload

### **Format Principal (Recommandé)**
```json
{
  "tags_ids": [1, 2, 3],
  "membre_ids": [1, 2, 3, 4]
}
```

### **Ancien Format (Toujours Supporté)**
```json
{
  "tag_ids": [1, 2, 3],
  "membre_ids": [1, 2, 3, 4]
}
```

## Paramètres

| Paramètre | Type | Description | Obligatoire |
|-----------|------|-------------|-------------|
| `tags_ids` | array | Liste des IDs des tags à associer | ✅ (nouveau format) |
| `tag_ids` | array | Liste des IDs des tags à associer | ✅ (ancien format) |
| `membre_ids` | array | Liste des IDs des membres | ✅ |

## Logique de Priorité

L'endpoint utilise la logique suivante pour déterminer quel format utiliser :

1. **Nouveau format prioritaire** : Si `tags_ids` est présent, il est utilisé
2. **Fallback vers l'ancien format** : Si `tags_ids` est absent, `tag_ids` est utilisé
3. **Erreur si aucun format** : Si aucun des deux n'est présent, une erreur 400 est retournée

## Exemples d'Utilisation

### **Exemple 1: Nouveau Format**
```bash
curl -X POST "http://localhost:8000/api/membres/taged_multiple/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "tags_ids": [1, 2, 3],
    "membre_ids": [1, 2, 3]
  }'
```

### **Exemple 2: Ancien Format (Compatibilité)**
```bash
curl -X POST "http://localhost:8000/api/membres/taged_multiple/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "tag_ids": [1, 2, 3],
    "membre_ids": [1, 2, 3]
  }'
```

### **Exemple 3: Format Mixte (Nouveau prioritaire)**
```bash
curl -X POST "http://localhost:8000/api/membres/taged_multiple/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "tags_ids": [1, 2, 3],
    "tag_ids": [4, 5, 6],
    "membre_ids": [1, 2, 3]
  }'
# Résultat: tags_ids [1, 2, 3] sera utilisé, tag_ids [4, 5, 6] sera ignoré
```

## Réponse

### **Succès (201 Created)**
```json
{
  "success": true,
  "message": "Association de 3 tags à 3 membres effectuée avec succès !",
  "data": {
    "etiquetages_crees": 9,
    "etiquetages_supprimes": 2,
    "tags_associes": [
      {
        "id": 1,
        "name": "Leader"
      },
      {
        "id": 2,
        "name": "Musicien"
      },
      {
        "id": 3,
        "name": "Enseignant"
      }
    ],
    "membres_associes": [
      {
        "id": 1,
        "nom": "Dupont",
        "prenom": "Jean"
      },
      {
        "id": 2,
        "nom": "Martin",
        "prenom": "Sophie"
      },
      {
        "id": 3,
        "nom": "Bernard",
        "prenom": "Pierre"
      }
    ],
    "total_associations": 9
  },
  "payload_recu": {
    "tags_ids": [1, 2, 3],
    "membre_ids": [1, 2, 3],
    "format_utilise": "nouveau"
  }
}
```

### **Erreur de Validation (400 Bad Request)**
```json
{
  "success": false,
  "error": "Les identifiants des tags (tags_ids) et des membres (membre_ids) sont requis"
}
```

### **Erreur de Ressource Non Trouvée (404 Not Found)**
```json
{
  "success": false,
  "error": "Tags non trouvés: [999, 998]"
}
```

## Validations

### **Validations Effectuées**

1. **Présence des paramètres** : Vérification que `tags_ids`/`tag_ids` et `membre_ids` sont présents
2. **Type des paramètres** : Vérification que les paramètres sont des listes
3. **Listes non vides** : Vérification que les listes ne sont pas vides
4. **Existence des tags** : Vérification que tous les tags existent en base
5. **Existence des membres** : Vérification que tous les membres existent en base

### **Messages d'Erreur**

| Erreur | Code | Message |
|--------|------|---------|
| Paramètres manquants | 400 | "Les identifiants des tags (tags_ids) et des membres (membre_ids) sont requis" |
| Type incorrect | 400 | "tags_ids et membre_ids doivent être des listes" |
| Liste vide | 400 | "Les listes tags_ids et membre_ids ne peuvent pas être vides" |
| Tags inexistants | 404 | "Tags non trouvés: [999, 998]" |
| Membres inexistants | 404 | "Membres non trouvés: [999, 998]" |

## Fonctionnement

### **Processus d'Association**

1. **Validation** : Vérification de tous les paramètres et ressources
2. **Suppression des doublons** : Suppression des associations existantes pour éviter les doublons
3. **Création en masse** : Création de toutes les nouvelles associations en une seule requête SQL
4. **Réponse détaillée** : Retour d'informations complètes sur l'opération

### **Optimisations**

- **Bulk Create** : Utilisation de `bulk_create` pour optimiser les performances
- **Requête unique** : Suppression des doublons en une seule requête
- **Validation préalable** : Vérification de l'existence avant traitement

## Utilisation Frontend

### **Service API**
```javascript
// src/api/membre.service.js
tagedMultiple(tagIds, membreIds) {
  return this.customAction('taged_multiple', {
    tags_ids: tagIds,  // Nouveau format
    membre_ids: membreIds
  });
}
```

### **Composable Vue.js**
```typescript
// src/composable/useTag.ts
const TagedMultiple = async (tagIds: number[], memberIds: number[]) => {
  const { error } = await api.create('api/membres/taged-multiple', {
    tags_ids: tagIds,  // Nouveau format
    membre_ids: memberIds,
  })
  
  if (error == null) {
    // Succès
  } else {
    // Gérer l'erreur
  }
}
```

### **Composant Vue**
```vue
<script setup>
const associateTags = async () => {
  const membre_ids = [memberId.value]
  const tag_ids = selectedTags.value.slice()
  
  try {
    const response = await axiosClient.post('/membres/taged-multiple', {
      tags_ids: tag_ids,  // Nouveau format
      membre_ids: membre_ids,
    })
    
    if (response.data.success) {
      notyf.success(response.data.message)
    }
  } catch (error) {
    console.error('Erreur:', error)
  }
}
</script>
```

## Migration

### **Migration Progressive**

1. **Phase 1** : L'ancien format continue de fonctionner
2. **Phase 2** : Mise à jour des services frontend pour utiliser le nouveau format
3. **Phase 3** : Mise à jour des composants pour utiliser le nouveau format
4. **Phase 4** : Dépréciation de l'ancien format (optionnel)

### **Recommandations**

- **Nouveau code** : Utiliser le nouveau format `tags_ids`
- **Code existant** : Peut continuer à utiliser l'ancien format
- **Tests** : Mettre à jour les tests pour utiliser le nouveau format

## Tests

### **Script de Test**
```bash
cd new_harvest_back/scriptsTests/
python test_taged_multiple_new_format.py
```

### **Tests Inclus**

- ✅ Nouveau format avec `tags_ids`
- ✅ Ancien format pour compatibilité
- ✅ Validation des paramètres vides
- ✅ Validation des ressources inexistantes
- ✅ Priorité du nouveau format
- ✅ Structure de réponse détaillée
- ✅ Tests de performance

## Avantages du Nouveau Format

### **✅ Améliorations**

1. **Cohérence** : `tags_ids` suit la même convention que `membre_ids`
2. **Validation renforcée** : Vérifications plus strictes
3. **Réponse détaillée** : Plus d'informations sur l'opération
4. **Gestion d'erreurs** : Messages d'erreur plus précis
5. **Compatibilité** : L'ancien format continue de fonctionner

### **📊 Métriques**

- **Étiquetages créés** : Nombre d'associations créées
- **Étiquetages supprimés** : Nombre de doublons supprimés
- **Tags associés** : Liste des tags utilisés
- **Membres associés** : Liste des membres concernés
- **Total d'associations** : Nombre total d'opérations

## Support

Pour toute question ou problème avec cet endpoint :

1. **Documentation** : Consulter cette documentation
2. **Tests** : Exécuter le script de test
3. **Logs** : Vérifier les logs du serveur Django
4. **Équipe** : Contacter l'équipe de développement 