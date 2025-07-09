# Services API - Documentation Complète

Ce document décrit tous les services API créés pour l'application Harvest Management.

## Architecture des Services

Tous les services suivent le pattern **Singleton** et utilisent le service API de base pour communiquer avec le backend Django.

### Structure commune

```typescript
export class ServiceName {
  private static instance: ServiceName;
  
  private constructor() {}
  
  public static getInstance(): ServiceName {
    if (!ServiceName.instance) {
      ServiceName.instance = new ServiceName();
    }
    return ServiceName.instance;
  }
  
  // Méthodes CRUD et métier
}
```

## Services Disponibles

### 1. Service d'Authentification (`authService`)

Gère l'authentification des utilisateurs.

```typescript
import { authService } from '../services';

// Connexion
const response = await authService.login({ email: 'user@example.com', password: 'password' });

// Vérification de l'authentification
const user = await authService.checkAuth();

// Déconnexion
await authService.logout();
```

**Méthodes principales :**
- `login(credentials)` - Connexion utilisateur
- `logout()` - Déconnexion
- `checkAuth()` - Vérification de l'authentification
- `getToken()` - Récupération du token
- `getUser()` - Récupération de l'utilisateur
- `isAuthenticated()` - Vérification si connecté

### 2. Service des Membres (`memberService`)

Gère les opérations CRUD des membres.

```typescript
import { memberService } from '../services';

// Récupérer tous les membres
const members = await memberService.getMembers();

// Créer un nouveau membre
const newMember = await memberService.createMember({
  nom: 'Doe',
  prenom: 'John',
  email: 'john@example.com',
  telephone: '+1234567890',
  groupe_id: 1,
  genre: 'Masculin',
  tag_ids: [1, 2],
  departement_id: 1,
  situation_matrimoniale: 'Célibataire'
});

// Rechercher des membres
const searchResults = await memberService.searchMembers('John');
```

**Méthodes principales :**
- `getMembers(filters?)` - Liste des membres avec filtres
- `getMember(id)` - Détails d'un membre
- `createMember(data)` - Créer un membre
- `updateMember(data)` - Mettre à jour un membre
- `deleteMember(id)` - Supprimer un membre
- `searchMembers(query)` - Recherche de membres
- `getMemberStatistics()` - Statistiques des membres
- `exportMembers(filters?, format?)` - Export des membres
- `importMembers(file)` - Import de membres

### 3. Service des Événements (`eventService`)

Gère les événements et leurs inscriptions.

```typescript
import { eventService } from '../services';

// Récupérer les événements à venir
const upcomingEvents = await eventService.getUpcomingEvents(10);

// Créer un événement
const newEvent = await eventService.createEvent({
  title: 'Réunion mensuelle',
  description: 'Réunion de l\'équipe',
  date: '2024-01-15',
  time: '14:00',
  location: 'Salle de conférence',
  type: 'meeting',
  maxAttendees: 50
});

// S'inscrire à un événement
await eventService.registerForEvent({
  event_id: '1',
  member_id: 123,
  notes: 'Je serai présent'
});
```

**Méthodes principales :**
- `getEvents(filters?)` - Liste des événements
- `getUpcomingEvents(limit?)` - Événements à venir
- `getPastEvents(limit?)` - Événements passés
- `createEvent(data)` - Créer un événement
- `registerForEvent(data)` - S'inscrire
- `unregisterFromEvent(eventId, memberId)` - Se désinscrire
- `getEventAttendees(eventId)` - Participants
- `cancelEvent(eventId, reason?)` - Annuler un événement

### 4. Service des Rendez-vous (`appointmentService`)

Gère les rendez-vous et leur planning.

```typescript
import { appointmentService } from '../services';

// Récupérer les rendez-vous du jour
const todayAppointments = await appointmentService.getTodayAppointments();

// Créer un rendez-vous
const newAppointment = await appointmentService.createAppointment({
  title: 'Consultation',
  client: 'Jean Dupont',
  date: '2024-01-15',
  time: '10:00',
  duration: 60,
  notes: 'Première consultation'
});

// Confirmer un rendez-vous
await appointmentService.confirmAppointment({
  appointment_id: '1',
  confirmed: true,
  notes: 'Confirmé par téléphone'
});
```

**Méthodes principales :**
- `getAppointments(filters?)` - Liste des rendez-vous
- `getTodayAppointments()` - Rendez-vous du jour
- `getWeekAppointments()` - Rendez-vous de la semaine
- `createAppointment(data)` - Créer un rendez-vous
- `confirmAppointment(data)` - Confirmer un rendez-vous
- `cancelAppointment(id, reason?)` - Annuler un rendez-vous
- `rescheduleAppointment(id, newDate, newTime)` - Reprogrammer
- `checkAvailability(date, time, duration)` - Vérifier disponibilité

### 5. Service des Départements (`departmentService`)

Gère les départements de l'organisation.

```typescript
import { departmentService } from '../services';

// Récupérer tous les départements
const departments = await departmentService.getDepartments();

// Créer un département
const newDepartment = await departmentService.createDepartment({
  nom: 'Ressources Humaines',
  mission: 'Gestion du personnel',
  color: '#FF6B6B',
  responsable_id: 123
});

// Récupérer les statistiques d'un département
const stats = await departmentService.getDepartmentStatistics('1');
```

**Méthodes principales :**
- `getDepartments(filters?)` - Liste des départements
- `createDepartment(data)` - Créer un département
- `getDepartmentStatistics(id)` - Statistiques du département
- `getDepartmentMembers(id, filters?)` - Membres du département
- `assignResponsible(id, memberId)` - Assigner un responsable
- `exportDepartments(filters?, format?)` - Export des départements

### 6. Service des Groupes (`groupService`)

Gère les groupes de membres.

```typescript
import { groupService } from '../services';

// Récupérer tous les groupes
const groups = await groupService.getGroups();

// Créer un groupe
const newGroup = await groupService.createGroup({
  nom: 'Groupe Alpha',
  description: 'Groupe de nouveaux membres',
  color: '#4ECDC4',
  departement_id: 1
});

// Ajouter des membres au groupe
await groupService.addMembersToGroup('1', [123, 124, 125]);
```

**Méthodes principales :**
- `getGroups(filters?)` - Liste des groupes
- `createGroup(data)` - Créer un groupe
- `getGroupStatistics(id)` - Statistiques du groupe
- `addMembersToGroup(id, memberIds)` - Ajouter des membres
- `removeMembersFromGroup(id, memberIds)` - Retirer des membres
- `assignResponsible(id, memberId)` - Assigner un responsable

### 7. Service des Tags (`tagService`)

Gère les tags pour catégoriser les membres.

```typescript
import { tagService } from '../services';

// Récupérer tous les tags
const tags = await tagService.getTags();

// Créer un tag
const newTag = await tagService.createTag({
  nom: 'Bénévole',
  description: 'Membre bénévole',
  color: '#45B7D1',
  category: 'Statut'
});

// Récupérer les tags populaires
const popularTags = await tagService.getPopularTags(10);
```

**Méthodes principales :**
- `getTags(filters?)` - Liste des tags
- `createTag(data)` - Créer un tag
- `getPopularTags(limit?)` - Tags populaires
- `getTagsByCategory(category)` - Tags par catégorie
- `mergeTags(sourceId, targetId)` - Fusionner des tags
- `getTagSuggestions(query, limit?)` - Suggestions de tags

### 8. Service des Étapes (`etapeService`)

Gère les étapes du processus d'intégration.

```typescript
import { etapeService } from '../services';

// Récupérer les étapes ordonnées
const etapes = await etapeService.getEtapesOrdered();

// Créer une étape
const newEtape = await etapeService.createEtape({
  libelle: 'Formation initiale',
  description: 'Formation de base pour nouveaux membres',
  ordre: 1,
  couleur: '#96CEB4',
  duree_estimee: 7
});

// Assigner un membre à une étape
await etapeService.assignMemberToEtape('1', 123);
```

**Méthodes principales :**
- `getEtapes(filters?)` - Liste des étapes
- `getEtapesOrdered()` - Étapes ordonnées
- `createEtape(data)` - Créer une étape
- `reorderEtapes(etapeIds)` - Réorganiser les étapes
- `assignMemberToEtape(id, memberId)` - Assigner un membre
- `completeEtapeForMember(id, memberId, notes?)` - Marquer comme terminée

### 9. Service des Statistiques (`statisticsService`)

Gère les statistiques et rapports.

```typescript
import { statisticsService } from '../services';

// Récupérer les statistiques du tableau de bord
const dashboardStats = await statisticsService.getDashboardStats();

// Statistiques des membres
const memberStats = await statisticsService.getMemberStatistics({
  date_from: '2024-01-01',
  date_to: '2024-12-31'
});

// Statistiques de croissance
const growthStats = await statisticsService.getGrowthStatistics('month');
```

**Méthodes principales :**
- `getDashboardStats()` - Statistiques du tableau de bord
- `getMemberStatistics(filters?)` - Statistiques des membres
- `getEventStatistics(filters?)` - Statistiques des événements
- `getGrowthStatistics(period)` - Statistiques de croissance
- `getGeographicStatistics()` - Statistiques géographiques
- `generateCustomReport(config)` - Rapport personnalisé
- `exportStatistics(type, filters?, format?)` - Export des statistiques

## Utilisation dans les Composants

### Exemple d'utilisation dans un composant React

```typescript
import React, { useState, useEffect } from 'react';
import { memberService, MemberType } from '../services';

const MembersList: React.FC = () => {
  const [members, setMembers] = useState<MemberType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadMembers();
  }, []);

  const loadMembers = async () => {
    try {
      setLoading(true);
      const response = await memberService.getMembers();
      setMembers(response.data);
    } catch (error: any) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateMember = async (memberData: CreateMemberData) => {
    try {
      const response = await memberService.createMember(memberData);
      setMembers(prev => [...prev, response.data]);
    } catch (error: any) {
      setError(error.message);
    }
  };

  if (loading) return <div>Chargement...</div>;
  if (error) return <div>Erreur: {error}</div>;

  return (
    <div>
      {members.map(member => (
        <div key={member.id}>
          {member.nom} {member.prenom} - {member.email}
        </div>
      ))}
    </div>
  );
};
```

## Gestion des Erreurs

Tous les services utilisent une gestion d'erreur centralisée :

```typescript
try {
  const response = await memberService.getMembers();
  // Traitement du succès
} catch (error: any) {
  // L'erreur est déjà formatée par le service API
  console.error('Erreur:', error.message);
  
  // Affichage des erreurs de validation
  if (error.errors) {
    Object.entries(error.errors).forEach(([field, messages]) => {
      console.error(`${field}: ${messages.join(', ')}`);
    });
  }
}
```

## Configuration des Endpoints

Tous les endpoints sont configurés dans `src/config/environment.ts` :

```typescript
export const config = {
  ENDPOINTS: {
    MEMBERS: {
      LIST: '/api/members/',
      CREATE: '/api/members/',
      DETAIL: (id: number) => `/api/members/${id}/`,
      // ...
    },
    // ...
  }
};
```

## Bonnes Pratiques

1. **Utilisation du pattern Singleton** : Chaque service a une instance unique
2. **Gestion d'erreurs centralisée** : Toutes les erreurs sont formatées de manière cohérente
3. **Types TypeScript** : Tous les services sont typés pour la sécurité
4. **Intercepteurs Axios** : Authentification automatique et gestion des erreurs
5. **Filtres et pagination** : Support des filtres et de la pagination
6. **Export/Import** : Fonctionnalités d'export et d'import pour les données
7. **Statistiques** : Services dédiés aux statistiques et rapports

## Installation et Configuration

1. Installer les dépendances :
```bash
npm install axios @types/node
```

2. Configurer les variables d'environnement :
```env
VITE_API_URL=http://localhost:8000
```

3. Importer et utiliser les services :
```typescript
import { memberService, eventService, statisticsService } from '../services';
``` 