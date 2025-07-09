import { apiService, ApiResponse } from './api';
import { DepartementType } from '../types';

// Interface pour la création d'un département
export interface CreateDepartmentData {
  nom: string;
  mission: string;
  color: string;
  responsable_id?: number;
  description?: string;
}

// Interface pour la mise à jour d'un département
export interface UpdateDepartmentData extends Partial<CreateDepartmentData> {
  id: string;
}

// Interface pour les filtres de départements
export interface DepartmentFilters {
  search?: string;
  responsable_id?: number;
  page?: number;
  page_size?: number;
}

// Service pour les départements
export class DepartmentService {
  private static instance: DepartmentService;

  private constructor() {}

  public static getInstance(): DepartmentService {
    if (!DepartmentService.instance) {
      DepartmentService.instance = new DepartmentService();
    }
    return DepartmentService.instance;
  }

  // Récupérer la liste des départements
  async getDepartments(filters?: DepartmentFilters): Promise<ApiResponse<DepartementType[]>> {
    try {
      const params = new URLSearchParams();
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            params.append(key, value.toString());
          }
        });
      }

      const url = `/api/departments/${filters ? `?${params.toString()}` : ''}`;
      return await apiService.get<DepartementType[]>(url);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer un département par ID
  async getDepartment(id: string): Promise<ApiResponse<DepartementType>> {
    try {
      return await apiService.get<DepartementType>(`/api/departments/${id}/`);
    } catch (error) {
      throw error;
    }
  }

  // Créer un nouveau département
  async createDepartment(departmentData: CreateDepartmentData): Promise<ApiResponse<DepartementType>> {
    try {
      return await apiService.post<DepartementType>('/api/departments/', departmentData);
    } catch (error) {
      throw error;
    }
  }

  // Mettre à jour un département
  async updateDepartment(departmentData: UpdateDepartmentData): Promise<ApiResponse<DepartementType>> {
    try {
      const { id, ...data } = departmentData;
      return await apiService.put<DepartementType>(`/api/departments/${id}/`, data);
    } catch (error) {
      throw error;
    }
  }

  // Supprimer un département
  async deleteDepartment(id: string): Promise<ApiResponse<void>> {
    try {
      return await apiService.delete<void>(`/api/departments/${id}/`);
    } catch (error) {
      throw error;
    }
  }

  // Rechercher des départements
  async searchDepartments(query: string): Promise<ApiResponse<DepartementType[]>> {
    try {
      return await apiService.get<DepartementType[]>(`/api/departments/search/?q=${encodeURIComponent(query)}`);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les statistiques d'un département
  async getDepartmentStatistics(departmentId: string): Promise<ApiResponse<{
    total_members: number;
    active_members: number;
    inactive_members: number;
    new_members_this_month: number;
    gender_distribution: {
      Masculin: number;
      Féminin: number;
    };
    age_distribution: {
      moins_18: number;
      "18_25": number;
      "26_35": number;
      "36_50": number;
      plus_50: number;
    };
  }>> {
    try {
      return await apiService.get(`/api/departments/${departmentId}/statistics/`);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les membres d'un département
  async getDepartmentMembers(departmentId: string, filters?: {
    search?: string;
    status?: string;
    page?: number;
    page_size?: number;
  }): Promise<ApiResponse<any[]>> {
    try {
      const params = new URLSearchParams();
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            params.append(key, value.toString());
          }
        });
      }

      const url = `/api/departments/${departmentId}/members/${filters ? `?${params.toString()}` : ''}`;
      return await apiService.get<any[]>(url);
    } catch (error) {
      throw error;
    }
  }

  // Assigner un responsable au département
  async assignResponsible(departmentId: string, memberId: number): Promise<ApiResponse<DepartementType>> {
    try {
      return await apiService.patch<DepartementType>(`/api/departments/${departmentId}/assign-responsible/`, {
        responsable_id: memberId
      });
    } catch (error) {
      throw error;
    }
  }

  // Retirer le responsable du département
  async removeResponsible(departmentId: string): Promise<ApiResponse<DepartementType>> {
    try {
      return await apiService.patch<DepartementType>(`/api/departments/${departmentId}/remove-responsible/`);
    } catch (error) {
      throw error;
    }
  }

  // Exporter les départements
  async exportDepartments(filters?: DepartmentFilters, format: 'csv' | 'excel' = 'csv'): Promise<ApiResponse<Blob>> {
    try {
      const params = new URLSearchParams();
      params.append('format', format);
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            params.append(key, value.toString());
          }
        });
      }

      const response = await apiService.get<Blob>(`/api/departments/export/?${params.toString()}`, {
        responseType: 'blob'
      });
      
      return response;
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les couleurs disponibles
  async getAvailableColors(): Promise<ApiResponse<string[]>> {
    try {
      return await apiService.get<string[]>('/api/departments/colors/');
    } catch (error) {
      throw error;
    }
  }

  // Vérifier si un nom de département existe
  async checkDepartmentNameExists(name: string, excludeId?: string): Promise<ApiResponse<{ exists: boolean }>> {
    try {
      const data: any = { name };
      if (excludeId) {
        data.exclude_id = excludeId;
      }
      return await apiService.post<{ exists: boolean }>('/api/departments/check-name/', data);
    } catch (error) {
      throw error;
    }
  }
}

// Export de l'instance unique
export const departmentService = DepartmentService.getInstance(); 