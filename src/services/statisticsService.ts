import { apiService, ApiResponse } from './api';
import { UserStatistiquesJSON, MemberStatistiquesType, DashboardStats, GroupeType, DepartementType } from '../types';

// Interface pour les filtres de statistiques
export interface StatisticsFilters {
  date_from?: string;
  date_to?: string;
  departement_id?: number;
  groupe_id?: number;
  tag_id?: number;
}

// Interface pour les statistiques de croissance
export interface GrowthStatistics {
  period: string;
  members_growth: number;
  events_growth: number;
  appointments_growth: number;
  revenue_growth?: number;
}

// Service pour les statistiques
export class StatisticsService {
  private static instance: StatisticsService;

  private constructor() {}

  public static getInstance(): StatisticsService {
    if (!StatisticsService.instance) {
      StatisticsService.instance = new StatisticsService();
    }
    return StatisticsService.instance;
  }

  // Récupérer les statistiques du tableau de bord
  async getDashboardStats(): Promise<ApiResponse<DashboardStats>> {
    try {
      return await apiService.get<DashboardStats>('/api/statistics/dashboard');
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les statistiques des utilisateurs
  async getUserStatistics(filters?: StatisticsFilters): Promise<ApiResponse<UserStatistiquesJSON>> {
    try {
      const params = new URLSearchParams();
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            params.append(key, value.toString());
          }
        });
      }

      const url = `/api/statistics/users/${filters ? `?${params.toString()}` : ''}`;
      return await apiService.get<UserStatistiquesJSON>(url);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les statistiques des membres
  async getMemberStatistics(filters?: StatisticsFilters): Promise<ApiResponse<MemberStatistiquesType>> {
    try {
      const params = new URLSearchParams();
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            params.append(key, value.toString());
          }
        });
      }

      const url = `/api/statistics/members/${filters ? `?${params.toString()}` : ''}`;
      return await apiService.get<MemberStatistiquesType>(url);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les statistiques des groupes
  async getGroupStatistics(): Promise<ApiResponse<GroupeType>> {
    try {
      const url = `/api/groupes/statistiques/`;
      return await apiService.get<GroupeType>(url);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les statistiques des départements
  async getDepartmentStatistics(): Promise<ApiResponse<DepartementType>> {
    try {
      const url = `/api/departements/statistiques/`;
      return await apiService.get<DepartementType>(url);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer l'évolution des membres par date de création
  async getMemberEvolution(filters?: {
    start_date?: string;
    end_date?: string;
    period?: 'daily' | 'monthly';
  }): Promise<ApiResponse<Array<{ date: string; value: number }>>> {
    try {
      const params = new URLSearchParams();
      
      // Ajouter tous les paramètres fournis, même s'ils sont vides
      if (filters) {
        // Ajouter le format s'il est fourni
        if (filters.period) {
          params.append('period', filters.period);
        }
        
        // Ajouter les dates seulement si elles sont fournies et non vides
        if (filters.start_date && filters.start_date.trim() !== '') {
          params.append('start_date', filters.start_date);
        }
        
        if (filters.end_date && filters.end_date.trim() !== '') {
          params.append('end_date', filters.end_date);
        }
      }

      // Construire l'URL avec les paramètres
      const queryString = params.toString();
      const url = `/api/membres/evolution-membres/${queryString ? `?${queryString}` : ''}`;
      
      console.log("URL de la requête:", url);
      return await apiService.get<Array<{ date: string; value: number }>>(url);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les statistiques des événements
  async getEventStatistics(filters?: StatisticsFilters): Promise<ApiResponse<{
    total_events: number;
    upcoming_events: number;
    past_events: number;
    cancelled_events: number;
    total_attendees: number;
    average_attendance: number;
    events_by_type: {
      meeting: number;
      workshop: number;
      conference: number;
      social: number;
    };
    events_by_month: {
      [key: string]: number;
    };
  }>> {
    try {
      const params = new URLSearchParams();
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            params.append(key, value.toString());
          }
        });
      }

      const url = `/api/statistics/events/${filters ? `?${params.toString()}` : ''}`;
      return await apiService.get(url);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les statistiques des rendez-vous
  async getAppointmentStatistics(filters?: StatisticsFilters): Promise<ApiResponse<{
    total_appointments: number;
    scheduled_appointments: number;
    confirmed_appointments: number;
    cancelled_appointments: number;
    completed_appointments: number;
    today_appointments: number;
    this_week_appointments: number;
    this_month_appointments: number;
    average_duration: number;
    appointments_by_status: {
      [key: string]: number;
    };
    appointments_by_month: {
      [key: string]: number;
    };
  }>> {
    try {
      const params = new URLSearchParams();
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            params.append(key, value.toString());
          }
        });
      }

      const url = `/api/statistics/appointments/${filters ? `?${params.toString()}` : ''}`;
      return await apiService.get(url);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les statistiques de croissance
  async getGrowthStatistics(period: 'week' | 'month' | 'quarter' | 'year' = 'month'): Promise<ApiResponse<GrowthStatistics[]>> {
    try {
      return await apiService.get<GrowthStatistics[]>(`/api/statistics/growth/?period=${period}`);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les statistiques géographiques
  async getGeographicStatistics(): Promise<ApiResponse<{
    countries: Array<{
      country: string;
      count: number;
    }>;
    cities: Array<{
      city: string;
      count: number;
    }>;
    regions: Array<{
      region: string;
      count: number;
    }>;
  }>> {
    try {
      return await apiService.get('/api/statistics/geographic/');
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les statistiques d'activité
  async getActivityStatistics(days: number = 30): Promise<ApiResponse<{
    daily_activity: Array<{
      date: string;
      new_members: number;
      new_events: number;
      new_appointments: number;
    }>;
    peak_hours: Array<{
      hour: number;
      activity_count: number;
    }>;
    peak_days: Array<{
      day: string;
      activity_count: number;
    }>;
  }>> {
    try {
      return await apiService.get(`/api/statistics/activity/?days=${days}`);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les statistiques de performance
  async getPerformanceStatistics(): Promise<ApiResponse<{
    response_time: {
      average: number;
      min: number;
      max: number;
    };
    error_rate: {
      total_errors: number;
      error_percentage: number;
      errors_by_type: {
        [key: string]: number;
      };
    };
    user_satisfaction: {
      average_rating: number;
      total_ratings: number;
      ratings_distribution: {
        [key: string]: number;
      };
    };
  }>> {
    try {
      return await apiService.get('/api/statistics/performance/');
    } catch (error) {
      throw error;
    }
  }

  // Générer un rapport personnalisé
  async generateCustomReport(reportConfig: {
    type: 'members' | 'events' | 'appointments' | 'users';
    filters?: StatisticsFilters;
    group_by?: string;
    sort_by?: string;
    limit?: number;
  }): Promise<ApiResponse<any>> {
    try {
      return await apiService.post('/api/statistics/custom-report/', reportConfig);
    } catch (error) {
      throw error;
    }
  }

  // Exporter les statistiques
  async exportStatistics(
    type: 'members' | 'events' | 'appointments' | 'users' | 'dashboard',
    filters?: StatisticsFilters,
    format: 'csv' | 'excel' | 'pdf' = 'csv'
  ): Promise<ApiResponse<Blob>> {
    try {
      const params = new URLSearchParams();
      params.append('type', type);
      params.append('format', format);
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            params.append(key, value.toString());
          }
        });
      }

      const response = await apiService.get<Blob>(`/api/statistics/export/?${params.toString()}`, {
        responseType: 'blob'
      });
      
      return response;
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les alertes et notifications
  async getAlerts(): Promise<ApiResponse<Array<{
    id: string;
    type: 'warning' | 'error' | 'info' | 'success';
    title: string;
    message: string;
    created_at: string;
    read: boolean;
  }>>> {
    try {
      return await apiService.get('/api/statistics/alerts/');
    } catch (error) {
      throw error;
    }
  }

  // Marquer une alerte comme lue
  async markAlertAsRead(alertId: string): Promise<ApiResponse<{ message: string }>> {
    try {
      return await apiService.patch<{ message: string }>(`/api/statistics/alerts/${alertId}/read/`);
    } catch (error) {
      throw error;
    }
  }

  // Marquer toutes les alertes comme lues
  async markAllAlertsAsRead(): Promise<ApiResponse<{ message: string }>> {
    try {
      return await apiService.patch<{ message: string }>('/api/statistics/alerts/mark-all-read/');
    } catch (error) {
      throw error;
    }
  }
}

// Export de l'instance unique
export const statisticsService = StatisticsService.getInstance(); 