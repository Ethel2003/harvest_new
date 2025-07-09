import { apiService, ApiResponse } from './api';
import { EtapeType } from '../types';

// Interface pour la création d'une étape
export interface CreateEtapeData {
  libelle: string;
  description: string;
  ordre?: number;
  couleur?: string;
  duree_estimee?: number; // en jours
  conditions?: string;
}

// Interface pour la mise à jour d'une étape
export interface UpdateEtapeData extends Partial<CreateEtapeData> {
  id: string;
}

// Interface pour les filtres d'étapes
export interface EtapeFilters {
  search?: string;
  ordre?: number;
  page?: number;
  page_size?: number;
}

// Service pour les étapes
export class EtapeService {
  private static instance: EtapeService;

  private constructor() {}

  public static getInstance(): EtapeService {
    if (!EtapeService.instance) {
      EtapeService.instance = new EtapeService();
    }
    return EtapeService.instance;
  }

  // Récupérer la liste des étapes
  async getEtapes(filters?: EtapeFilters): Promise<ApiResponse<EtapeType[]>> {
    try {
      const params = new URLSearchParams();
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            params.append(key, value.toString());
          }
        });
      }

      const url = `/api/etapes/${filters ? `?${params.toString()}` : ''}`;
      return await apiService.get<EtapeType[]>(url);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer toutes les étapes (alias pour getEtapes)
  async getAllEtapes(): Promise<ApiResponse<EtapeType[]>> {
    return this.getEtapes();
  }

  // Récupérer une étape par ID
  async getEtape(id: string): Promise<ApiResponse<EtapeType>> {
    try {
      return await apiService.get<EtapeType>(`/api/etapes/${id}/`);
    } catch (error) {
      throw error;
    }
  }

  // Créer une nouvelle étape
  async createEtape(etapeData: CreateEtapeData): Promise<ApiResponse<EtapeType>> {
    try {
      return await apiService.post<EtapeType>('/api/etapes/', etapeData);
    } catch (error) {
      throw error;
    }
  }

  // Mettre à jour une étape
  async updateEtape(etapeData: UpdateEtapeData): Promise<ApiResponse<EtapeType>> {
    try {
      const { id, ...data } = etapeData;
      return await apiService.put<EtapeType>(`/api/etapes/${id}/`, data);
    } catch (error) {
      throw error;
    }
  }

  // Supprimer une étape
  async deleteEtape(id: string): Promise<ApiResponse<void>> {
    try {
      return await apiService.delete<void>(`/api/etapes/${id}/`);
    } catch (error) {
      throw error;
    }
  }

  // Rechercher des étapes
  async searchEtapes(query: string): Promise<ApiResponse<EtapeType[]>> {
    try {
      return await apiService.get<EtapeType[]>(`/api/etapes/search/?q=${encodeURIComponent(query)}`);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les étapes ordonnées
  async getEtapesOrdered(): Promise<ApiResponse<EtapeType[]>> {
    try {
      return await apiService.get<EtapeType[]>('/api/etapes/ordered/');
    } catch (error) {
      throw error;
    }
  }

  // Réorganiser les étapes
  async reorderEtapes(etapeIds: string[]): Promise<ApiResponse<{ message: string }>> {
    try {
      return await apiService.post<{ message: string }>('/api/etapes/reorder/', {
        etape_ids: etapeIds
      });
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les statistiques d'une étape
  async getEtapeStatistics(etapeId: string): Promise<ApiResponse<{
    total_membres: number;
    membres_actuels: number;
    membres_completes: number;
    duree_moyenne: number;
    progression: number;
  }>> {
    try {
      return await apiService.get(`/api/etapes/${etapeId}/statistics/`);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les membres d'une étape
  async getEtapeMembers(etapeId: string, filters?: {
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

      const url = `/api/etapes/${etapeId}/members/${filters ? `?${params.toString()}` : ''}`;
      return await apiService.get<any[]>(url);
    } catch (error) {
      throw error;
    }
  }

  // Assigner un membre à une étape
  async assignMemberToEtape(etapeId: string, memberId: number): Promise<ApiResponse<{ message: string }>> {
    try {
      return await apiService.post<{ message: string }>(`/api/etapes/${etapeId}/assign-member/`, {
        member_id: memberId
      });
    } catch (error) {
      throw error;
    }
  }

  // Retirer un membre d'une étape
  async removeMemberFromEtape(etapeId: string, memberId: number): Promise<ApiResponse<{ message: string }>> {
    try {
      return await apiService.delete<{ message: string }>(`/api/etapes/${etapeId}/remove-member/`, {
        data: { member_id: memberId }
      });
    } catch (error) {
      throw error;
    }
  }

  // Marquer une étape comme terminée pour un membre
  async completeEtapeForMember(etapeId: string, memberId: number, notes?: string): Promise<ApiResponse<{ message: string }>> {
    try {
      const data: any = { member_id: memberId };
      if (notes) {
        data.notes = notes;
      }
      return await apiService.post<{ message: string }>(`/api/etapes/${etapeId}/complete/`, data);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les couleurs disponibles
  async getAvailableColors(): Promise<ApiResponse<string[]>> {
    try {
      return await apiService.get<string[]>('/api/etapes/colors/');
    } catch (error) {
      throw error;
    }
  }

  // Vérifier si un libellé d'étape existe
  async checkEtapeLibelleExists(libelle: string, excludeId?: string): Promise<ApiResponse<{ exists: boolean }>> {
    try {
      const data: any = { libelle };
      if (excludeId) {
        data.exclude_id = excludeId;
      }
      return await apiService.post<{ exists: boolean }>('/api/etapes/check-libelle/', data);
    } catch (error) {
      throw error;
    }
  }

  // Exporter les étapes
  async exportEtapes(filters?: EtapeFilters, format: 'csv' | 'excel' = 'csv'): Promise<ApiResponse<Blob>> {
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

      const response = await apiService.get<Blob>(`/api/etapes/export/?${params.toString()}`, {
        responseType: 'blob'
      });
      
      return response;
    } catch (error) {
      throw error;
    }
  }

  // Dupliquer une étape
  async duplicateEtape(etapeId: string, newLibelle?: string): Promise<ApiResponse<EtapeType>> {
    try {
      const data = newLibelle ? { new_libelle: newLibelle } : {};
      return await apiService.post<EtapeType>(`/api/etapes/${etapeId}/duplicate/`, data);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les étapes actives
  async getActiveEtapes(): Promise<ApiResponse<EtapeType[]>> {
    try {
      return await apiService.get<EtapeType[]>('/api/etapes/active/');
    } catch (error) {
      throw error;
    }
  }

  // Activer/Désactiver une étape
  async toggleEtapeStatus(etapeId: string, active: boolean): Promise<ApiResponse<EtapeType>> {
    try {
      return await apiService.patch<EtapeType>(`/api/etapes/${etapeId}/toggle-status/`, {
        active
      });
    } catch (error) {
      throw error;
    }
  }
}

// Export de l'instance unique
export const etapeService = EtapeService.getInstance(); 