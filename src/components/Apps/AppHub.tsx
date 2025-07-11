import React from "react";
import { Link } from "react-router-dom";
import {
  FileText,
  ClipboardList,
  BookMarked,
  Building2,
  Tag,
  Users,
} from "lucide-react";

// Configuration des cartes d'applications
const APPS_CONFIG = [
  {
    id: "formulaire",
    title: "FORMULAIRE",
    subtitle: "Gestion de Formulaire",
    icon: FileText,
    path: "/apps/forms",
  },
  {
    id: "sondage",
    title: "SONDAGE",
    subtitle: "Gérer les Sondages",
    icon: ClipboardList,
    path: "/apps/surveys",
  },
  {
    id: "secretariat",
    title: "SÉCRÉTARIAT",
    subtitle: "Gérer les rendez-vous",
    icon: BookMarked,
    path: "/secretariat",
  },
  {
    id: "departement",
    title: "DÉPARTEMENT",
    subtitle: "Organiser les départements",
    icon: Building2,
    path: "/departments",
  },
  {
    id: "tags",
    title: "TAGS",
    subtitle: "Gérer les tags et étiquettes",
    icon: Tag,
    path: "/tags",
  },
  {
    id: "groupes",
    title: "GROUPES",
    subtitle: "Gérer les groupes d'utilisateurs",
    icon: Users,
    path: "/groups",
  },
];

const FormBuilder: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 flex flex-col items-center justify-center py-10 px-4">
      {/* Description professionnelle en haut */}
      <div className="max-w-2xl w-full mb-10 text-center">
        <h1 className="text-3xl md:text-4xl font-extrabold text-gray-900 mb-2 tracking-tight">
          Espace Applications
        </h1>
        <p className="text-gray-500 text-lg md:text-xl font-medium">
          Accédez rapidement à vos outils essentiels&nbsp;: formulaires,
          sondages, gestion des rendez-vous,  des départements, 
          des tags et des groupes d'utilisateurs.{" "}
          <br className="hidden md:block" />
        </p>
      </div>
      {/* Grille des applications */}
      <div className="w-full max-w-5xl grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        {APPS_CONFIG.map((app) => (
          <Link
            key={app.id}
            to={app.path}
            className="group block focus:outline-none focus:ring-4 focus:ring-green-200 rounded-2xl transition-shadow"
          >
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100 hover:shadow-2xl hover:border-green-200 transition-all duration-300 flex flex-col items-center text-center relative overflow-hidden">
              {/* Effet décoratif pro */}
              <div className="absolute -top-6 -right-6 w-20 h-20 bg-green-50 rounded-full opacity-60 group-hover:scale-110 group-hover:opacity-80 transition-transform duration-300 z-0" />
              {/* Icône */}
              <div className="relative z-10 w-16 h-16 bg-gradient-to-tr from-green-100 to-green-200 rounded-xl flex items-center justify-center mb-5 shadow group-hover:from-green-200 group-hover:to-green-300 transition-colors">
                <app.icon
                  className="text-green-600 group-hover:text-green-700 transition-colors duration-200"
                  size={36}
                />
              </div>
              {/* Titre */}
              <p className="text-lg font-bold text-gray-800 mb-1 tracking-wide uppercase letter-spacing-1 z-10">
                {app.title}
              </p>
              {/* Sous-titre */}
              <p className="text-gray-500 text-base font-medium z-10">
                {app.subtitle}
              </p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default FormBuilder;
