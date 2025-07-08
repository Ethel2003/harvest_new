import React, { useState } from "react";
import {
  ChevronDown,
  ArrowLeft,
  Tag,
  CheckSquare,
  Users,
  RefreshCw,
  Inbox,
  Home,
  UserPlus,
} from "lucide-react";
import type { MemberType } from "../../types";

// --- Sous-composants pour la clarté ---
type InfoSectionProps = { details: Record<string, string> };
const InfoSection: React.FC<InfoSectionProps> = ({ details }) => (
  <div>
    <h3 className="text-xs font-semibold uppercase text-gray-500 mb-4 tracking-wider">
      Informations
    </h3>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
      {Object.entries(details).map(([label, value]) => (
        <div key={label}>
          <p className="text-sm font-medium text-gray-800">{label}</p>
          <p className="text-sm text-gray-600">{value || "Non spécifiée"}</p>
        </div>
      ))}
    </div>
  </div>
);

type DataPlaceholderProps = { title: string };
const DataPlaceholder: React.FC<DataPlaceholderProps> = ({ title }) => (
  <div>
    <h3 className="text-xs font-semibold uppercase text-gray-500 mb-4 tracking-wider">
      {title}
    </h3>
    <div className="flex flex-col items-center justify-center text-center py-12 bg-gray-50/70 rounded-lg border border-dashed">
      <Inbox size={48} className="text-gray-300" />
      <p className="mt-2 text-sm text-gray-500">Aucune donnée</p>
    </div>
  </div>
);

type TagsSectionProps = { tags: string[] };
const TagsSection: React.FC<TagsSectionProps> = ({ tags }) => (
  <div className="bg-white rounded-lg shadow-sm border p-4">
    <h3 className="text-xs font-semibold uppercase text-gray-500 mb-3 tracking-wider">
      Tags Associés
    </h3>
    {tags && tags.length > 0 ? (
      <div className="flex flex-wrap gap-2">
        {tags.map((tag: string) => (
          <span
            key={tag}
            className="px-3 py-1 bg-gray-100 border border-gray-200 rounded-full text-sm text-gray-700"
          >
            {tag}
          </span>
        ))}
      </div>
    ) : (
      <p className="text-sm text-gray-500 italic">Aucun tag associé.</p>
    )}
  </div>
);

const FamilySection: React.FC = () => (
  <div className="bg-white rounded-lg shadow-sm border p-4 text-center">
    <h3 className="text-xs font-semibold uppercase text-gray-500 mb-4 tracking-wider">
      Conjoint(e) & Enfants
    </h3>
    <div className="flex flex-col items-center justify-center py-6">
      <UserPlus size={40} className="text-gray-300" />
      <p className="mt-3 text-sm text-gray-500">
        Aucun(e) conjoint(e) enregistré(e)
      </p>
      <button className="mt-2 px-3 py-1 border rounded-md text-xs text-gray-600 hover:bg-gray-100">
        Ajouter un(e) conjoint(e)
      </button>
      <p className="mt-4 text-sm text-gray-500">Aucun enfant enregistré</p>
      <button className="mt-2 px-3 py-1 border rounded-md text-xs text-gray-600 hover:bg-gray-100">
        Ajouter un enfant
      </button>
    </div>
  </div>
);

// --- COMPOSANT PRINCIPAL DE LA PAGE DE DÉTAILS ---
type MemberDetailsPageProps = {
  member: MemberType;
  onBack: () => void;
};

const MemberDetailsPage: React.FC<MemberDetailsPageProps> = ({
  member,
  onBack,
}) => {
  const [isActionMenuOpen, setIsActionMenuOpen] = useState(false);

  if (!member) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p>Membre non trouvé.</p>
        <button onClick={onBack} className="ml-4 text-blue-600">
          Retour
        </button>
      </div>
    );
  }

  const infoDetails: Record<string, string> = {
    Nationalité: member.nationalite || "Non spécifiée",
    Profession: member.profession || "Non spécifiée",
    "Date de naissance": member.birthDate || "Non spécifiée",
    Ville: member.ville || "Non spécifiée",
    Adresse: member.adresse || "Non spécifiée",
    "Situation matrimoniale": member.maritalStatus || "Non spécifiée",
  };

  return (
    <div className="min-h-screen bg-[#F8F9FA] p-4 sm:p-6 lg:p-8 font-sans">
      {/* En-tête de la page */}
      <header className="flex mx-auto max-w-6xl justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800 uppercase">Details</h1>
          <div className="relative">
            <button
              onClick={() => setIsActionMenuOpen(!isActionMenuOpen)}
              className="flex items-center gap-2 px-4 py-2 bg-white text-gray-700 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors shadow-sm"
            >
              <span>Actions</span>
              <ChevronDown size={16} />
            </button>
            {isActionMenuOpen && (
              <div className="absolute right-0 mt-2 w-60 bg-white rounded-md shadow-lg border z-10">
                <ul className="py-1 text-sm text-gray-700">
                  <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center gap-3">
                    <Tag size={16} className="text-gray-400" /> Associer un tag
                  </li>
                  <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center gap-3">
                    <CheckSquare size={16} className="text-gray-400" /> Associer
                    une étape
                  </li>
                  <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center gap-3">
                    <Home size={16} className="text-gray-400" /> Insérer dans un
                    département
                  </li>
                  <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center gap-3">
                    <RefreshCw size={16} className="text-gray-400" /> Rétirer
                    d'un département
                  </li>
                  <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center gap-3">
                    <Users size={16} className="text-gray-400" /> Insérer dans
                    un groupe
                  </li>
                  <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center gap-3">
                    <RefreshCw size={16} className="text-gray-400" /> Rétirer
                    d'un groupe
                  </li>
                </ul>
              </div>
            )}
          </div>
          <button
            onClick={onBack}
            className="flex items-center gap-2 px-4 py-2 bg-white text-blue-600 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors shadow-sm"
          >
            <ArrowLeft size={16} />
            <span>Retour</span>
          </button>
        
      </header>

      {/* Carte principale des détails */}
      <main className="bg-white rounded-lg shadow-md border border-gray-200 p-8  mx-auto max-w-6xl">
        <div className="flex flex-col items-center text-center">
          <div
            className={`w-24 h-24 ${
              member.color || "bg-teal-500"
            } rounded-full flex items-center justify-center text-white text-4xl font-bold`}
          >
            {member.initials}
          </div>
          <h2 className="mt-4 text-2xl font-semibold text-gray-900">
            {member.name} {member.firstName}
          </h2>
        </div>
        <hr className="my-8" />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-10">
            <InfoSection details={infoDetails} />
            <hr />
            <DataPlaceholder title="Groupes" />
            <hr />
            <DataPlaceholder title="Départements" />
            <hr />
            <DataPlaceholder title="Intégration" />
          </div>
          <div className="lg:col-span-1 space-y-8">
            <TagsSection tags={member.tags} />
            <FamilySection />
          </div>
        </div>
      </main>
    </div>
  );
};

export default MemberDetailsPage;
