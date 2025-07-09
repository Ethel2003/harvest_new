# Statistiques des Utilisateurs

## Vue d'ensemble

Ce module fournit des statistiques détaillées sur les utilisateurs de l'application, permettant de suivre l'évolution de la base utilisateurs et d'analyser leur répartition.

## Endpoint API

### GET /api/users/statistiques/

Retourne les statistiques complètes des utilisateurs.

#### Réponse

```json
{
  "success": true,
  "data": {
    "statistiques_globales": {
      "total_users": 15,
      "users_actifs": 12,
      "users_inactifs": 3,
      "nouveaux_users": 2
    },
    "repartition_roles": {
      "Admin": 3,
      "Utilisateur": 12
    },
    "repartition_date_creation": {
      "2024-01": 5,
      "2024-02": 8,
      "2024-03": 2
    }
  }
}
```

#### Détails des champs

**statistiques_globales :**
- `total_users` : Nombre total d'utilisateurs dans le système
- `users_actifs` : Nombre d'utilisateurs actifs (is_active=True)
- `users_inactifs` : Nombre d'utilisateurs inactifs (is_active=False)
- `nouveaux_users` : Nombre d'utilisateurs créés ce mois

**repartition_roles :**
- Objet avec les noms des groupes/roles comme clés et le nombre d'utilisateurs comme valeurs

**repartition_date_creation :**
- Objet avec les mois (format YYYY-MM) comme clés et le nombre d'utilisateurs créés comme valeurs

## Frontend

### Interface TypeScript

```typescript
export interface UserStatistiquesJSON {
  data: {
    statistiques_globales: {
      total_users: number
      users_actifs: number
      users_inactifs: number
      nouveaux_users: number
    }
    repartition_roles: {
      [key: string]: number
    }
    repartition_date_creation: {
      [key: string]: number
    }
  }
}
```

### Composable Vue.js

```typescript
const { users, getUsers, getUsersStatistiques, usersStatistiques } = useUsers()

// Récupérer les statistiques
await getUsersStatistiques()

// Accéder aux données
const totalUsers = usersStatistiques.value.data.statistiques_globales.total_users
```

### Utilisation dans le template

```vue
<template>
  <VBlock
    :title="usersCount.toString()"
    subtitle="Nombre d'utilisateurs"
    center
    m-responsive
    t-responsive
  >
    <template #icon>
      <VIconBox color="green" rounded>
        <i class="fas fa-user-friends" aria-hidden="true"></i>
      </VIconBox>
    </template>
  </VBlock>
</template>

<script setup>
const usersCount = ref(0)

onMounted(async () => {
  await getUsersStatistiques()
  usersCount.value = usersStatistiques.value.data.statistiques_globales.total_users
})
</script>
```

## Tests

### Script de test

Le script `test_users_statistiques.py` permet de tester l'endpoint :

```bash
cd new_harvest_back/scriptsTests
python test_users_statistiques.py
```

### Tests automatisés

Pour exécuter tous les tests API incluant les statistiques des utilisateurs :

```bash
cd new_harvest_back/scriptsTests
python run_all_api_tests.py
```

## Permissions

- **Endpoint statistiques** : Accessible aux utilisateurs authentifiés
- **Données sensibles** : Les statistiques ne révèlent pas d'informations personnelles des utilisateurs

## Performance

- **Optimisation** : Utilise des requêtes optimisées avec `Count()` et `annotate()`
- **Cache** : Les statistiques peuvent être mises en cache côté client
- **Fréquence** : Recommandé de rafraîchir les statistiques périodiquement (ex: toutes les heures)

## Évolutions futures

- Ajout de statistiques par département d'activité
- Historique des connexions
- Statistiques de performance des utilisateurs
- Export des données en CSV/Excel 