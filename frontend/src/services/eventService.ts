import { apiService, ApiResponse } from './api';
import { Event } from '../types';

// Interface pour la création d'un événement
export interface CreateEventData {
  title: string;
  description: string;
  date: string;
  time: string;
  location: string;
  maxAttendees?: number;
  type: 'meeting' | 'workshop' | 'conference' | 'social';
  organizer_id?: number;
  tags?: string[];
}

// Interface pour la mise à jour d'un événement
export interface UpdateEventData extends Partial<CreateEventData> {
  id: string;
}

// Interface pour les filtres d'événements
export interface EventFilters {
  search?: string;
  type?: string;
  date_from?: string;
  date_to?: string;
  location?: string;
  organizer_id?: number;
  page?: number;
  page_size?: number;
}

// Interface pour l'inscription à un événement
export interface EventRegistration {
  event_id: string;
  member_id: number;
  notes?: string;
}

// Service pour les événements
export class EventService {
  private static instance: EventService;

  private constructor() {}

  public static getInstance(): EventService {
    if (!EventService.instance) {
      EventService.instance = new EventService();
    }
    return EventService.instance;
  }

  // Récupérer la liste des événements
  async getEvents(filters?: EventFilters): Promise<ApiResponse<Event[]>> {
    try {
      const params = new URLSearchParams();
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            params.append(key, value.toString());
          }
        });
      }

      const url = `/api/events/${filters ? `?${params.toString()}` : ''}`;
      return await apiService.get<Event[]>(url);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer un événement par ID
  async getEvent(id: string): Promise<ApiResponse<Event>> {
    try {
      return await apiService.get<Event>(`/api/events/${id}/`);
    } catch (error) {
      throw error;
    }
  }

  // Créer un nouvel événement
  async createEvent(eventData: CreateEventData): Promise<ApiResponse<Event>> {
    try {
      return await apiService.post<Event>('/api/events/', eventData);
    } catch (error) {
      throw error;
    }
  }

  // Mettre à jour un événement
  async updateEvent(eventData: UpdateEventData): Promise<ApiResponse<Event>> {
    try {
      const { id, ...data } = eventData;
      return await apiService.put<Event>(`/api/events/${id}/`, data);
    } catch (error) {
      throw error;
    }
  }

  // Supprimer un événement
  async deleteEvent(id: string): Promise<ApiResponse<void>> {
    try {
      return await apiService.delete<void>(`/api/events/${id}/`);
    } catch (error) {
      throw error;
    }
  }

  // Rechercher des événements
  async searchEvents(query: string): Promise<ApiResponse<Event[]>> {
    try {
      return await apiService.get<Event[]>(`/api/events/search/?q=${encodeURIComponent(query)}`);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les événements à venir
  async getUpcomingEvents(limit?: number): Promise<ApiResponse<Event[]>> {
    try {
      const url = limit ? `/api/events/upcoming/?limit=${limit}` : '/api/events/upcoming/';
      return await apiService.get<Event[]>(url);
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les événements passés
  async getPastEvents(limit?: number): Promise<ApiResponse<Event[]>> {
    try {
      const url = limit ? `/api/events/past/?limit=${limit}` : '/api/events/past/';
      return await apiService.get<Event[]>(url);
    } catch (error) {
      throw error;
    }
  }

  // S'inscrire à un événement
  async registerForEvent(registration: EventRegistration): Promise<ApiResponse<{ message: string }>> {
    try {
      return await apiService.post<{ message: string }>('/api/events/register/', registration);
    } catch (error) {
      throw error;
    }
  }

  // Se désinscrire d'un événement
  async unregisterFromEvent(eventId: string, memberId: number): Promise<ApiResponse<{ message: string }>> {
    try {
      return await apiService.delete<{ message: string }>(`/api/events/${eventId}/unregister/`, {
        data: { member_id: memberId }
      });
    } catch (error) {
      throw error;
    }
  }

  // Récupérer les participants d'un événement
  async getEventAttendees(eventId: string): Promise<ApiResponse<any[]>> {
    try {
      return await apiService.get<any[]>(`/api/events/${eventId}/attendees/`);
    } catch (error) {
      throw error;
    }
  }

  // Exporter les événements
  async exportEvents(filters?: EventFilters, format: 'csv' | 'excel' = 'csv'): Promise<ApiResponse<Blob>> {
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

      const response = await apiService.get<Blob>(`/api/events/export/?${params.toString()}`, {
        responseType: 'blob'
      });
      
      return response;
    } catch (error) {
      throw error;
    }
  }

  // Dupliquer un événement
  async duplicateEvent(eventId: string, newDate?: string): Promise<ApiResponse<Event>> {
    try {
      const data = newDate ? { new_date: newDate } : {};
      return await apiService.post<Event>(`/api/events/${eventId}/duplicate/`, data);
    } catch (error) {
      throw error;
    }
  }

  // Annuler un événement
  async cancelEvent(eventId: string, reason?: string): Promise<ApiResponse<Event>> {
    try {
      const data = reason ? { reason } : {};
      return await apiService.patch<Event>(`/api/events/${eventId}/cancel/`, data);
    } catch (error) {
      throw error;
    }
  }

  // Réactiver un événement annulé
  async reactivateEvent(eventId: string): Promise<ApiResponse<Event>> {
    try {
      return await apiService.patch<Event>(`/api/events/${eventId}/reactivate/`);
    } catch (error) {
      throw error;
    }
  }

  // Envoyer des rappels pour un événement
  async sendEventReminders(eventId: string): Promise<ApiResponse<{ sent: number; failed: number }>> {
    try {
      return await apiService.post<{ sent: number; failed: number }>(`/api/events/${eventId}/reminders/`);
    } catch (error) {
      throw error;
    }
  }
}

// Export de l'instance unique
export const eventService = EventService.getInstance(); 