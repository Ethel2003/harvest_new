// Export des services principaux
export { apiService } from './api';
export { authService } from './authService';

// Export des services métier
export { memberService } from './memberService';
export { eventService } from './eventService';
export { appointmentService } from './appointmentService';
export { departmentService } from './departmentService';
export { groupService } from './groupService';
export { tagService } from './tagService';
export { etapeService } from './etapeService';
export { statisticsService } from './statisticsService';

// Export des types communs
export type { ApiResponse, ApiError } from './api';
export type { LoginCredentials, RegisterData, User, AuthResponse } from './authService';
export type { CreateMemberData, UpdateMemberData, MemberFilters } from './memberService';
export type { CreateEventData, UpdateEventData, EventFilters, EventRegistration } from './eventService';
export type { CreateAppointmentData, UpdateAppointmentData, AppointmentFilters, AppointmentConfirmation } from './appointmentService';
export type { CreateDepartmentData, UpdateDepartmentData, DepartmentFilters } from './departmentService';
export type { CreateGroupData, UpdateGroupData, GroupFilters } from './groupService';
export type { CreateTagData, UpdateTagData, TagFilters } from './tagService';
export type { CreateEtapeData, UpdateEtapeData, EtapeFilters } from './etapeService';
export type { StatisticsFilters, GrowthStatistics } from './statisticsService'; 