# Endpoint Évolution des Membres

## Description

L'endpoint `evolution_membres` permet de récupérer l'évolution du nombre total de membres par date de création. Il retourne un format spécifique optimisé pour les graphiques et tableaux de bord.

## Route

```
GET /api/membres/evolution_membres/
```

## Authentification

Cet endpoint nécessite une authentification par token.

## Paramètres de requête

| Paramètre     | Type   | Requis | Description                                   | Exemple        |
| -------------- | ------ | ------ | --------------------------------------------- | -------------- |
| `start_date` | string | Non    | Date de début au format YYYY-MM-DD           | `2024-01-01` |
| `end_date`   | string | Non    | Date de fin au format YYYY-MM-DD              | `2024-12-31` |
| `format`     | string | Non    | Format d'affichage (`daily` ou `monthly`) | `daily`      |

### Format des dates

- **Format quotidien** (`format=daily`) : `30 Jun`, `02 Jul`, `03 Jul`
- **Format mensuel** (`format=monthly`) : `Jul '25`, `Aug '25`

## Réponse

### Structure de la réponse

```json
{
  "success": true,
  "data": [
    {
      "date": "30 Jun",
      "value": 0
    },
    {
      "date": "Jul '25",
      "value": 1
    },
    {
      "date": "02 Jul",
      "value": 2
    },
    {
      "date": "03 Jul",
      "value": 3
    }
  ]
}
```

### Format des données

- `date` : Date formatée selon le paramètre `format`
- `value` : Nombre cumulatif de membres à cette date

## Exemples d'utilisation

### 1. Récupération de toutes les données (format quotidien par défaut)

```bash
curl -X GET "http://localhost:8000/api/membres/evolution_membres/" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 2. Format mensuel

```bash
curl -X GET "http://localhost:8000/api/membres/evolution_membres/?format=monthly" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 3. Filtrage par période

```bash
curl -X GET "http://localhost:8000/api/membres/evolution_membres/?start_date=2024-01-01&end_date=2024-06-30&format=daily" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 4. Utilisation avec JavaScript/TypeScript

```typescript
import { statisticsService } from '../services/statisticsService';

// Récupération de l'évolution des membres
const getMemberEvolution = async () => {
  try {
    const response = await statisticsService.getMemberEvolution({
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      format: 'daily'
    });
  
    if (response.data.success) {
      const evolutionData = response.data.data;
      console.log('Évolution des membres:', evolutionData);
    }
  } catch (error) {
    console.error('Erreur:', error);
  }
};
```

### 5. Utilisation avec React

```tsx
import React, { useState, useEffect } from 'react';
import { statisticsService } from '../services/statisticsService';

const MemberEvolutionChart = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await statisticsService.getMemberEvolution();
        const apiData = response.data as any;
      
        if (apiData.success) {
          setData(apiData.data);
        }
      } catch (error) {
        console.error('Erreur:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Chargement...</div>;

  return (
    <div>
      <h3>Évolution des Membres</h3>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Nombre de Membres</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.date}</td>
              <td>{item.value}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
```

## Gestion des erreurs

### Erreur de format de date

```json
{
  "success": false,
  "error": "Format de date de début invalide. Utilisez YYYY-MM-DD"
}
```

### Erreur serveur

```json
{
  "success": false,
  "error": "Erreur lors du calcul de l'évolution des membres: [détails]"
}
```

## Logique de calcul

1. **Récupération des données** : Tous les membres avec une date de création valide
2. **Tri chronologique** : Tri par date de création croissante
3. **Calcul cumulatif** : Pour chaque date, calcul du nombre total de membres jusqu'à cette date
4. **Formatage** : Application du format de date demandé (quotidien ou mensuel)
5. **Déduplication** : Si plusieurs membres ont la même date, un seul point de données est créé avec la valeur cumulée

## Cas d'usage

### Tableaux de bord

- Affichage de l'évolution de la croissance de la communauté
- Graphiques de tendance
- Indicateurs de performance

### Rapports

- Analyse de la croissance mensuelle/quotidienne
- Comparaison de périodes
- Prévisions basées sur les tendances

### Monitoring

- Suivi de l'activité d'inscription
- Détection de pics d'activité
- Évaluation de l'efficacité des campagnes

## Performance

- **Indexation** : L'endpoint utilise l'index sur `created_at` pour des performances optimales
- **Filtrage** : Les filtres de date sont appliqués au niveau de la base de données
- **Pagination** : Non applicable car les données sont déjà agrégées par date

## Tests

Un script de test est disponible : `scriptsTests/test_evolution_membres.py`

```bash
cd new_harvest_back
python scriptsTests/test_evolution_membres.py
```

## Intégration avec le frontend

Le composant `MemberEvolutionChart` est disponible dans le frontend pour afficher ces données :

```tsx
import MemberEvolutionChart from '../components/Dashboard/MemberEvolutionChart';

// Utilisation simple
<MemberEvolutionChart />

// Avec options personnalisées
<MemberEvolutionChart 
  title="Croissance de la Communauté"
  height={500}
  showFilters={true}
/>
```

## Évolutions futures

- Ajout de filtres par groupe/département
- Calcul de métriques dérivées (taux de croissance, moyenne mobile)
- Export des données en CSV/Excel
- Cache des résultats pour améliorer les performances
