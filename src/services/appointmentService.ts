import { apiService, ApiResponse } from './api';
import { Appointment } from '../types';

// Interface pour la création d'un rendez-vous
export interface CreateAppointmentData {
  title: string;
  client: string;
  date: string;
  time: string;
  duration: number;
  notes?: string;
  member_id?: number;
  type?: string;
  priority?: 'low' | 'medium' | 'high';
}

// Interface pour la mise à jour d'un rendez-vous
export interface UpdateAppointmentData extends Partial<CreateAppointmentData> {
  id: string;
}

// Interface pour les filtres de rendez-vous
export interface AppointmentFilters {
  search?: string;
  status?: 'scheduled' | 'confirmed' | 'cancelled' | 'completed';
  date_from?: string;
  date_to?: string;
  client?: string;
  member_id?: number;
  priority?: string;
  page?: number;
  page_size?: number;
}

// Interface pour la confirmation d'un rendez-vous
export interface AppointmentConfirmation {
  appointment_id: string;
  confirmed: boolean;
  notes?: string;
}

// Service pour les rendez-vous
export class AppointmentService {
  private static instance: AppointmentService;

  private constructor() {}

  public static getInstance(): AppointmentService {
    if (!AppointmentService.instance) {
      AppointmentService.instance = new AppointmentService();
    }
    return AppointmentService.instance;
  }

  // Récupérer la liste des rendez-vous
  async getAppointments(filters?: AppointmentFilters): Promise<ApiResponse<Appointment[]>> {
    try {
      const params = new URLSearchParams();
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            params.append(key, value.toString());
          }
        });
      }

      const url = `/api/appointments/${filters ? `?${params.toString()}` : ''}`;
      return await apiService.get<Appointment[]>(url);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer un rendez-vous par ID
  async getAppointment(id: string): Promise<ApiResponse<Appointment>> {
    try {
      return await apiService.get<Appointment>(`/api/appointments/${id}/`);
    } catch (error) {
      throw error;
    }
  }

  // Créer un nouveau rendez-vous
  async createAppointment(appointmentData: CreateAppointmentData): Promise<ApiResponse<Appointment>> {
    try {
      return await apiService.post<Appointment>('/api/appointments/', appointmentData);
    } catch (error) {
      throw error;
    }
  }

  // Mettre à jour un rendez-vous
  async updateAppointment(appointmentData: UpdateAppointmentData): Promise<ApiResponse<Appointment>> {
    try {
      const { id, ...data } = appointmentData;
      return await apiService.put<Appointment>(`/api/appointments/${id}/`, data);
    } catch (error) {
      throw error;
    }
  }

  // Supprimer un rendez-vous
  async deleteAppointment(id: string): Promise<ApiResponse<void>> {
    try {
      return await apiService.delete<void>(`/api/appointments/${id}/`);
    } catch (error) {
      throw error;
    }
  }

  // Rechercher des rendez-vous
  async searchAppointments(query: string): Promise<ApiResponse<Appointment[]>> {
    try {
      return await apiService.get<Appointment[]>(`/api/appointments/search/?q=${encodeURIComponent(query)}`);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les rendez-vous du jour
  async getTodayAppointments(): Promise<ApiResponse<Appointment[]>> {
    try {
      return await apiService.get<Appointment[]>('/api/appointments/today/');
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les rendez-vous de la semaine
  async getWeekAppointments(): Promise<ApiResponse<Appointment[]>> {
    try {
      return await apiService.get<Appointment[]>('/api/appointments/week/');
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les rendez-vous du mois
  async getMonthAppointments(): Promise<ApiResponse<Appointment[]>> {
    try {
      return await apiService.get<Appointment[]>('/api/appointments/month/');
    } catch (error) {
      throw error;
    }
  }

  // Confirmer un rendez-vous
  async confirmAppointment(confirmation: AppointmentConfirmation): Promise<ApiResponse<Appointment>> {
    try {
      return await apiService.patch<Appointment>(`/api/appointments/${confirmation.appointment_id}/confirm/`, {
        confirmed: confirmation.confirmed,
        notes: confirmation.notes
      });
    } catch (error) {
      throw error;
    }
  }

  // Annuler un rendez-vous
  async cancelAppointment(appointmentId: string, reason?: string): Promise<ApiResponse<Appointment>> {
    try {
      const data = reason ? { reason } : {};
      return await apiService.patch<Appointment>(`/api/appointments/${appointmentId}/cancel/`, data);
    } catch (error) {
      throw error;
    }
  }

  // Marquer un rendez-vous comme terminé
  async completeAppointment(appointmentId: string, notes?: string): Promise<ApiResponse<Appointment>> {
    try {
      const data = notes ? { notes } : {};
      return await apiService.patch<Appointment>(`/api/appointments/${appointmentId}/complete/`, data);
    } catch (error) {
      throw error;
    }
  }

  // Reprogrammer un rendez-vous
  async rescheduleAppointment(appointmentId: string, newDate: string, newTime: string): Promise<ApiResponse<Appointment>> {
    try {
      return await apiService.patch<Appointment>(`/api/appointments/${appointmentId}/reschedule/`, {
        new_date: newDate,
        new_time: newTime
      });
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les rendez-vous d'un client
  async getClientAppointments(clientId: string): Promise<ApiResponse<Appointment[]>> {
    try {
      return await apiService.get<Appointment[]>(`/api/appointments/client/${clientId}/`);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les rendez-vous d'un membre
  async getMemberAppointments(memberId: number): Promise<ApiResponse<Appointment[]>> {
    try {
      return await apiService.get<Appointment[]>(`/api/appointments/member/${memberId}/`);
    } catch (error) {
      throw error;
    }
  }

  // Exporter les rendez-vous
  async exportAppointments(filters?: AppointmentFilters, format: 'csv' | 'excel' = 'csv'): Promise<ApiResponse<Blob>> {
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

      const response = await apiService.get<Blob>(`/api/appointments/export/?${params.toString()}`, {
        responseType: 'blob'
      });
      
      return response;
    } catch (error) {
      throw error;
    }
  }

  // Envoyer des rappels pour les rendez-vous
  async sendAppointmentReminders(): Promise<ApiResponse<{ sent: number; failed: number }>> {
    try {
      return await apiService.post<{ sent: number; failed: number }>('/api/appointments/reminders/');
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les statistiques des rendez-vous
  async getAppointmentStatistics(): Promise<ApiResponse<{
    total: number;
    scheduled: number;
    confirmed: number;
    cancelled: number;
    completed: number;
    today: number;
    this_week: number;
    this_month: number;
  }>> {
    try {
      return await apiService.get('/api/appointments/statistics/');
    } catch (error) {
      throw error;
    }
  }

  // Vérifier la disponibilité
  async checkAvailability(date: string, time: string, duration: number, excludeId?: string): Promise<ApiResponse<{ available: boolean; conflicts: Appointment[] }>> {
    try {
      const data: any = { date, time, duration };
      if (excludeId) {
        data.exclude_id = excludeId;
      }
      return await apiService.post('/api/appointments/check-availability/', data);
    } catch (error) {
      throw error;
    }
  }
}

// Export de l'instance unique
export const appointmentService = AppointmentService.getInstance(); 