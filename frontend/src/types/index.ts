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

export interface GroupeType {
  id: number;
  nom: string;
  description?: string;
  color: string;
  membres_count: number;
  created_at: string;
  updated_at: string;
}

export interface GroupeStatistiquesType {
  groupes: GroupeType[];
  statistiques_globales: {
    total_groupes: number;
    total_membres: number;
    moyenne_membres_par_groupe: number;
    groupe_plus_populaire: GroupeType | null;
  };
}

export interface TagType {
  id: number;
  name: string;
}

export interface EtapeType {
  id: number;
  libelle: string;
  description: string;
}

export interface DepartementType {
  success: boolean;
  data: {
    departements: Array<{
      id: number;
      nom: string;
      mission: string;
      color: string;
      membres_count: number;
      created_at: string;
      updated_at: string;
    }>;
    statistiques_globales: {
      total_departements: number;
      total_serviteurs: number;
      moyenne_serviteurs_par_departement: number;
      departement_plus_populaire: {
        id: number;
        nom: string;
        mission: string;
        color: string;
        membres_count: number;
        created_at: string;
        updated_at: string;
      } | null;
    };
  };
  error?: string;
}

export interface MemberType {
  id: number;
  nom: string;
  prenom: string;
  adresse: string;
  ville?: string;
  telephone: string;
  email: string;
  profession?: string;
  nationalite?: string;
  color: string;
  genre: string;
  date_naissance?: string;
  situation_matrimoniale: string;
  uuid?: string;
  statut: string;
  created_at: string;
  updated_at: string;
  categorie_age?: number;
  conjoint?: number;
}

// Interface pour la réponse paginée de Django REST Framework
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Interface pour les métadonnées de pagination
export interface PaginationMeta {
  currentPage: number;
  totalPages: number;
  totalItems: number;
  itemsPerPage: number;
  hasNext: boolean;
  hasPrevious: boolean;
}

// Interface pour la réponse des membres avec pagination
export interface MembersResponse extends PaginatedResponse<MemberType> {}

export interface EnfantType {
  enfant_id: number
  pere_id: number
  mere_id: number
}

export interface RoleType {
  id: number
  nom: string
  mission?: string
}

export interface UserStatistiquesJSON {
  data: {
    statistiques_globales: {
      total_users: number
      users_actifs: number
      users_inactifs: number
      nouveaux_users: number
    }
    repartition_roles: {
      [key: string]: number
    }
    repartition_date_creation: {
      [key: string]: number
    }
  }
}

export interface IntegrationType {
  id: number
  etape_id: number
  membre_id: number
  created_at: string
}

export interface MemberStatistiquesType {
  data: {
    statistiques_globales: {
      total_membres: number
      membres_avec_email: number
      membres_avec_telephone: number
      membres_avec_date_naissance: number
      membres_avec_conjoint: number
      membres_avec_enfants: number
      nouveaux_membres: number
    }
    repartition_genre: {
      Masculin: number
      Féminin: number
    }
    repartition_statut: {
      Inscrit: number
      Membre: number
    }
    repartition_situation: {
      "Célibataire": number
      "Marié(e)": number
    }
    repartition_age: {
      moins_18: number
      "18_25": number
      "26_35": number
      "36_50": number
      plus_50: number
      total_avec_age: number
    }
    membres_par_tag: Array<{
      tag: string
      nombre: number
    }>
    membres_par_departement: Array<{
      departement: string
      nombre: number
    }>
    membres_par_groupe: Array<{
      groupe: string
      nombre: number
    }>
 }
}