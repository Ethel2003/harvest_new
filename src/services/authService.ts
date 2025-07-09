import { apiService, ApiResponse, ApiError } from './api';

// Interfaces pour l'authentification
export interface LoginCredentials {
    email: string;
    password: string;
}

export interface RegisterData {
    username: string;
    email: string;
    password: string;
    password_confirm: string;
}

export interface User {
    id: number;
    username: string;
    email: string;
    first_name?: string;
    last_name?: string;
    is_active: boolean;
    date_joined: string;
}

export interface AuthResponse {
    data: {
        token: string;
        user: User;
    }
}

// Ré-export de ApiError pour la cohérence
export type { ApiError };

// Service d'authentification
export class AuthService {
    private static instance: AuthService;

    private constructor() { }

    public static getInstance(): AuthService {
        if (!AuthService.instance) {
            AuthService.instance = new AuthService();
        }
        return AuthService.instance;
    }

    // Connexion utilisateur
    async login(credentials: LoginCredentials): Promise<ApiResponse<AuthResponse>> {
        try {
            const response = await apiService.post<AuthResponse>('/api/login', credentials);
            console.log("Login response", response);

            // Stockage du token
            if (response.data.data.token) {
                localStorage.setItem('authToken', response.data.data.token);
                localStorage.setItem('user', JSON.stringify(response.data.data.user));
            }

            return response;
        } catch (error) {
            throw error;
        }
    }

    // Inscription utilisateur
    // async register(userData: RegisterData): Promise<ApiResponse<AuthResponse>> {
    //     try {
    //         const response = await apiService.post<AuthResponse>('/api/auth/register/', userData);

    //         // Stockage du token après inscription
    //         if (response.data.token) {
    //             localStorage.setItem('authToken', response.data.token);
    //             localStorage.setItem('user', JSON.stringify(response.data.user));
    //         }

    //         return response;
    //     } catch (error) {
    //         throw error;
    //     }
    // }

    // Déconnexion utilisateur
    async logout(): Promise<void> {
        try {
            await apiService.post('/api/logout');
        } catch (error) {
            console.error('Erreur lors de la déconnexion:', error);
        } finally {
            // Suppression des données locales
            localStorage.removeItem('authToken');
            localStorage.removeItem('user');
        }
    }

    // Vérification de l'authentification
    async checkAuth(): Promise<ApiResponse<User>> {
        try {
            return await apiService.get<User>('/api/verify-token');
        } catch (error) {
            // Si l'utilisateur n'est pas authentifié, supprimer les données locales
            localStorage.removeItem('authToken');
            localStorage.removeItem('user');
            throw error;
        }
    }

    // Récupération du token stocké
    getToken(): string | null {
        return localStorage.getItem('authToken');
    }

    // Récupération de l'utilisateur stocké
    getUser(): User | null {
        const userStr = localStorage.getItem('user');
        if (userStr) {
            try {
                return JSON.parse(userStr);
            } catch (error) {
                console.error('Erreur lors du parsing de l\'utilisateur:', error);
                return null;
            }
        }
        return null;
    }

    // Vérification si l'utilisateur est connecté
    isAuthenticated(): boolean {
        return !!this.getToken();
    }

    // Rafraîchissement du token (si nécessaire)
    async refreshToken(): Promise<ApiResponse<{ token: string }>> {
        try {
            const response = await apiService.post<{ token: string }>('/api/verify-token');

            if (response.data.token) {
                localStorage.setItem('authToken', response.data.token);
            }

            return response;
        } catch (error) {
            throw error;
        }
    }
}

// Export de l'instance unique
export const authService = AuthService.getInstance(); 