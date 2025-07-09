# Modèle Regroupements - Documentation

## Vue d'ensemble

Le modèle `Regroupements` a été implémenté pour gérer la relation many-to-many entre les `Membres` et les `Groupes`. Ce modèle remplace les anciennes relations indirectes via les modèles `Degre` et `Integration`.

## Architecture

### Modèle Regroupements

```python
class Regroupements(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='regroupements')
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='regroupements')
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_sortie = models.DateTimeField(null=True, blank=True)
    actif = models.BooleanField(default=True)
  
    class Meta:
        unique_together = ['membre', 'groupe']
```

### Fonctionnalités

- **Relation many-to-many** : Un membre peut appartenir à plusieurs groupes, un groupe peut avoir plusieurs membres
- **Gestion des états** : Champ `actif` pour marquer les appartenances actives/inactives
- **Historique** : Dates d'inscription et de sortie pour tracer l'historique
- **Contrainte d'unicité** : Un membre ne peut pas être dans le même groupe plusieurs fois

## API Endpoints

### Regroupements

#### Liste des regroupements

```
GET /api/regroupements/
```

#### Regroupements actifs

```
GET /api/regroupements/actifs/
```

#### Ajouter un membre à un groupe

```
POST /api/regroupements/ajouter_membre_groupe/
{
    "membre_id": 1,
    "groupe_id": 2
}
```

#### CRUD standard

```
GET /api/regroupements/{id}/
POST /api/regroupements/
PUT /api/regroupements/{id}/
DELETE /api/regroupements/{id}/
```

### Groupes (mise à jour)

#### Liste des groupes avec nombre de membres

```
GET /api/groupes/
```

**Nouveau champ** : `nombre_membres` calculé automatiquement

#### Statistiques des groupes

```
GET /api/groupes/statistiques/
```

Retourne :

- Liste des groupes avec nombre de membres
- Statistiques globales (total, moyenne, groupe le plus populaire)

#### Ajouter des membres à un groupe

```
POST /api/groupes/{id}/insert_membre/
{
    "membre_ids": [1, 2, 3]
}
```

#### Retirer des membres d'un groupe

```
POST /api/groupes/{id}/remove_membre/
{
    "membre_ids": [1, 2, 3]
}
```

## Migration des données

### Script de migration

Le script `scriptsTests/migrate_existing_data.py` permet de migrer les données existantes :

```bash
cd new_harvest_back
python scriptsTests/migrate_existing_data.py
```

Ce script :

1. Migre les relations `Degre` vers `Regroupements`
2. Migre les relations `Integration` vers `Regroupements`
3. Vérifie l'intégrité des données
4. Génère des statistiques

### Exécution des migrations Django

```bash
cd new_harvest_back
python manage.py makemigrations
python manage.py migrate
```

## Tests

### Script de test complet

Le script `scriptsTests/test_regroupements_complet.py` teste toutes les fonctionnalités :

```bash
cd new_harvest_back
python scriptsTests/test_regroupements_complet.py
```

Tests inclus :

- ✅ Création de groupes et membres
- ✅ Ajout/retrait de membres dans les groupes
- ✅ Calcul du nombre de membres par groupe
- ✅ Statistiques globales
- ✅ Liste des regroupements actifs
- ✅ Vérification des contraintes d'unicité

## Utilisation dans le frontend

### Récupération des groupes avec effectifs

```typescript
// Récupérer la liste des groupes avec nombre de membres
const response = await fetch('/api/groupes/', {
  headers: {
    'Authorization': `Token ${token}`,
    'Content-Type': 'application/json'
  }
});

const data = await response.json();
// Chaque groupe contient maintenant le champ 'nombre_membres'
```

### Statistiques des groupes

```typescript
// Récupérer les statistiques détaillées
const response = await fetch('/api/groupes/statistiques/', {
  headers: {
    'Authorization': `Token ${token}`,
    'Content-Type': 'application/json'
  }
});

const data = await response.json();
// Contient les statistiques globales et par groupe
```

### Gestion des regroupements

```typescript
// Ajouter un membre à un groupe
const response = await fetch('/api/regroupements/ajouter_membre_groupe/', {
  method: 'POST',
  headers: {
    'Authorization': `Token ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    membre_id: 1,
    groupe_id: 2
  })
});
```

## Avantages de cette implémentation

### 1. **Simplicité**

- Relation directe et claire entre Membres et Groupes
- Plus besoin de passer par des modèles intermédiaires complexes

### 2. **Performance**

- Requêtes optimisées avec `prefetch_related`
- Calcul automatique du nombre de membres
- Index sur les clés étrangères

### 3. **Flexibilité**

- Gestion des états actif/inactif
- Historique des appartenances
- Contraintes d'unicité configurables

### 4. **Maintenabilité**

- Code plus lisible et maintenable
- API RESTful cohérente
- Documentation complète

### 5. **Évolutivité**

- Facile d'ajouter de nouveaux champs
- Support pour des fonctionnalités futures
- Compatible avec les standards Django

## Migration depuis l'ancien système

### Avant (via Degre/Integration)

```python
# Ancienne façon de récupérer les membres d'un groupe
membres = Membre.objects.filter(degre__groupe=groupe)
# ou
membres = Membre.objects.filter(integration__groupe=groupe)
```

### Après (via Regroupements)

```python
# Nouvelle façon plus simple
membres = Membre.objects.filter(regroupements__groupe=groupe, regroupements__actif=True)
# ou directement depuis le groupe
membres = groupe.regroupements.filter(actif=True).values_list('membre', flat=True)
```

## Sécurité et validation

- **Authentification requise** pour toutes les opérations
- **Validation des données** côté serveur
- **Contraintes d'unicité** pour éviter les doublons
- **Gestion des erreurs** avec messages explicites

## Support et maintenance

Pour toute question ou problème :

1. Consulter les logs Django
2. Exécuter les scripts de test
3. Vérifier l'intégrité des données avec le script de migration
4. Consulter la documentation de l'API

---

**Date de création** : 2025-06-30
**Version** : 1.0
**Auteur** : Brunice
