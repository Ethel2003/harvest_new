import React, { useState } from "react";
import { Link } from "react-router-dom";
import {
  Search,
  Calendar,
  Plus,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import Sidebar from "./Sidebar";
import AppointmentModal from "./AppointmentModal";

// --- SOUS-COMPOSANTS ---

/**
 * Le magnifique état "vide" avec l'illustration SVG recréée.
 */
const EmptyState: React.FC = () => (
  <div className="text-center py-16 px-6 flex flex-col items-center justify-center h-full">
    <div className="w-full max-w-sm mx-auto mb-8">
      {/* SVG  */}
      <svg viewBox="0 0 350 250" xmlns="http://www.w3.org/2000/svg">
        <g opacity="0.1">
          <circle cx="288" cy="130" r="10" fill="#4ade80" />
          <circle cx="68" cy="195" r="15" fill="#4ade80" />
          <path
            d="M 320 20 a 10 10 0 1 0 20 0 a 10 10 0 1 0 -20 0"
            fill="#4ade80"
          />
        </g>
        <g transform="translate(20, 190)">
          <path
            d="M 0 0 h 30 a 10 10 0 0 1 10 10 v 20 H -10 v -20 a 10 10 0 0 1 10 -10 z"
            fill="#d1d5db"
          />
          <g transform="translate(15, 0)">
            <path
              d="M -20 -50 c 0 -20 40 -20 40 0 l 0 20 l -10 0 c 0 0 -5 -15 -20 -15 s -20 15 -20 15 l -10 0 z"
              fill="#a3e635"
            />
            <path
              d="M -15 -30 c 0 -10 30 -10 30 0"
              fill="#65a30d"
              opacity="0.5"
            />
          </g>
        </g>
        <g id="phone-ui">
          <rect
            x="100"
            y="20"
            width="150"
            height="210"
            rx="20"
            fill="#ffffff"
            stroke="#e5e7eb"
            strokeWidth="2"
          />
          <line
            x1="115"
            y1="40"
            x2="160"
            y2="40"
            stroke="#d1d5db"
            strokeWidth="4"
            strokeLinecap="round"
          />
          <circle
            cx="230"
            cy="40"
            r="8"
            fill="#f3f4f6"
            stroke="#e5e7eb"
            strokeWidth="1"
          />
          <rect x="115" y="60" width="120" height="80" rx="10" fill="#f3f4f6" />
          <rect x="125" y="70" width="30" height="30" rx="5" fill="#a3e635" />
          <rect x="165" y="75" width="60" height="8" rx="4" fill="#d1d5db" />
          <rect x="165" y="90" width="40" height="8" rx="4" fill="#e5e7eb" />
          <path
            d="M 235 65 l -10 10 l -5 -5"
            stroke="#4ade80"
            strokeWidth="3"
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <rect x="115" y="150" width="55" height="30" rx="5" fill="#f3f4f6" />
          <rect x="180" y="150" width="55" height="30" rx="5" fill="#f3f4f6" />
          <rect
            x="115"
            y="190"
            width="120"
            height="25"
            rx="12.5"
            fill="#a3e635"
          />
        </g>
        <g id="person">
          <path d="M 230 110 l 15 40 l -30 0 z" fill="#4b5563" />
          <circle cx="230" cy="95" r="12" fill="#374151" />
          <g transform="translate(230, 150)">
            <path d="M 0 0 l -10 30 h 20 z" fill="#6b7280" />
          </g>
          <g id="arm" transform="translate(225, 115) rotate(-30)">
            <rect x="-35" y="-5" width="40" height="10" rx="5" fill="#4b5563" />
          </g>
        </g>
        <g id="magnifying-glass" transform="translate(280, 160)">
          <circle r="18" fill="#ffffff" stroke="#9ca3af" strokeWidth="2" />
          <circle r="12" fill="none" stroke="#9ca3af" strokeWidth="2" />
          <line
            x1="15"
            y1="15"
            x2="25"
            y2="25"
            stroke="#9ca3af"
            strokeWidth="3"
            strokeLinecap="round"
          />
        </g>
      </svg>
    </div>
    <h3 className="text-xl font-semibold text-gray-800">
      Nous n'avons pas trouvé de résultats correspondants.
    </h3>
    <p className="mt-2 text-sm text-gray-500 max-w-lg mx-auto">
      Dommage. Il semble que nous n'ayons trouvé aucun résultat correspondant
      aux termes de recherche que vous avez saisis. Veuillez essayer d'autres
      termes de recherche ou critères.
    </p>
  </div>
);


/**
 * Le composant principal, maintenant simplifié.
 */
const AppointmentsList: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [appointments, setAppointments] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);

  // 3. Suppression des états pour les autres modales
  // const [showAvailabilityModal, setShowAvailabilityModal] = useState(false);
  // const [showCategoryModal, setShowCategoryModal] = useState(false);

  const filteredAppointments = appointments.filter(() => true);

  return (
    <div className="bg-[#f5f5f5] min-h-screen p-4 sm:p-6 lg:p-8 font-sans">
      <div className="flex flex-col lg:flex-row gap-6">
        {/* 4. On passe la clé de l'onglet actif au Sidebar */}
        <Sidebar activeKey="rendez-vous" />

        <main className="flex-1">
          <div className="bg-white rounded-xl shadow-md border border-gray-200 min-h-[85vh] flex flex-col">
            <div className="p-4 flex flex-wrap gap-4 justify-between items-center border-b border-gray-200">
              <div className="flex items-center gap-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
                  <input
                    type="text"
                    placeholder="Rechercher..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full max-w-xs pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none bg-gray-50"
                  />
                </div>
                <span className="text-sm text-gray-500">{filteredAppointments.length} enregistrement trouvé</span>
              </div>
              <div className="flex items-center gap-2">
                <button className="px-4 py-2 bg-white text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-100 text-sm font-medium flex items-center gap-2 transition-colors">
                  <Calendar size={16} /> Voir le résumé
                </button>
                <button
                  onClick={() => setShowAddModal(true)}
                  className="bg-[#76C12C] text-white py-2.5 rounded-lg hover:bg-[#66a825] transition-colors font-semibold shadow-md px-4 flex items-center gap-2"
                >
                  <Plus size={16} /> Créer un nouveau rendez-vous
                </button>
              </div>
            </div>

            <div className="flex-grow flex flex-col">
              {filteredAppointments.length === 0 ? (
                <EmptyState />
              ) : (
                <div className="p-4"><p>La liste des rendez-vous apparaîtrait ici.</p></div>
              )}
            </div>

            <div className="p-4 flex justify-end items-center border-t border-gray-200 mt-auto">
                <div className="flex items-center gap-2">
                    <button disabled className="p-2 rounded-lg border bg-white hover:bg-gray-100 disabled:opacity-50"><ChevronLeft size={18} /></button>
                    <button disabled className="p-2 rounded-lg border bg-white hover:bg-gray-100 disabled:opacity-50"><ChevronRight size={18} /></button>
                </div>
            </div>
          </div>
        </main>
      </div>

      {showAddModal && (
        <AppointmentModal onClose={() => setShowAddModal(false)} onSubmit={() => { setShowAddModal(false); }}/>
      )}
    </div>
  );
};

export default AppointmentsList;