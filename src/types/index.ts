export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  role: "admin" | "manager" | "member";
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
  status: "active" | "inactive";
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
  type: "meeting" | "workshop" | "conference" | "social";
}

export interface Appointment {
  id: string;
  title: string;
  client: string;
  date: string;
  time: string;
  duration: number;
  status: "scheduled" | "confirmed" | "cancelled" | "completed";
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
  image?: string;
  initials: string;
  color: string;
  nationalite: string;
  profession: string;
  genre: "homme" | "femme" | "autre";
  dateNaissance: string;
  situationMatrimoniale: "celibataire" | "marie";
  birthDate?: string;
  ville: string;
  adresse: string;
  maritalStatus?: string;
}

export interface Department {
  id: string;
  name: string;
  description?: string;
  createdAt: string;
}
