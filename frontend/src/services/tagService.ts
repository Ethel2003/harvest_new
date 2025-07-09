import { apiService, ApiResponse } from './api';
import { TagType } from '../types';

// Interface pour la création d'un tag
export interface CreateTagData {
  nom: string;
  description?: string;
  color?: string;
  category?: string;
}

// Interface pour la mise à jour d'un tag
export interface UpdateTagData extends Partial<CreateTagData> {
  id: string;
}

// Interface pour les filtres de tags
export interface TagFilters {
  search?: string;
  category?: string;
  page?: number;
  page_size?: number;
}

// Service pour les tags
export class TagService {
  private static instance: TagService;

  private constructor() {}

  public static getInstance(): TagService {
    if (!TagService.instance) {
      TagService.instance = new TagService();
    }
    return TagService.instance;
  }

  // Récupérer la liste des tags
  async getTags(filters?: TagFilters): Promise<ApiResponse<TagType[]>> {
    try {
      const params = new URLSearchParams();
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            params.append(key, value.toString());
          }
        });
      }

      const url = `/api/tags/tous_les_tags/${filters ? `?${params.toString()}` : ''}`;
      return await apiService.get<TagType[]>(url);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer tous les tags (alias pour getTags)
  async getAllTags(): Promise<ApiResponse<TagType[]>> {
    return this.getTags();
  }

  // Récupérer un tag par ID
  async getTag(id: string): Promise<ApiResponse<TagType>> {
    try {
      return await apiService.get<TagType>(`/api/tags/${id}/`);
    } catch (error) {
      throw error;
    }
  }

  // Créer un nouveau tag
  async createTag(tagData: CreateTagData): Promise<ApiResponse<TagType>> {
    try {
      return await apiService.post<TagType>('/api/tags/', tagData);
    } catch (error) {
      throw error;
    }
  }

  // Mettre à jour un tag
  async updateTag(tagData: UpdateTagData): Promise<ApiResponse<TagType>> {
    try {
      const { id, ...data } = tagData;
      return await apiService.put<TagType>(`/api/tags/${id}/`, data);
    } catch (error) {
      throw error;
    }
  }

  // Supprimer un tag
  async deleteTag(id: string): Promise<ApiResponse<void>> {
    try {
      return await apiService.delete<void>(`/api/tags/${id}/`);
    } catch (error) {
      throw error;
    }
  }

  // Rechercher des tags
  async searchTags(query: string): Promise<ApiResponse<TagType[]>> {
    try {
      return await apiService.get<TagType[]>(`/api/tags/search/?q=${encodeURIComponent(query)}`);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les statistiques d'un tag
  async getTagStatistics(tagId: string): Promise<ApiResponse<{
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
      return await apiService.get(`/api/tags/${tagId}/statistics/`);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les membres d'un tag
  async getTagMembers(tagId: string, filters?: {
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

      const url = `/api/tags/${tagId}/members/${filters ? `?${params.toString()}` : ''}`;
      return await apiService.get<any[]>(url);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les catégories de tags
  async getTagCategories(): Promise<ApiResponse<string[]>> {
    try {
      return await apiService.get<string[]>('/api/tags/categories/');
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les tags par catégorie
  async getTagsByCategory(category: string): Promise<ApiResponse<TagType[]>> {
    try {
      return await apiService.get<TagType[]>(`/api/tags/category/${encodeURIComponent(category)}/`);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les tags populaires
  async getPopularTags(limit?: number): Promise<ApiResponse<Array<TagType & { member_count: number }>>> {
    try {
      const url = limit ? `/api/tags/popular/?limit=${limit}` : '/api/tags/popular/';
      return await apiService.get<Array<TagType & { member_count: number }>>(url);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les tags récents
  async getRecentTags(limit?: number): Promise<ApiResponse<TagType[]>> {
    try {
      const url = limit ? `/api/tags/recent/?limit=${limit}` : '/api/tags/recent/';
      return await apiService.get<TagType[]>(url);
    } catch (error) {
      throw error;
    }
  }

  // Fusionner des tags
  async mergeTags(sourceTagId: string, targetTagId: string): Promise<ApiResponse<{ message: string; merged_count: number }>> {
    try {
      return await apiService.post<{ message: string; merged_count: number }>('/api/tags/merge/', {
        source_tag_id: sourceTagId,
        target_tag_id: targetTagId
      });
    } catch (error) {
      throw error;
    }
  }

  // Exporter les tags
  async exportTags(filters?: TagFilters, format: 'csv' | 'excel' = 'csv'): Promise<ApiResponse<Blob>> {
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

      const response = await apiService.get<Blob>(`/api/tags/export/?${params.toString()}`, {
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
      return await apiService.get<string[]>('/api/tags/colors/');
    } catch (error) {
      throw error;
    }
  }

  // Vérifier si un nom de tag existe
  async checkTagNameExists(name: string, excludeId?: string): Promise<ApiResponse<{ exists: boolean }>> {
    try {
      const data: any = { name };
      if (excludeId) {
        data.exclude_id = excludeId;
      }
      return await apiService.post<{ exists: boolean }>('/api/tags/check-name/', data);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les suggestions de tags
  async getTagSuggestions(query: string, limit?: number): Promise<ApiResponse<TagType[]>> {
    try {
      const url = limit 
        ? `/api/tags/suggestions/?q=${encodeURIComponent(query)}&limit=${limit}`
        : `/api/tags/suggestions/?q=${encodeURIComponent(query)}`;
      return await apiService.get<TagType[]>(url);
    } catch (error) {
      throw error;
    }
  }
}

// Export de l'instance unique
export const tagService = TagService.getInstance(); 