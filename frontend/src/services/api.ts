import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { config } from '../config/environment';

// Configuration de base de l'API
const API_BASE_URL = config.API_URL;

// Interface pour les réponses API
export interface ApiResponse<T = any> {
  data: T;
  status: number;
  message?: string;
}

// Interface pour les erreurs API
export interface ApiError {
  message: string;
  status: number;
  errors?: Record<string, string[]>;
}

// Configuration de l'instance axios
const createApiInstance = (): AxiosInstance => {
  const instance = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Intercepteur pour ajouter le token d'authentification
  instance.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Token ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Intercepteur pour gérer les réponses
  instance.interceptors.response.use(
    (response: AxiosResponse) => {
      return response;
    },
    (error) => {
      // Gestion des erreurs d'authentification
      if (error.response?.status === 401) {
        localStorage.removeItem('authToken');
        window.location.href = '/login';
      }
      return Promise.reject(error);
    }
  );

  return instance;
};

// Instance API
const api = createApiInstance();

// Classe de service API générique
export class ApiService {
  private static instance: ApiService;
  private api: AxiosInstance;

  private constructor() {
    this.api = createApiInstance();
  }

  public static getInstance(): ApiService {
    if (!ApiService.instance) {
      ApiService.instance = new ApiService();
    }
    return ApiService.instance;
  }

  // Méthodes HTTP génériques
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.api.get<T>(url, config);
      return {
        data: response.data,
        status: response.status,
      };
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.api.post<T>(url, data, config);
      return {
        data: response.data,
        status: response.status,
      };
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.api.put<T>(url, data, config);
      return {
        data: response.data,
        status: response.status,
      };
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  async patch<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.api.patch<T>(url, data, config);
      return {
        data: response.data,
        status: response.status,
      };
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.api.delete<T>(url, config);
      return {
        data: response.data,
        status: response.status,
      };
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  // Gestion des erreurs
  private handleError(error: any): ApiError {
    if (error.response) {
      return {
        message: error.response.data?.message || 'Une erreur est survenue',
        status: error.response.status,
        errors: error.response.data?.errors,
      };
    } else if (error.request) {
      return {
        message: 'Impossible de se connecter au serveur',
        status: 0,
      };
    } else {
      return {
        message: error.message || 'Une erreur inattendue est survenue',
        status: 0,
      };
    }
  }
}

// Export de l'instance unique
export const apiService = ApiService.getInstance();

// Export de l'instance axios directe pour les cas spéciaux
export { api }; 