import { apiService, ApiResponse, ApiError } from './api';
import { MemberType, MemberStatistiquesType, MembersResponse, PaginationMeta } from '../types';

// Interface pour la création d'un membre
export interface CreateMemberData {
  nom: string;
  prenom: string;
  adresse: string;
  email: string;
  telephone: string;
  groupe_id: number;
  genre: string;
  tag_ids: number[];
  departement_id: number;
  nationalite?: string;
  profession?: string;
  date_naissance?: string;
  conjoint_id?: number;
  situation_matrimoniale: string;
}

// Interface pour la mise à jour d'un membre
export interface UpdateMemberData extends Partial<CreateMemberData> {
  id: number;
}

// Interface pour les filtres de recherche
export interface MemberFilters {
  search?: string;
  departement_id?: number;
  groupe_id?: number;
  tag_ids?: number[];
  etape_id?: number;
  genre?: string;
  situation_matrimoniale?: string;
  status?: string;
  page?: number;
  page_size?: number;
}

// Service pour les membres
export class MemberService {
  private static instance: MemberService;

  private constructor() {}

  public static getInstance(): MemberService {
    if (!MemberService.instance) {
      MemberService.instance = new MemberService();
    }
    return MemberService.instance;
  }

  // Récupérer la liste des membres
  async getMembers(filters?: MemberFilters): Promise<{ data: MemberType[]; pagination: PaginationMeta }> {
    try {
      const params = new URLSearchParams();
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            if (Array.isArray(value)) {
              value.forEach(v => params.append(key, v.toString()));
            } else {
              params.append(key, value.toString());
            }
          }
        });
      }

      const url = `/api/membres/${filters ? `?${params.toString()}` : ''}`;
      const response = await apiService.get<MembersResponse>(url);
      
      // Extraire les données de pagination
      const pagination: PaginationMeta = {
        currentPage: filters?.page || 1,
        totalPages: Math.ceil(response.data.count / (filters?.page_size || 10)),
        totalItems: response.data.count,
        itemsPerPage: filters?.page_size || 10,
        hasNext: !!response.data.next,
        hasPrevious: !!response.data.previous,
      };

      return {
        data: response.data.results,
        pagination
      };
    } catch (error) {
      throw error;
    }
  }

  // Récupérer un membre par ID
  async getMember(id: number): Promise<ApiResponse<MemberType>> {
    try {
      return await apiService.get<MemberType>(`/api/membres/${id}/`);
    } catch (error) {
      throw error;
    }
  }

  // Créer un nouveau membre
  async createMember(memberData: CreateMemberData): Promise<ApiResponse<MemberType>> {
    try {
      return await apiService.post<MemberType>('/api/membres/', memberData);
    } catch (error) {
      throw error;
    }
  }

  // Mettre à jour un membre
  async updateMember(memberData: UpdateMemberData): Promise<ApiResponse<MemberType>> {
    try {
      const { id, ...data } = memberData;
      return await apiService.put<MemberType>(`/api/membres/${id}/`, data);
    } catch (error) {
      throw error;
    }
  }

  // Supprimer un membre
  async deleteMember(id: number): Promise<ApiResponse<void>> {
    try {
      return await apiService.delete<void>(`/api/membres/${id}/`);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les statistiques des membres
  async getMemberStatistics(): Promise<ApiResponse<MemberStatistiquesType>> {
    try {
      return await apiService.get<MemberStatistiquesType>('/api/membres/statistics/');
    } catch (error) {
      throw error;
    }
  }

  // Rechercher des membres
  async searchMembers(query: string): Promise<ApiResponse<MemberType[]>> {
    try {
      return await apiService.get<MemberType[]>(`/api/membres/search/?q=${encodeURIComponent(query)}`);
    } catch (error) {
      throw error;
    }
  }

  // Exporter les membres
  async exportMembers(filters?: MemberFilters, format: 'csv' | 'excel' = 'csv'): Promise<ApiResponse<Blob>> {
    try {
      const params = new URLSearchParams();
      params.append('format', format);
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            if (Array.isArray(value)) {
              value.forEach(v => params.append(key, v.toString()));
            } else {
              params.append(key, value.toString());
            }
          }
        });
      }

      const response = await apiService.get<Blob>(`/api/membres/export/?${params.toString()}`, {
        responseType: 'blob'
      });
      
      return response;
    } catch (error) {
      throw error;
    }
  }

  // Importer des membres
  async importMembers(file: File): Promise<ApiResponse<{ imported: number; errors: string[] }>> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      return await apiService.post<{ imported: number; errors: string[] }>('/api/membres/import/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    } catch (error) {
      throw error;
    }
  }

  // Ajouter des tags à un membre
  async addTagsToMember(memberId: number, tagIds: number[]): Promise<ApiResponse<MemberType>> {
    try {
      return await apiService.post<MemberType>(`/api/membres/${memberId}/tags/`, { tag_ids: tagIds });
    } catch (error) {
      throw error;
    }
  }

  // Supprimer des tags d'un membre
  async removeTagsFromMember(memberId: number, tagIds: number[]): Promise<ApiResponse<MemberType>> {
    try {
      return await apiService.delete<MemberType>(`/api/membres/${memberId}/tags/`, {
        data: { tag_ids: tagIds }
      });
    } catch (error) {
      throw error;
    }
  }

  // Changer le département d'un membre
  async changeMemberDepartment(memberId: number, departementId: number): Promise<ApiResponse<MemberType>> {
    try {
      return await apiService.patch<MemberType>(`/api/membres/${memberId}/department/`, {
        departement_id: departementId
      });
    } catch (error) {
      throw error;
    }
  }

  // Changer le groupe d'un membre
  async changeMemberGroup(memberId: number, groupeId: number): Promise<ApiResponse<MemberType>> {
    try {
      return await apiService.patch<MemberType>(`/api/membres/${memberId}/group/`, {
        groupe_id: groupeId
      });
    } catch (error) {
      throw error;
    }
  }

  // === NOUVELLES MÉTHODES POUR LES ENDPOINTS DE FILTRAGE ===

  // Récupérer les membres par groupes
  async getMembersByGroups(groupIds: number[]): Promise<{ data: MemberType[]; pagination: PaginationMeta }> {
    try {
      const params = new URLSearchParams();
      groupIds.forEach(id => params.append('groupes[]', id.toString()));
      
      const response = await apiService.get<MembersResponse>(`/api/membres/par_groupes/?${params.toString()}`);
      
      const pagination: PaginationMeta = {
        currentPage: 1,
        totalPages: 1,
        totalItems: response.data.count,
        itemsPerPage: response.data.count,
        hasNext: false,
        hasPrevious: false,
      };

      return {
        data: response.data.results,
        pagination
      };
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les membres par étapes
  async getMembersByEtapes(etapeIds: number[]): Promise<{ data: MemberType[]; pagination: PaginationMeta }> {
    try {
      const params = new URLSearchParams();
      etapeIds.forEach(id => params.append('etapes[]', id.toString()));
      
      const response = await apiService.get<MembersResponse>(`/api/membres/par_etapes/?${params.toString()}`);
      
      const pagination: PaginationMeta = {
        currentPage: 1,
        totalPages: 1,
        totalItems: response.data.count,
        itemsPerPage: response.data.count,
        hasNext: false,
        hasPrevious: false,
      };

      return {
        data: response.data.results,
        pagination
      };
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les membres par tags
  async getMembersByTags(tagIds: number[]): Promise<{ data: MemberType[]; pagination: PaginationMeta }> {
    try {
      const params = new URLSearchParams();
      tagIds.forEach(id => params.append('tags[]', id.toString()));
      
      const response = await apiService.get<MembersResponse>(`/api/membres/par_tags/?${params.toString()}`);
      
      const pagination: PaginationMeta = {
        currentPage: 1,
        totalPages: 1,
        totalItems: response.data.count,
        itemsPerPage: response.data.count,
        hasNext: false,
        hasPrevious: false,
      };

      return {
        data: response.data.results,
        pagination
      };
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les membres avec filtres combinés
  async getMembersWithCombinedFilters(filters: {
    groupes?: number[];
    etapes?: number[];
    tags?: number[];
    search?: string;
    page?: number;
    page_size?: number;
  }): Promise<{ data: MemberType[]; pagination: PaginationMeta }> {
    try {
      const params = new URLSearchParams();
      
      if (filters.groupes) {
        filters.groupes.forEach(id => params.append('groupes[]', id.toString()));
      }
      if (filters.etapes) {
        filters.etapes.forEach(id => params.append('etapes[]', id.toString()));
      }
      if (filters.tags) {
        filters.tags.forEach(id => params.append('tags[]', id.toString()));
      }
      if (filters.search) {
        params.append('search', filters.search);
      }
      if (filters.page) {
        params.append('page', filters.page.toString());
      }
      if (filters.page_size) {
        params.append('page_size', filters.page_size.toString());
      }
      
      const response = await apiService.get<MembersResponse>(`/api/membres/filtres_combines/?${params.toString()}`);
      
      const pagination: PaginationMeta = {
        currentPage: filters.page || 1,
        totalPages: Math.ceil(response.data.count / (filters.page_size || 10)),
        totalItems: response.data.count,
        itemsPerPage: filters.page_size || 10,
        hasNext: !!response.data.next,
        hasPrevious: !!response.data.previous,
      };

      return {
        data: response.data.results,
        pagination
      };
    } catch (error) {
      throw error;
    }
  }

  // Récupérer tous les membres (sans pagination)
  async getAllMembers(): Promise<ApiResponse<MemberType[]>> {
    try {
      return await apiService.get<MemberType[]>('/api/membres/tous_les_membres/');
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les membres simples (version allégée)
  async getSimpleMembers(): Promise<ApiResponse<MemberType[]>> {
    try {
      return await apiService.get<MemberType[]>('/api/membres/membres_simples/');
    } catch (error) {
      throw error;
    }
  }

  // Récupérer un membre avec toutes ses relations
  async getMemberWithRelations(memberId: number): Promise<ApiResponse<MemberType>> {
    try {
      return await apiService.get<MemberType>(`/api/membres/${memberId}/membre_avec_relations/`);
    } catch (error) {
      throw error;
    }
  }
}

// Export de l'instance unique
export const memberService = MemberService.getInstance(); 