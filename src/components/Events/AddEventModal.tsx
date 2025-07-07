import { Calendar, X } from "lucide-react";

interface AddEventModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const AddEventModal = ({ isOpen, onClose }: AddEventModalProps) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl shadow-lg w-full max-w-lg relative">
        {/* Bouton de fermeture (croix) */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-700 focus:outline-none"
          aria-label="Fermer la modale"
        >
          <X size={24} />
        </button>
        <div className="p-6">
          <div className="mb-6 flex items-center justify-between">
            <h3 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
              <Calendar className="text-[#76C12C]" size={28} />
              Créer un événement
            </h3>
          </div>
          <form className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Titre */}
              <div>
                <label htmlFor="event-title" className="block text-xs font-semibold text-gray-700 mb-1 uppercase tracking-wide">
                  Titre
                </label>
                <input
                  id="event-title"
                  type="text"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:border-transparent transition"
                  placeholder="Ex : Réunion de lancement"
                />
              </div>
              {/* Type */}
              <div>
                <label htmlFor="event-type" className="block text-xs font-semibold text-gray-700 mb-1 uppercase tracking-wide">
                  Type
                </label>
                <select
                  id="event-type"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:border-transparent transition"
                >
                  <option value="meeting">Réunion</option>
                  <option value="workshop">Atelier</option>
                  <option value="conference">Conférence</option>
                  <option value="social">Social</option>
                </select>
              </div>
              {/* Date */}
              <div>
                <label htmlFor="event-date" className="block text-xs font-semibold text-gray-700 mb-1 uppercase tracking-wide">
                  Date
                </label>
                <div className="relative">
                  <input
                    id="event-date"
                    type="date"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:border-transparent transition"
                  />
                  <Calendar className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
                </div>
              </div>
              {/* Heure */}
              <div>
                <label htmlFor="event-time" className="block text-xs font-semibold text-gray-700 mb-1 uppercase tracking-wide">
                  Heure
                </label>
                <div className="relative">
                  <input
                    id="event-time"
                    type="time"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:border-transparent transition"
                  />
                </div>
              </div>
              {/* Lieu */}
              <div className="md:col-span-2">
                <label htmlFor="event-location" className="block text-xs font-semibold text-gray-700 mb-1 uppercase tracking-wide">
                  Lieu
                </label>
                <input
                  id="event-location"
                  type="text"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:border-transparent transition"
                  placeholder="Ex : Salle A, En ligne, etc."
                />
              </div>
              {/* Description */}
              <div className="md:col-span-2">
                <label htmlFor="event-description" className="block text-xs font-semibold text-gray-700 mb-1 uppercase tracking-wide">
                  Description
                </label>
                <textarea
                  id="event-description"
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:border-transparent transition"
                  placeholder="Décris brièvement l'événement"
                />
              </div>
            </div>
            <div className="flex space-x-3 pt-4">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
              >
                Annuler
              </button>
              <button
                type="submit"
                className="flex-1 px-4 py-2 text-white bg-[#76C12C] rounded-lg hover:bg-[#5da021] transition-colors flex items-center justify-center gap-2"
              >
                <Calendar size={18} /> Créer
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AddEventModal; 