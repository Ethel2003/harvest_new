# Utilitaire de Gestion des Couleurs

## Vue d'ensemble

L'utilitaire de couleur (`colorUtils.ts`) permet de convertir les valeurs numériques de couleur stockées dans le backend en vrais codes couleur hexadécimaux utilisables dans l'interface utilisateur.

## Problème résolu

Le backend stocke les couleurs comme des chaînes de caractères numériques (ex: `'1'`, `'2'`, `'3'`) dans les champs `color` des modèles `Groupe` et `Departement`. Ces valeurs doivent être converties en codes couleur hexadécimaux pour être utilisées dans les graphiques et l'interface.

## Fonctionnalités

### 🎨 Palette de couleurs prédéfinies

30 couleurs modernes et harmonieuses prêtes à l'emploi :

```typescript
COLOR_PALETTE = {
  '1': '#FF6B6B',   // Rouge corail
  '2': '#4ECDC4',   // Turquoise
  '3': '#45B7D1',   // Bleu ciel
  '4': '#96CEB4',   // Vert menthe
  '5': '#FFEAA7',   // Jaune doux
  // ... et 25 autres couleurs
}
```

### 🔧 Fonctions principales

#### `convertColorToHex(colorValue, fallbackColor?)`

Convertit une valeur de couleur en code hexadécimal.

```typescript
import { convertColorToHex } from '../utils/colorUtils';

// Conversion de valeurs numériques
convertColorToHex('1')     // → '#FF6B6B'
convertColorToHex('2')     // → '#4ECDC4'
convertColorToHex('25')    // → '#FCF3CF'

// Valeurs déjà hexadécimales
convertColorToHex('#FF0000') // → '#FF0000'

// Valeurs null/undefined
convertColorToHex(null)    // → '#3B82F6' (couleur par défaut)
```

#### `getColorByName(name)`

Génère une couleur cohérente basée sur un nom.

```typescript
import { getColorByName } from '../utils/colorUtils';

getColorByName('Groupe A')     // → Couleur cohérente pour "Groupe A"
getColorByName('Département B') // → Couleur cohérente pour "Département B"
```

#### `getColorByIndex(index)`

Obtient une couleur de la palette par index.

```typescript
import { getColorByIndex } from '../utils/colorUtils';

getColorByIndex(1)  // → '#FF6B6B'
getColorByIndex(5)  // → '#FFEAA7'
getColorByIndex(99) // → '#3B82F6' (couleur par défaut)
```

### 🎯 Fonctions utilitaires

#### `getContrastColor(backgroundColor)`

Retourne noir ou blanc selon la luminosité du fond.

```typescript
import { getContrastColor } from '../utils/colorUtils';

getContrastColor('#FF6B6B') // → '#000000' (noir pour fond clair)
getContrastColor('#1F2937') // → '#FFFFFF' (blanc pour fond foncé)
```

#### `darkenColor(color, amount)`

Assombrit une couleur.

```typescript
import { darkenColor } from '../utils/colorUtils';

darkenColor('#FF6B6B', 30) // → Couleur assombrie de 30%
```

#### `lightenColor(color, amount)`

Éclaircit une couleur.

```typescript
import { lightenColor } from '../utils/colorUtils';

lightenColor('#FF6B6B', 30) // → Couleur éclaircie de 30%
```

#### `getColorWithAlpha(color, alpha)`

Ajoute de la transparence.

```typescript
import { getColorWithAlpha } from '../utils/colorUtils';

getColorWithAlpha('#FF6B6B', 0.3) // → 'rgba(255, 107, 107, 0.3)'
```

## Utilisation dans le Dashboard

### Avant (problématique)

```typescript
const groupsData = groups?.data?.groupes?.map(groupe => ({
  name: groupe.nom,
  value: groupe.membres_count,
  color: groupe.color // ← Valeur numérique comme "1", "2", etc.
})) || []
```

### Après (solution)

```typescript
import { convertColorToHex } from '../../utils/colorUtils';

const groupsData = groups?.data?.groupes?.map(groupe => ({
  name: groupe.nom,
  value: groupe.membres_count,
  color: convertColorToHex(groupe.color) // ← Code hexadécimal comme "#FF6B6B"
})) || []
```

## Intégration dans les composants

### Composant Dashboard

```typescript
import React, { useState, useEffect } from 'react';
import { convertColorToHex } from '../../utils/colorUtils';
import { statisticsService } from '../../services';

const Dashboard: React.FC = () => {
  const [groups, setGroups] = useState<GroupeType | null>(null);
  const [departments, setDepartments] = useState<DepartementType | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [groupResponse, departmentResponse] = await Promise.all([
          statisticsService.getGroupStatistics(),
          statisticsService.getDepartmentStatistics()
        ]);

        setGroups(groupResponse.data);
        setDepartments(departmentResponse.data);
      } catch (error) {
        console.error("Erreur lors du chargement des statistiques:", error);
      }
    };

    fetchStats();
  }, []);

  // Transformation avec conversion des couleurs
  const groupsData = groups?.data?.groupes?.map(groupe => ({
    name: groupe.nom,
    value: groupe.membres_count,
    color: convertColorToHex(groupe.color)
  })) || [];

  const departmentsData = departments?.data?.departements?.map(departement => ({
    name: departement.nom,
    value: departement.membres_count,
    color: convertColorToHex(departement.color)
  })) || [];

  return (
    <div>
      {/* Graphiques avec couleurs converties */}
      <PieChart data={groupsData} />
      <PieChart data={departmentsData} />
    </div>
  );
};
```

### Composant de carte statistique

```typescript
import React from 'react';
import { convertColorToHex, getColorWithAlpha } from '../../utils/colorUtils';

interface StatsCardProps {
  title: string;
  value: number;
  colorValue: string | number;
  icon: React.ComponentType;
}

const StatsCard: React.FC<StatsCardProps> = ({ title, value, colorValue, icon: Icon }) => {
  const hexColor = convertColorToHex(colorValue);
  const backgroundColor = getColorWithAlpha(hexColor, 0.1);

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
        </div>
        <div 
          className="p-3 rounded-full"
          style={{ backgroundColor }}
        >
          <Icon 
            className="w-6 h-6" 
            style={{ color: hexColor }}
          />
        </div>
      </div>
    </div>
  );
};
```

## Gestion des cas d'erreur

L'utilitaire gère automatiquement les cas d'erreur :

```typescript
// Valeurs null/undefined
convertColorToHex(null)        // → '#3B82F6' (couleur par défaut)
convertColorToHex(undefined)   // → '#3B82F6' (couleur par défaut)
convertColorToHex('')          // → '#3B82F6' (couleur par défaut)

// Valeurs numériques hors palette
convertColorToHex('999')       // → Couleur générée basée sur la valeur
convertColorToHex('abc')       // → Couleur générée basée sur la chaîne

// Valeurs hexadécimales invalides
convertColorToHex('#invalid')  // → Couleur générée basée sur la chaîne
```

## Personnalisation

### Ajouter de nouvelles couleurs à la palette

```typescript
// Dans colorUtils.ts
export const COLOR_PALETTE = {
  // ... couleurs existantes
  '31': '#FF9999',  // Nouvelle couleur
  '32': '#99FF99',  // Nouvelle couleur
  '33': '#9999FF',  // Nouvelle couleur
} as const;
```

### Modifier les couleurs par défaut

```typescript
// Dans colorUtils.ts
export const DEFAULT_COLORS = {
  primary: '#YOUR_COLOR',    // Votre couleur principale
  secondary: '#YOUR_COLOR',  // Votre couleur secondaire
  // ... autres couleurs
} as const;
```

## Tests et démonstration

### Composant de démonstration

Un composant `ColorDemo` est disponible pour tester toutes les fonctionnalités :

```typescript
import ColorDemo from '../components/Utils/ColorDemo';

// Dans votre application
<ColorDemo />
```

### Tests manuels

```typescript
// Test de conversion
console.log(convertColorToHex('1')); // → '#FF6B6B'
console.log(convertColorToHex('2')); // → '#4ECDC4'

// Test de couleur par nom
console.log(getColorByName('Groupe A')); // → Couleur cohérente

// Test de variations
console.log(darkenColor('#FF6B6B', 30)); // → Couleur assombrie
console.log(lightenColor('#FF6B6B', 30)); // → Couleur éclaircie
```

## Bonnes pratiques

1. **Toujours utiliser `convertColorToHex()`** pour les valeurs de couleur du backend
2. **Utiliser `getColorByName()`** pour une cohérence visuelle basée sur les noms
3. **Gérer les cas d'erreur** avec des couleurs de fallback
4. **Utiliser les variations** (`darkenColor`, `lightenColor`) pour créer des hiérarchies visuelles
5. **Tester les contrastes** avec `getContrastColor()` pour l'accessibilité

## Performance

- Les conversions sont rapides et optimisées
- La palette est en cache (const)
- Les fonctions sont pures (même entrée = même sortie)
- Pas d'appels réseau ou de calculs complexes

## Compatibilité

- ✅ TypeScript
- ✅ React
- ✅ Tous les navigateurs modernes
- ✅ SSR (Server-Side Rendering)
- ✅ Tests unitaires

## Support

Pour toute question ou problème avec l'utilitaire de couleur :

1. Consultez la documentation ci-dessus
2. Utilisez le composant `ColorDemo` pour tester
3. Vérifiez les logs de la console pour les erreurs
4. Testez avec différentes valeurs d'entrée
