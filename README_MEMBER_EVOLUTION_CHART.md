# Guide d'utilisation du composant MemberEvolutionChart

## Description

Le composant `MemberEvolutionChart` remplace l'ancien `LineChart` et affiche l'évolution du nombre de membres par date de création. Il utilise les données réelles de l'API et offre des fonctionnalités de filtrage avancées.

## Installation et import

```tsx
import MemberEvolutionChart from '../components/Dashboard/MemberEvolutionChart';
```

## Utilisation de base

### 1. Utilisation simple

```tsx
<MemberEvolutionChart />
```

### 2. Avec options personnalisées

```tsx
<MemberEvolutionChart 
  title="Évolution des Membres"
  height={400}
  showFilters={true}
  className="w-full"
/>
```

## Props disponibles

| Prop | Type | Défaut | Description |
|------|------|--------|-------------|
| `title` | string | `'Évolution des Membres'` | Titre du composant |
| `height` | number | `400` | Hauteur du composant en pixels |
| `showFilters` | boolean | `true` | Afficher/masquer les filtres |
| `className` | string | `''` | Classes CSS supplémentaires |

## Exemples d'intégration

### 1. Remplacement du LineChart dans le Dashboard

```tsx
// Ancien code avec LineChart
<div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
  <div className="flex items-center justify-between mb-6">
    <h3 className="text-lg font-semibold text-gray-900">Nouveaux membres</h3>
    <button className="text-gray-400 hover:text-gray-600">
      <MoreHorizontal className="w-5 h-5" />
    </button>
  </div>
  <LineChart data={newMembersData} />
</div>

// Nouveau code avec MemberEvolutionChart
<MemberEvolutionChart 
  title="Évolution des Membres"
  height={300}
  showFilters={true}
/>
```

### 2. Pleine largeur dans le Dashboard

```tsx
<div className="mb-8">
  <MemberEvolutionChart 
    title="Évolution des Membres"
    height={400}
    showFilters={true}
    className="w-full"
  />
</div>
```

### 3. Layout en deux colonnes

```tsx
<div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
  <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
    <MemberEvolutionChart 
      title="Évolution Quotidienne"
      height={350}
      showFilters={false}
    />
  </div>
  <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
    <MemberEvolutionChart 
      title="Évolution Mensuelle"
      height={350}
      showFilters={false}
    />
  </div>
</div>
```

### 4. Dashboard avec contrôles de mise en page

```tsx
import React, { useState } from 'react';
import MemberEvolutionChart from './MemberEvolutionChart';

const DashboardWithControls: React.FC = () => {
  const [chartLayout, setChartLayout] = useState<'full' | 'split'>('full');

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      {/* Contrôles de mise en page */}
      <div className="mb-6 bg-white rounded-lg p-4 shadow-sm border border-gray-200">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">Options d'affichage</h3>
          <div className="flex items-center space-x-4">
            <label className="flex items-center space-x-2">
              <input
                type="radio"
                name="layout"
                value="full"
                checked={chartLayout === 'full'}
                onChange={(e) => setChartLayout(e.target.value as 'full' | 'split')}
                className="text-blue-600 focus:ring-blue-500"
              />
              <span className="text-sm text-gray-700">Pleine largeur</span>
            </label>
            <label className="flex items-center space-x-2">
              <input
                type="radio"
                name="layout"
                value="split"
                checked={chartLayout === 'split'}
                onChange={(e) => setChartLayout(e.target.value as 'full' | 'split')}
                className="text-blue-600 focus:ring-blue-500"
              />
              <span className="text-sm text-gray-700">Deux colonnes</span>
            </label>
          </div>
        </div>
      </div>

      {/* Charts Section - Layout dynamique */}
      {chartLayout === 'full' ? (
        <div className="mb-8">
          <MemberEvolutionChart 
            title="Évolution des Membres - Vue complète"
            height={450}
            showFilters={true}
            className="w-full"
          />
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <MemberEvolutionChart 
              title="Évolution Quotidienne"
              height={350}
              showFilters={false}
            />
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <MemberEvolutionChart 
              title="Évolution Mensuelle"
              height={350}
              showFilters={false}
            />
          </div>
        </div>
      )}
    </div>
  );
};
```

## Fonctionnalités

### 1. Filtres intégrés

Le composant inclut des filtres pour :
- **Format** : Quotidien ou mensuel
- **Période** : Date de début et de fin
- **Réinitialisation** : Bouton pour remettre à zéro les filtres

### 2. Statistiques rapides

Affichage automatique de :
- **Total Membres** : Nombre total actuel
- **Nouveaux (période)** : Évolution sur la période sélectionnée
- **Points de données** : Nombre de points affichés

### 3. Tableau de données

Affichage en tableau avec :
- **Date** : Format selon le filtre choisi
- **Nombre de Membres** : Valeur cumulée
- **Évolution** : Différence avec la période précédente

### 4. États de chargement et d'erreur

- **Chargement** : Spinner avec message
- **Erreur** : Message d'erreur avec bouton de retry
- **Aucune donnée** : Message informatif

## Avantages par rapport au LineChart

### ✅ Données réelles
- Utilise l'API backend au lieu de données statiques
- Données en temps réel et à jour

### ✅ Filtres interactifs
- Filtrage par période
- Choix du format d'affichage
- Réinitialisation facile

### ✅ Statistiques enrichies
- Métriques calculées automatiquement
- Évolution entre les périodes
- Informations contextuelles

### ✅ Gestion d'erreurs
- États de chargement et d'erreur
- Messages informatifs
- Possibilité de retry

### ✅ Interface moderne
- Design cohérent avec le reste de l'application
- Responsive et accessible
- Animations et transitions

## Migration depuis LineChart

### Étape 1 : Remplacer l'import

```tsx
// Ancien
import LineChart from './LineChart';

// Nouveau
import MemberEvolutionChart from './MemberEvolutionChart';
```

### Étape 2 : Remplacer l'utilisation

```tsx
// Ancien
<LineChart data={newMembersData} />

// Nouveau
<MemberEvolutionChart 
  title="Évolution des Membres"
  height={300}
  showFilters={true}
/>
```

### Étape 3 : Supprimer les données statiques

```tsx
// Supprimer cette section
const newMembersData = [
  { date: '30 Jun', value: 0 },
  { date: 'Jul \'25', value: 1 },
  // ...
];
```

## Personnalisation avancée

### 1. Styles personnalisés

```tsx
<MemberEvolutionChart 
  className="custom-chart-styles"
  title="Mon titre personnalisé"
/>
```

### 2. Hauteur adaptative

```tsx
<MemberEvolutionChart 
  height={window.innerHeight * 0.6}
  showFilters={false}
/>
```

### 3. Intégration dans un layout complexe

```tsx
<div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
  <div className="xl:col-span-2">
    <MemberEvolutionChart 
      title="Évolution principale"
      height={400}
      showFilters={true}
    />
  </div>
  <div className="xl:col-span-1">
    <MemberEvolutionChart 
      title="Vue résumée"
      height={400}
      showFilters={false}
    />
  </div>
</div>
```

## Dépannage

### Problème : Données ne se chargent pas
- Vérifiez que l'API backend est accessible
- Vérifiez l'authentification
- Consultez la console pour les erreurs

### Problème : Filtres ne fonctionnent pas
- Vérifiez que les dates sont au bon format (YYYY-MM-DD)
- Assurez-vous que l'endpoint supporte les paramètres

### Problème : Affichage incorrect
- Vérifiez que les props sont correctement passées
- Consultez les types TypeScript pour la validation

## Support et maintenance

Le composant utilise :
- **API** : `statisticsService.getMemberEvolution()`
- **Types** : `MemberEvolutionData[]`
- **Utils** : `convertColorToHex()` pour les couleurs
- **Styles** : Tailwind CSS pour le design

Pour toute question ou problème, consultez :
- La documentation de l'endpoint : `README_ENDPOINT_EVOLUTION_MEMBRES.md`
- Les types TypeScript dans `types/index.ts`
- Le service de statistiques dans `services/statisticsService.ts` 