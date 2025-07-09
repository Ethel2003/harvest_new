import React, { createContext, useContext, useState, useEffect } from 'react';
// import { authService, User, LoginCredentials, RegisterData, ApiError } from '../services/authService';
import { authService, User, LoginCredentials, ApiError } from '../services/authService';
import { apiService } from '../services/api';

interface AuthContextType {
  user: User | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  // register: (userData: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  resetPassword: (email: string) => Promise<void>;
  isLoading: boolean;
  error: string | null;
  clearError: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Vérification de l'authentification au chargement
    const checkAuth = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        if (authService.isAuthenticated()) {
          const response = await authService.checkAuth();
          setUser(response.data);
        }
      } catch (error: any) {
        console.error('Erreur lors de la vérification de l\'authentification:', error);
        // L'erreur est gérée silencieusement car l'utilisateur peut ne pas être connecté
      } finally {
        setIsLoading(false);
      }
    };
    
    checkAuth();
  }, []);

  const login = async (credentials: LoginCredentials) => {
    try {
      setIsLoading(true);
      setError(null);
      
      const response = await authService.login(credentials);
      setUser(response.data.data.user);
    } catch (error: any) {
      const apiError = error as ApiError;
      setError(apiError.message || 'Erreur lors de la connexion');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // const register = async (userData: RegisterData) => {
  //   try {
  //     setIsLoading(true);
  //     setError(null);
      
  //     const response = await authService.register(userData);
  //     setUser(response.data.user);
  //   } catch (error: any) {
  //     const apiError = error as ApiError;
  //     setError(apiError.message || 'Erreur lors de l\'inscription');
  //     throw error;
  //   } finally {
  //     setIsLoading(false);
  //   }
  // };

  const logout = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      await authService.logout();
      setUser(null);
    } catch (error: any) {
      console.error('Erreur lors de la déconnexion:', error);
      // Même en cas d'erreur, on supprime les données locales
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const resetPassword = async (email: string) => {
    try {
      setIsLoading(true);
      setError(null);
      
      await apiService.post('/api/auth/reset-password/', { email });
    } catch (error: any) {
      const apiError = error as ApiError;
      setError(apiError.message || 'Erreur lors de la réinitialisation du mot de passe');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const clearError = () => {
    setError(null);
  };

  return (
    <AuthContext.Provider value={{ 
      user, 
      login, 
      // register,
      logout, 
      resetPassword, 
      isLoading, 
      error,
      clearError
    }}>
      {children}
    </AuthContext.Provider>
  );
};