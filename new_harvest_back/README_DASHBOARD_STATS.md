# Endpoint des Statistiques du Tableau de Bord

## Vue d'ensemble

L'endpoint `/api/statistics/dashboard/` permet de récupérer les statistiques principales du tableau de bord de l'application Harvest.

## Endpoint

### GET /api/statistics/dashboard/

**Description:** Récupère le nombre total d'utilisateurs, groupes, départements et membres.

**URL:** `http://localhost:8000/api/statistics/dashboard/`

**Méthode:** `GET`

**Authentification:** Requise (Token d'authentification)

**Headers requis:**
```
Authorization: Token <votre_token>
Content-Type: application/json
```

## Format de la réponse

### Succès (200 OK)

```json
{
  "departments": 5,
  "groups": 12,
  "users": 8,
  "members": 150
}
```

### Erreur d'authentification (401 Unauthorized)

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Erreur serveur (500 Internal Server Error)

```json
{
  "error": "Erreur lors de la récupération des statistiques: <message_d_erreur>"
}
```

## Champs de la réponse

| Champ | Type | Description |
|-------|------|-------------|
| `departments` | number | Nombre total de départements |
| `groups` | number | Nombre total de groupes |
| `users` | number | Nombre total d'utilisateurs (User Django) |
| `members` | number | Nombre total de membres |

## Exemples d'utilisation

### cURL

```bash
# Récupérer les statistiques
curl -X GET \
  http://localhost:8000/api/statistics/dashboard/ \
  -H "Authorization: Token votre_token_ici" \
  -H "Content-Type: application/json"
```

### JavaScript/TypeScript (Frontend)

```typescript
import { statisticsService } from '../services';

// Récupérer les statistiques du tableau de bord
const loadDashboardStats = async () => {
  try {
    const response = await statisticsService.getDashboardStats();
    console.log('Statistiques:', response.data);
    
    // Utiliser les données
    const { departments, groups, users, members } = response.data;
    
  } catch (error) {
    console.error('Erreur:', error);
  }
};
```

### Python (Backend)

```python
import requests

def get_dashboard_stats(token):
    url = "http://localhost:8000/api/statistics/dashboard/"
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erreur {response.status_code}: {response.text}")
```

## Implémentation côté Backend

### Vue Django (views.py)

```python
class DashboardStatsView(APIView):
    """
    Vue pour récupérer les statistiques du tableau de bord.
    Retourne le nombre d'utilisateurs, groupes, départements et membres.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            # Compter les départements
            departments_count = Departement.objects.count()
            
            # Compter les groupes
            groups_count = Groupe.objects.count()
            
            # Compter les utilisateurs (User de Django)
            users_count = User.objects.count()
            
            # Compter les membres
            members_count = Membre.objects.count()
            
            # Préparer la réponse au format demandé
            stats = {
                "departments": departments_count,
                "groups": groups_count,
                "users": users_count,
                "members": members_count
            }
            
            return Response(stats, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": f"Erreur lors de la récupération des statistiques: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

### URL (urls.py)

```python
urlpatterns = [
    # ... autres URLs ...
    path('statistics/dashboard', DashboardStatsView.as_view(), name='dashboard-stats'),
    # ... autres URLs ...
]
```

## Implémentation côté Frontend

### Service TypeScript

```typescript
// src/services/statisticsService.ts
import { apiService } from './apiService';
import { DashboardStats } from '../types';

class StatisticsService {
  private static instance: StatisticsService;

  private constructor() {}

  public static getInstance(): StatisticsService {
    if (!StatisticsService.instance) {
      StatisticsService.instance = new StatisticsService();
    }
    return StatisticsService.instance;
  }

  async getDashboardStats(): Promise<ApiResponse<DashboardStats>> {
    try {
      return await apiService.get<DashboardStats>('/api/statistics/dashboard/');
    } catch (error) {
      throw error;
    }
  }
}

export const statisticsService = StatisticsService.getInstance();
```

### Type TypeScript

```typescript
// src/types/index.ts
export interface DashboardStats {
  departments: number;
  groups: number;
  users: number;
  members: number;
}
```

### Composant React

```typescript
// src/components/Dashboard/DashboardStats.tsx
import React, { useState, useEffect } from 'react';
import { statisticsService } from '../../services';
import { DashboardStats } from '../../types';

const DashboardStatsComponent: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardStats();
  }, []);

  const loadDashboardStats = async () => {
    try {
      const response = await statisticsService.getDashboardStats();
      setStats(response.data);
    } catch (error) {
      console.error('Erreur:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Chargement...</div>;
  if (!stats) return <div>Aucune donnée</div>;

  return (
    <div>
      <h2>Statistiques du Tableau de Bord</h2>
      <p>Départements: {stats.departments}</p>
      <p>Groupes: {stats.groups}</p>
      <p>Utilisateurs: {stats.users}</p>
      <p>Membres: {stats.members}</p>
    </div>
  );
};
```

## Tests

### Script de test Python

```bash
# Tester l'endpoint
python test_dashboard_stats.py

# Créer des données de test et tester
python test_dashboard_stats.py --create-data
```

### Test manuel

1. **Démarrer le serveur Django:**
   ```bash
   python manage.py runserver
   ```

2. **Se connecter pour obtenir un token:**
   ```bash
   curl -X POST http://localhost:8000/api/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "votre_username", "password": "votre_password"}'
   ```

3. **Appeler l'endpoint des statistiques:**
   ```bash
   curl -X GET http://localhost:8000/api/statistics/dashboard/ \
     -H "Authorization: Token votre_token_ici"
   ```

## Sécurité

- **Authentification requise:** L'endpoint nécessite un token d'authentification valide
- **Permissions:** Seuls les utilisateurs authentifiés peuvent accéder aux statistiques
- **Validation:** Les données sont validées côté serveur avant d'être retournées

## Performance

- **Requêtes optimisées:** Utilisation de `count()` pour des requêtes rapides
- **Cache:** Possibilité d'ajouter du cache pour améliorer les performances
- **Indexation:** Les modèles utilisés sont déjà indexés par défaut

## Évolutions futures

- Ajout de statistiques temporelles (évolution dans le temps)
- Filtres par période (mois, trimestre, année)
- Statistiques détaillées par département/groupe
- Export des statistiques en CSV/Excel
- Graphiques et visualisations

## Support

Pour toute question ou problème avec cet endpoint, consultez:
- La documentation de l'API
- Les logs du serveur Django
- Le script de test fourni 