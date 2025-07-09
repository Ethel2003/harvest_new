# Configuration Frontend-Backend

Ce document explique comment configurer la liaison entre le frontend React et le backend Django.

## Configuration requise

### 1. Dépendances à installer

```bash
cd frontend
npm install axios @types/node
```

### 2. Variables d'environnement

Créez un fichier `.env.local` dans le dossier `frontend/` :

```env
# Configuration de l'API
VITE_API_URL=http://localhost:8000

# Configuration de l'environnement
VITE_NODE_ENV=development
```

## Architecture de la liaison

### 1. Configuration Vite (vite.config.ts)

Le proxy Vite est configuré pour rediriger les appels `/api` vers le backend Django :

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      secure: false,
    },
  },
},
```

### 2. Service API (src/services/api.ts)

Le service API utilise Axios pour communiquer avec le backend :

- **Configuration automatique** : URL de base, timeouts, headers
- **Intercepteurs** : Ajout automatique du token d'authentification
- **Gestion d'erreurs** : Redirection automatique en cas d'erreur 401
- **Pattern Singleton** : Instance unique pour toute l'application

### 3. Service d'authentification (src/services/authService.ts)

Gère l'authentification avec le backend Django :

- **Connexion** : `POST /api/auth/login/`
- **Inscription** : `POST /api/auth/register/`
- **Déconnexion** : `POST /api/auth/logout/`
- **Vérification** : `GET /api/auth/user/`
- **Stockage local** : Token et données utilisateur

### 4. Contexte d'authentification (src/contexts/AuthContext.tsx)

Fournit l'état d'authentification à toute l'application :

- **État global** : Utilisateur connecté, chargement, erreurs
- **Méthodes** : Login, logout, register, resetPassword
- **Persistance** : Vérification automatique au chargement

### 5. Configuration centralisée (src/config/environment.ts)

Configuration centralisée pour toute l'application :

- **URLs d'API** : Endpoints pour chaque ressource
- **Messages d'erreur** : Messages standardisés
- **Validation** : Règles de validation des formulaires

## Utilisation

### 1. Connexion utilisateur

```typescript
import { useAuth } from '../contexts/AuthContext';

const { login, error, isLoading } = useAuth();

const handleLogin = async () => {
  try {
    await login({ username: 'user', password: 'password' });
    // Redirection automatique après connexion
  } catch (error) {
    // Gestion des erreurs
  }
};
```

### 2. Appels API authentifiés

```typescript
import { apiService } from '../services/api';

// Les appels incluent automatiquement le token d'authentification
const response = await apiService.get('/api/members/');
const members = response.data;
```

### 3. Gestion des erreurs

```typescript
import { ApiError } from '../services/api';

try {
  const response = await apiService.post('/api/members/', memberData);
} catch (error) {
  const apiError = error as ApiError;
  console.error(apiError.message);
  // Affichage des erreurs de validation
  if (apiError.errors) {
    Object.entries(apiError.errors).forEach(([field, messages]) => {
      console.error(`${field}: ${messages.join(', ')}`);
    });
  }
}
```

## Sécurité

### 1. Authentification par token

- **Token d'authentification** : Stocké dans localStorage
- **Headers automatiques** : Ajout du token à chaque requête
- **Expiration** : Gestion automatique des tokens expirés

### 2. Protection CORS

Le backend Django est configuré avec `django-cors-headers` pour permettre les requêtes depuis le frontend.

### 3. Validation des données

- **Frontend** : Validation côté client avec les règles définies
- **Backend** : Validation côté serveur obligatoire
- **Messages d'erreur** : Affichage des erreurs de validation

## Développement

### 1. Démarrage en développement

```bash
# Terminal 1 - Backend Django
cd new_harvest_back
python manage.py runserver

# Terminal 2 - Frontend React
cd frontend
npm run dev
```

### 2. URLs d'accès

- **Frontend** : http://localhost:5173
- **Backend** : http://localhost:8000
- **API** : http://localhost:8000/api/

### 3. Debugging

- **Console navigateur** : Logs des appels API
- **Network tab** : Inspection des requêtes HTTP
- **Django debug** : Logs du backend dans le terminal

## Production

### 1. Variables d'environnement

```env
VITE_API_URL=https://votre-domaine.com
VITE_NODE_ENV=production
```

### 2. Build de production

```bash
cd frontend
npm run build
```

### 3. Configuration CORS

En production, configurez CORS dans Django pour restreindre les origines autorisées :

```python
CORS_ALLOWED_ORIGINS = [
    'https://votre-domaine-frontend.com',
]
```

## Troubleshooting

### 1. Erreur CORS

- Vérifiez que `django-cors-headers` est installé
- Vérifiez la configuration CORS dans `settings.py`
- Assurez-vous que l'URL du frontend est autorisée

### 2. Erreur d'authentification

- Vérifiez que le token est bien stocké dans localStorage
- Vérifiez que le token n'est pas expiré
- Vérifiez les logs du backend pour les erreurs d'authentification

### 3. Erreur de proxy

- Vérifiez que le backend Django fonctionne sur le port 8000
- Vérifiez la configuration du proxy dans `vite.config.ts`
- Redémarrez le serveur de développement

### 4. Erreurs TypeScript

- Installez les types nécessaires : `npm install @types/node`
- Vérifiez la configuration TypeScript dans `tsconfig.json`
- Assurez-vous que tous les imports sont corrects
