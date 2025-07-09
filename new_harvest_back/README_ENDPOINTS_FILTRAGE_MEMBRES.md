# Guide d'utilisation des endpoints de filtrage des membres

## Vue d'ensemble

Ce guide explique comment utiliser les différents endpoints de filtrage des membres dans votre application frontend. Ces endpoints permettent de récupérer des listes de membres selon différents critères de filtrage.

## Endpoints disponibles

### 1. Filtrage par groupes
**Endpoint:** `GET /api/membres/par_groupes/`

**Paramètres:**
- `groupes[]`: Liste des IDs des groupes (peut être multiple)

**Exemple d'utilisation:**
```javascript
// Filtrer les membres appartenant aux groupes 1, 2 et 3
const response = await memberService.getMembersByGroups([1, 2, 3]);

// URL générée: /api/membres/par_groupes/?groupes[]=1&groupes[]=2&groupes[]=3
```

### 2. Filtrage par étapes
**Endpoint:** `GET /api/membres/par_etapes/`

**Paramètres:**
- `etapes[]`: Liste des IDs des étapes (peut être multiple)

**Exemple d'utilisation:**
```javascript
// Filtrer les membres à l'étape 1 et 2
const response = await memberService.getMembersByEtapes([1, 2]);

// URL générée: /api/membres/par_etapes/?etapes[]=1&etapes[]=2
```

### 3. Filtrage par tags
**Endpoint:** `GET /api/membres/par_tags/`

**Paramètres:**
- `tags[]`: Liste des IDs des tags (peut être multiple)

**Exemple d'utilisation:**
```javascript
// Filtrer les membres ayant les tags 1, 2 et 3
const response = await memberService.getMembersByTags([1, 2, 3]);

// URL générée: /api/membres/par_tags/?tags[]=1&tags[]=2&tags[]=3
```

### 4. Filtres combinés
**Endpoint:** `GET /api/membres/filtres_combines/`

**Paramètres:**
- `groupes[]`: Liste des IDs des groupes (optionnel)
- `etapes[]`: Liste des IDs des étapes (optionnel)
- `tags[]`: Liste des IDs des tags (optionnel)
- `search`: Terme de recherche (optionnel)
- `page`: Numéro de page (optionnel)
- `page_size`: Taille de la page (optionnel)

**Exemple d'utilisation:**
```javascript
// Filtrage combiné avec recherche et pagination
const response = await memberService.getMembersWithCombinedFilters({
  groupes: [1, 2],
  etapes: [1],
  tags: [3, 4],
  search: "Jean",
  page: 1,
  page_size: 25
});

// URL générée: /api/membres/filtres_combines/?groupes[]=1&groupes[]=2&etapes[]=1&tags[]=3&tags[]=4&search=Jean&page=1&page_size=25
```

### 5. Tous les membres (sans pagination)
**Endpoint:** `GET /api/membres/tous_les_membres/`

**Exemple d'utilisation:**
```javascript
// Récupérer tous les membres
const response = await memberService.getAllMembers();
```

### 6. Membres simples (version allégée)
**Endpoint:** `GET /api/membres/membres_simples/`

**Exemple d'utilisation:**
```javascript
// Récupérer les membres avec des données réduites
const response = await memberService.getSimpleMembers();
```

### 7. Membre avec relations
**Endpoint:** `GET /api/membres/{id}/membre_avec_relations/`

**Exemple d'utilisation:**
```javascript
// Récupérer un membre avec toutes ses relations
const response = await memberService.getMemberWithRelations(123);
```

## Intégration dans le composant MembersList

Le composant `MembersList` a été mis à jour pour utiliser ces endpoints. Voici les principales fonctionnalités :

### États de filtrage
```typescript
interface FilterState {
  groupes: number[];
  etapes: number[];
  tags: number[];
  search: string;
}
```

### Logique de chargement
Le composant utilise automatiquement l'endpoint approprié selon les filtres actifs :

1. **Aucun filtre actif** → Utilise l'endpoint de base avec pagination
2. **Filtres actifs** → Utilise l'endpoint `filtres_combines`

### Fonctionnalités disponibles

#### Filtres interactifs
- ✅ Filtrage par groupes avec recherche
- ✅ Filtrage par étapes avec recherche  
- ✅ Filtrage par tags avec recherche
- ✅ Recherche textuelle globale
- ✅ Combinaison de plusieurs filtres

#### Interface utilisateur
- ✅ Indicateurs visuels des filtres actifs
- ✅ Bouton pour effacer tous les filtres
- ✅ États de chargement avec spinners
- ✅ Messages d'erreur et états vides
- ✅ Pagination automatique

#### Actions en lot
- ✅ Sélection multiple de membres
- ✅ Actions groupées (tags, étapes, départements, groupes)

## Exemples d'utilisation pratique

### 1. Filtrer les membres d'un groupe spécifique
```javascript
// Dans votre composant React
const [members, setMembers] = useState([]);

useEffect(() => {
  const loadMembers = async () => {
    try {
      const response = await memberService.getMembersByGroups([1]); // Groupe ID 1
      setMembers(response.data);
    } catch (error) {
      console.error('Erreur:', error);
    }
  };
  
  loadMembers();
}, []);
```

### 2. Recherche combinée
```javascript
// Recherche avec plusieurs critères
const searchMembers = async () => {
  const filters = {
    groupes: [1, 2],        // Membres des groupes 1 et 2
    etapes: [1],            // À l'étape 1
    tags: [3],              // Avec le tag 3
    search: "Jean",         // Nom contenant "Jean"
    page: 1,
    page_size: 25
  };
  
  const response = await memberService.getMembersWithCombinedFilters(filters);
  return response.data;
};
```

### 3. Gestion des erreurs
```javascript
const loadMembersWithErrorHandling = async () => {
  try {
    setLoading(true);
    const response = await memberService.getMembersByGroups([1]);
    setMembers(response.data);
  } catch (error) {
    console.error('Erreur lors du chargement:', error);
    // Afficher un message d'erreur à l'utilisateur
    setError('Impossible de charger les membres');
  } finally {
    setLoading(false);
  }
};
```

## Bonnes pratiques

### 1. Gestion de l'état de chargement
Toujours afficher un indicateur de chargement pendant les requêtes :
```javascript
const [loading, setLoading] = useState(false);

const loadData = async () => {
  setLoading(true);
  try {
    // Requête API
  } finally {
    setLoading(false);
  }
};
```

### 2. Gestion des erreurs
Implémenter une gestion d'erreur robuste :
```javascript
try {
  const response = await memberService.getMembersByGroups([1]);
  setMembers(response.data);
} catch (error) {
  console.error('Erreur:', error);
  // Afficher un message d'erreur approprié
}
```

### 3. Optimisation des performances
- Utiliser la pagination pour les grandes listes
- Mettre en cache les données de filtres (groupes, étapes, tags)
- Éviter les requêtes inutiles avec des debounce sur la recherche

### 4. Expérience utilisateur
- Afficher des états de chargement
- Donner un feedback visuel pour les actions
- Permettre d'annuler les filtres facilement
- Sauvegarder les préférences de filtrage

## Dépannage

### Problèmes courants

1. **Erreur 404 sur les endpoints**
   - Vérifier que le serveur Django est démarré
   - Vérifier que les URLs sont correctes
   - Vérifier l'authentification

2. **Filtres qui ne fonctionnent pas**
   - Vérifier que les IDs des filtres existent en base
   - Vérifier le format des paramètres
   - Vérifier les logs du serveur

3. **Performance lente**
   - Utiliser la pagination
   - Limiter le nombre de filtres simultanés
   - Optimiser les requêtes côté serveur

### Debug
Pour déboguer les requêtes, utilisez les outils de développement du navigateur :
```javascript
// Activer le debug des requêtes
console.log('URL:', url);
console.log('Paramètres:', params);
console.log('Réponse:', response);
```

## Conclusion

Ces endpoints offrent une flexibilité maximale pour filtrer et rechercher les membres selon vos besoins. Le composant `MembersList` intégré utilise ces endpoints de manière optimale avec une interface utilisateur intuitive et des performances optimisées. 