export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  role: 'admin' | 'manager' | 'member';
}

export interface Member {
  id: string;
  name: string;
  email: string;
  phone?: string;
  department: string;
  group: string;
  stage: string;
  tags: string[];
  joinDate: string;
  status: 'active' | 'inactive';
}

export interface Event {
  id: string;
  title: string;
  description: string;
  date: string;
  time: string;
  location: string;
  attendees: number;
  maxAttendees?: number;
  type: 'meeting' | 'workshop' | 'conference' | 'social';
}

export interface Appointment {
  id: string;
  title: string;
  client: string;
  date: string;
  time: string;
  duration: number;
  status: 'scheduled' | 'confirmed' | 'cancelled' | 'completed';
  notes?: string;
}

export interface DashboardStats {
  departments: number;
  groups: number;
  users: number;
  members: number;
}

export interface MemberType {
  id: string;
  name: string;
  firstName: string;
  email: string;
  phone: string;
  group: string;
  stage: string;
  tags: string[];
  initials: string;
  color: string;
  nationality?: string;
  profession?: string;
  birthDate?: string;
  city?: string;
  address?: string;
  maritalStatus?: string;
}