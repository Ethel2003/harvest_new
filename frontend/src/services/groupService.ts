import { apiService, ApiResponse } from './api';
import { GroupeType, GroupeStatistiquesType } from '../types';

// Interface pour la création d'un groupe
export interface CreateGroupData {
  nom: string;
  description: string;
  color: string;
  responsable_id?: number;
  departement_id?: number;
}

// Interface pour la mise à jour d'un groupe
export interface UpdateGroupData extends Partial<CreateGroupData> {
  id: string;
}

// Interface pour les filtres de groupes
export interface GroupFilters {
  search?: string;
  departement_id?: number;
  responsable_id?: number;
  page?: number;
  page_size?: number;
}

// Service pour les groupes
export class GroupService {
  private static instance: GroupService;

  private constructor() {}

  public static getInstance(): GroupService {
    if (!GroupService.instance) {
      GroupService.instance = new GroupService();
    }
    return GroupService.instance;
  }

  // Récupérer la liste des groupes
  async getGroups(): Promise<ApiResponse<GroupeStatistiquesType>> {
    try {
      const url = `/api/groupes/statistiques/`;
      return await apiService.get<GroupeStatistiquesType>(url);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer seulement la liste des groupes (sans statistiques)
  async getGroupsList(): Promise<ApiResponse<GroupeType[]>> {
    try {
      const response = await this.getGroups();
      return {
        ...response,
        data: response.data.groupes
      };
    } catch (error) {
      throw error;
    }
  }

  // Récupérer un groupe par ID
  async getGroup(id: string): Promise<ApiResponse<GroupeType>> {
    try {
      return await apiService.get<GroupeType>(`/api/groups/${id}/`);
    } catch (error) {
      throw error;
    }
  }

  // Créer un nouveau groupe
  async createGroup(groupData: CreateGroupData): Promise<ApiResponse<GroupeType>> {
    try {
      return await apiService.post<GroupeType>('/api/groups/', groupData);
    } catch (error) {
      throw error;
    }
  }

  // Mettre à jour un groupe
  async updateGroup(groupData: UpdateGroupData): Promise<ApiResponse<GroupeType>> {
    try {
      const { id, ...data } = groupData;
      return await apiService.put<GroupeType>(`/api/groups/${id}/`, data);
    } catch (error) {
      throw error;
    }
  }

  // Supprimer un groupe
  async deleteGroup(id: string): Promise<ApiResponse<void>> {
    try {
      return await apiService.delete<void>(`/api/groups/${id}/`);
    } catch (error) {
      throw error;
    }
  }

  // Rechercher des groupes
  async searchGroups(query: string): Promise<ApiResponse<GroupeType[]>> {
    try {
      return await apiService.get<GroupeType[]>(`/api/groups/search/?q=${encodeURIComponent(query)}`);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les statistiques d'un groupe
  async getGroupStatistics(groupId: string): Promise<ApiResponse<{
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
      return await apiService.get(`/api/groups/${groupId}/statistics/`);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les membres d'un groupe
  async getGroupMembers(groupId: string, filters?: {
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

      const url = `/api/groups/${groupId}/members/${filters ? `?${params.toString()}` : ''}`;
      return await apiService.get<any[]>(url);
    } catch (error) {
      throw error;
    }
  }

  // Assigner un responsable au groupe
  async assignResponsible(groupId: string, memberId: number): Promise<ApiResponse<GroupeType>> {
    try {
      return await apiService.patch<GroupeType>(`/api/groups/${groupId}/assign-responsible/`, {
        responsable_id: memberId
      });
    } catch (error) {
      throw error;
    }
  }

  // Retirer le responsable du groupe
  async removeResponsible(groupId: string): Promise<ApiResponse<GroupeType>> {
    try {
      return await apiService.patch<GroupeType>(`/api/groups/${groupId}/remove-responsible/`);
    } catch (error) {
      throw error;
    }
  }

  // Assigner un département au groupe
  async assignDepartment(groupId: string, departementId: number): Promise<ApiResponse<GroupeType>> {
    try {
      return await apiService.patch<GroupeType>(`/api/groups/${groupId}/assign-department/`, {
        departement_id: departementId
      });
    } catch (error) {
      throw error;
    }
  }

  // Retirer le département du groupe
  async removeDepartment(groupId: string): Promise<ApiResponse<GroupeType>> {
    try {
      return await apiService.patch<GroupeType>(`/api/groups/${groupId}/remove-department/`);
    } catch (error) {
      throw error;
    }
  }

  // Ajouter des membres au groupe
  async addMembersToGroup(groupId: string, memberIds: number[]): Promise<ApiResponse<{ added: number; errors: string[] }>> {
    try {
      return await apiService.post<{ added: number; errors: string[] }>(`/api/groups/${groupId}/add-members/`, {
        member_ids: memberIds
      });
    } catch (error) {
      throw error;
    }
  }

  // Retirer des membres du groupe
  async removeMembersFromGroup(groupId: string, memberIds: number[]): Promise<ApiResponse<{ removed: number; errors: string[] }>> {
    try {
      return await apiService.delete<{ removed: number; errors: string[] }>(`/api/groups/${groupId}/remove-members/`, {
        data: { member_ids: memberIds }
      });
    } catch (error) {
      throw error;
    }
  }

  // Exporter les groupes
  async exportGroups(filters?: GroupFilters, format: 'csv' | 'excel' = 'csv'): Promise<ApiResponse<Blob>> {
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

      const response = await apiService.get<Blob>(`/api/groups/export/?${params.toString()}`, {
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
      return await apiService.get<string[]>('/api/groups/colors/');
    } catch (error) {
      throw error;
    }
  }

  // Vérifier si un nom de groupe existe
  async checkGroupNameExists(name: string, excludeId?: string): Promise<ApiResponse<{ exists: boolean }>> {
    try {
      const data: any = { name };
      if (excludeId) {
        data.exclude_id = excludeId;
      }
      return await apiService.post<{ exists: boolean }>('/api/groups/check-name/', data);
    } catch (error) {
      throw error;
    }
  }
}

// Export de l'instance unique
export const groupService = GroupService.getInstance(); 