import React, { useState } from "react";
import { Link } from "react-router-dom";
import {
  Search,
  Plus,
} from "lucide-react";
import Sidebar from "./Sidebar";
import CategoryModal from "./CategoryModal";

// Un EmptyState spécifique pour les catégories
const EmptyState: React.FC = () => {
  return (
    <div className="text-center py-16 px-6 flex flex-col items-center justify-center h-full">
      <div className="w-full max-w-xs mx-auto mb-8">
        {/* SVG sur mesure évoquant l'organisation, le tri et l'étiquetage */}
        <svg viewBox="0 0 300 220" xmlns="http://www.w3.org/2000/svg">
          {/* Éléments de fond subtils */}
          <g opacity="0.4">
            <circle cx="280" cy="30" r="12" fill="#e5e7eb" />
            <rect x="20" y="180" width="30" height="8" rx="4" fill="#f3f4f6" />
            <rect x="25" y="195" width="20" height="8" rx="4" fill="#f3f4f6" />
          </g>

          {/* Dossiers/Fiches en arrière-plan */}
          <g transform="translate(10, 20)">
            <path
              d="M 40 180 L 40 50 A 10 10 0 0 1 50 40 H 120 L 140 60 H 220 A 10 10 0 0 1 230 70 V 180 Z"
              fill="#ffffff"
              stroke="#e5e7eb"
              strokeWidth="2"
            />
            <rect x="55" y="40" width="60" height="8" rx="4" fill="#d1d5db" />
          </g>
          <g transform="translate(40, 45)">
            <path
              d="M 40 155 L 40 50 A 10 10 0 0 1 50 40 H 120 L 140 60 H 220 A 10 10 0 0 1 230 70 V 155 Z"
              fill="#ffffff"
              stroke="#e5e7eb"
              strokeWidth="2"
            />
            <rect x="55" y="40" width="60" height="8" rx="4" fill="#cbd5e1" />
          </g>

          {/* Dossier principal au premier plan avec une étiquette de couleur */}
          <g transform="translate(60, 70)">
            <path
              d="M 40 130 L 40 50 A 10 10 0 0 1 50 40 H 120 L 140 60 H 220 A 10 10 0 0 1 230 70 V 130 Z"
              fill="#ffffff"
              stroke="#9ca3af"
              strokeWidth="2"
            />
            {/* Étiquette colorée */}
            <rect x="55" y="40" width="60" height="8" rx="4" fill="#a3e635" />

            {/* Contenu simulé du dossier */}
            <g transform="translate(20, 20)">
              <rect
                x="50"
                y="50"
                width="120"
                height="6"
                rx="3"
                fill="#e5e7eb"
              />
              <rect
                x="50"
                y="65"
                width="100"
                height="6"
                rx="3"
                fill="#f3f4f6"
              />
              <rect
                x="50"
                y="80"
                width="120"
                height="6"
                rx="3"
                fill="#e5e7eb"
              />
              <rect x="50" y="95" width="80" height="6" rx="3" fill="#f3f4f6" />
            </g>
          </g>

          {/* Icône flottante pour l'action */}
          <g transform="translate(240, 80)">
            <circle cx="0" cy="0" r="25" fill="#16a34a" />
            <path
              d="M -10 0 H 10 M 0 -10 V 10"
              stroke="white"
              strokeWidth="3"
              strokeLinecap="round"
            />
          </g>
        </svg>
      </div>
      <h3 className="text-xl font-semibold text-gray-800">
        Organisez vos rendez-vous par catégories
      </h3>
      <p className="mt-2 text-sm text-gray-500 max-w-lg mx-auto">
        Créez des catégories pour structurer vos entretiens et filtrer plus
        facilement votre planning. Par exemple : "Suivi spirituel", "Entretien
        d'accueil", "Aide sociale".
      </p>
    </div>
  );
};

const CategoryListPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [categories, setCategories] = useState([]); // Liste des catégories
  const [showAddCategoryModal, setShowAddCategoryModal] = useState(false);

  return (
    <div className="bg-[#f5f5f5] min-h-screen p-4 sm:p-6 lg:p-8 font-sans">
      <div className="flex flex-col lg:flex-row gap-6">
        {/* On passe la clé active pour que le Sidebar sache quel onglet illuminer */}
        <Sidebar activeKey="categories" />

        <main className="flex-1">
          <div className="bg-white rounded-xl shadow-md border border-gray-200 min-h-[85vh] flex flex-col">
            <div className="p-4 flex flex-wrap gap-4 justify-between items-center border-b border-gray-200">
              <div className="flex items-center gap-4">
                <div className="relative">
                  <Search
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                    size={18}
                  />
                  <input
                    type="text"
                    placeholder="Rechercher une catégorie..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full max-w-xs pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none bg-gray-50"
                  />
                </div>
                <span className="text-sm text-gray-500">
                  {categories.length} enregistrement trouvé
                </span>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setShowAddCategoryModal(true)}
                  className="bg-[#76C12C] text-white py-2.5 rounded-lg hover:bg-[#66a825] transition-colors font-semibold shadow-md px-4 flex items-center gap-2"
                >
                  <Plus size={16} />
                  Créer une catégorie
                </button>
              </div>
            </div>

            <div className="flex-grow flex flex-col">
              {categories.length === 0 ? (
                <EmptyState />
              ) : (
                <div className="p-4">
                  <p>La liste des catégories apparaîtrait ici.</p>
                </div>
              )}
            </div>

            <div className="p-4 flex justify-end items-center border-t border-gray-200 mt-auto">
              {/* Pagination */}
            </div>
          </div>
        </main>
      </div>

      {showAddCategoryModal && (
        <CategoryModal
          onClose={() => setShowAddCategoryModal(false)}
          onSubmit={(data) => {
            console.log(data);
          }}
        />
      )}
    </div>
  );
};

export default CategoryListPage;
