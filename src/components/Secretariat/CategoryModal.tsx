import React, { useRef, useEffect } from "react";
import { X, Plus } from "lucide-react";

export type CategoryModalProps = {
  onClose: () => void;
  onSubmit: (data: any) => void;
};

const CategoryModal: React.FC<CategoryModalProps> = ({ onClose, onSubmit }) => {
  const firstInputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    firstInputRef.current?.focus();
  }, []);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-lg shadow-2xl w-full max-w-lg p-8 relative">
        {/* Bouton de fermeture */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-red-500"
          aria-label="Fermer le modal"
        >
          <X size={22} />
        </button>
        {/* Titre */}
        <h2 className="text-lg font-bold uppercase mb-2 text-gray-800 tracking-wide">
          Ajouter une catégorie de rendez-vous
        </h2>
        <div className="mb-4 text-gray-500 text-sm">
          Merci de renseigner les informations pour ajouter une nouvelle
          catégorie de rendez-vous.
        </div>
        <hr className="mb-6" />
        {/* Formulaire */}
        <form
          className="flex flex-col gap-5"
          onSubmit={(e) => {
            e.preventDefault();
            // Récupère les données ici
            onSubmit({});
          }}
        >
          <div>
            <label className="font-semibold mb-1 block">Description *</label>
            <textarea
              ref={firstInputRef}
              className="w-full border rounded px-3 py-2 min-h-[80px] focus:ring-2 focus:ring-[#76C12C] focus:border-[#76C12C] transition placeholder:text-gray-400 resize-none"
              placeholder="Description de la catégorie..."
              aria-label="Description de la catégorie"
              required
            />
          </div>
          <div>
            <label className="font-semibold mb-1 block">
              Choisir les leaders
            </label>
            <select className="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-[#76C12C] focus:border-[#76C12C] transition">
              <option>Sélectionner la ou les leader(s)...</option>
            </select>
          </div>
          {/* Boutons */}
          <div className="flex justify-end gap-4 mt-6">
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-2 bg-red-700 text-white rounded font-semibold hover:bg-red-800 transition-colors flex items-center gap-2"
              aria-label="Annuler"
            >
              <X size={18} /> Annuler
            </button>
            <button
              type="submit"
              className="bg-[#76C12C] text-white py-2.5 rounded-lg hover:bg-[#66a825] transition-colors font-semibold shadow-md px-6 flex items-center gap-2"
              aria-label="Ajouter la catégorie"
            >
              <Plus size={18} /> Ajouter
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CategoryModal;
