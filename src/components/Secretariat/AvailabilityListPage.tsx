
import React, { useState } from "react";
import {
  Search,
  Plus,
} from "lucide-react";
import Sidebar from "./Sidebar";
import AvailabilityModal from "./AvailabilityModal";
import { Link } from "react-router-dom";

// On peut aussi réutiliser l'EmptyState
const EmptyState: React.FC = () => {
  return (
    <div className="text-center py-16 px-6 flex flex-col items-center justify-center h-full">
      <div className="w-full max-w-xs mx-auto mb-8">
        {/* SVG sur mesure évoquant la planification et la disponibilité */}
        <svg viewBox="0 0 300 220" xmlns="http://www.w3.org/2000/svg">
          {/* Éléments de fond décoratifs */}
          <g opacity="0.5">
            <circle cx="20" cy="20" r="10" fill="#a3e635" opacity="0.3" />
            <rect
              x="270"
              y="180"
              width="20"
              height="20"
              rx="5"
              fill="#e5e7eb"
            />
            <path
              d="M 280 40 L 290 50 L 280 60 Z"
              fill="#a3e635"
              opacity="0.4"
            />
          </g>

          {/* Calendrier stylisé */}
          <g id="calendar">
            <rect
              x="50"
              y="30"
              width="200"
              height="160"
              rx="15"
              fill="#ffffff"
              stroke="#e5e7eb"
              strokeWidth="2"
            />
            <rect
              x="50"
              y="30"
              width="200"
              height="30"
              rx="15"
              ry="15"
              fill="#f3f4f6"
              stroke="#e5e7eb"
              strokeWidth="2"
              style={{ borderBottomLeftRadius: 0, borderBottomRightRadius: 0 }}
            />
            <circle cx="65" cy="45" r="4" fill="#fca5a5" />
            <circle cx="80" cy="45" r="4" fill="#fde047" />
            <circle cx="95" cy="45" r="4" fill="#86efac" />

            {/* Grille du calendrier */}
            <g stroke="#f3f4f6" strokeWidth="1">
              <line x1="50" y1="90" x2="250" y2="90" />
              <line x1="50" y1="125" x2="250" y2="125" />
              <line x1="50" y1="160" x2="250" y2="160" />
              <line x1="100" y1="60" x2="100" y2="190" />
              <line x1="150" y1="60" x2="150" y2="190" />
              <line x1="200" y1="60" x2="200" y2="190" />
            </g>

            {/* Cases cochées */}
            <rect
              x="110"
              y="100"
              width="30"
              height="15"
              rx="4"
              fill="#dcfce7"
            />
            <path
              d="M 115 107 l 5 5 l 10 -10"
              stroke="#22c55e"
              strokeWidth="2"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
            />

            <rect
              x="160"
              y="135"
              width="30"
              height="15"
              rx="4"
              fill="#dcfce7"
            />
            <path
              d="M 165 142 l 5 5 l 10 -10"
              stroke="#22c55e"
              strokeWidth="2"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </g>

          {/* Personnage ajoutant une disponibilité */}
          <g id="person">
            <g transform="translate(60, 150)">
              <path d="M -10 0 C -10 -20, 10 -20, 10 0 Z" fill="#6b7280" />
              <circle cx="0" cy="-25" r="10" fill="#4b5563" />
            </g>
            <g transform="translate(85, 110) rotate(20)">
              <rect
                x="-30"
                y="-4"
                width="35"
                height="8"
                rx="4"
                fill="#4b5563"
              />
              {/* Checkmark en main */}
              <g transform="translate(-35, 0)">
                <rect width="20" height="20" rx="5" fill="#16a34a" />
                <path
                  d="M 5 10 l 4 4 l 6 -6"
                  stroke="white"
                  strokeWidth="2"
                  fill="none"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </g>
            </g>
          </g>
        </svg>
      </div>
      <h3 className="text-xl font-semibold text-gray-800">
        Définissez vos premières disponibilités
      </h3>
      <p className="mt-2 text-sm text-gray-500 max-w-lg mx-auto">
        Créez des créneaux horaires pour indiquer quand vous êtes libre, et
        permettez ainsi aux membres de prendre rendez-vous avec vous facilement.
      </p>
    </div>
  );
};

const AvailabilityListPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [availabilities, setAvailabilities] = useState([]); // Liste des disponibilités
  const [showAddAvailabilityModal, setShowAddAvailabilityModal] =
    useState(false);

  return (
    <div className="bg-[#f5f5f5] min-h-screen p-4 sm:p-6 lg:p-8 font-sans">
      <div className="flex flex-col lg:flex-row gap-6">
        <Sidebar activeKey="disponibilites" />

        <main className="flex-1">
          <div className="bg-white rounded-xl shadow-md border border-gray-200 min-h-[85vh] flex flex-col">
            <div className="p-4 flex flex-wrap gap-4 justify-between items-center border-b border-gray-200">
              {/* En-tête de la section */}
              <div className="flex items-center gap-4">
                <div className="relative">
                  <Search
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                    size={18}
                  />
                  <input
                    type="text"
                    placeholder="Rechercher..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full max-w-xs pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none bg-gray-50"
                  />
                </div>
                <span className="text-sm text-gray-500">
                  {availabilities.length} enregistrement trouvé
                </span>
              </div>
              <div className="flex items-center gap-2">
                {/* C'est ce bouton qui ouvre la modale de création */}
                <button
                  onClick={() => setShowAddAvailabilityModal(true)}
                  className="bg-[#76C12C] text-white py-2.5 rounded-lg hover:bg-[#66a825] transition-colors font-semibold shadow-md px-4 flex items-center gap-2"
                >
                  <Plus size={16} />
                  Créer une disponibilité
                </button>
              </div>
            </div>

            {/* Contenu principal */}
            <div className="flex-grow flex flex-col">
              {availabilities.length === 0 ? (
                <EmptyState />
              ) : (
                <div className="p-4">
                  <p>La liste des disponibilités apparaîtrait ici.</p>
                </div>
              )}
            </div>

            {/* Pagination */}
            <div className="p-4 flex justify-end items-center border-t border-gray-200 mt-auto">
              {/* ... votre pagination ... */}
            </div>
          </div>
        </main>
      </div>

      {/* La modale est maintenant gérée par CETTE page */}
      {showAddAvailabilityModal && (
        <AvailabilityModal
          onClose={() => setShowAddAvailabilityModal(false)}
          onSubmit={(data) => {
            console.log(data);
          }}
        />
      )}
    </div>
  );
};

export default AvailabilityListPage;
