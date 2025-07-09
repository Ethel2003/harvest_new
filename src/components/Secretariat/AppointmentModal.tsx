import React, { useRef, useEffect } from "react";
import { X, Plus } from "lucide-react";

export type AppointmentModalProps = {
  onClose: () => void;
  onSubmit: (data: any) => void;
};

const AppointmentModal: React.FC<AppointmentModalProps> = ({
  onClose,
  onSubmit,
}) => {
  const firstInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    firstInputRef.current?.focus();
  }, []);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-lg shadow-2xl w-full max-w-3xl p-8 relative">
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
          Créer un rendez-vous
        </h2>
        <div className="mb-4 text-gray-500 text-sm">
          Merci de remplir tous les champs nécessaires pour planifier un nouveau
          rendez-vous.
        </div>
        <hr className="mb-6" />
        {/* Formulaire */}
        <form
          className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-5"
          onSubmit={(e) => {
            e.preventDefault();
            // Récupère les données ici
            onSubmit({});
          }}
        >
          {/* Colonne 1 */}
          <div className="flex flex-col gap-4">
            <div>
              <label className="font-semibold mb-1 block">Nom *</label>
              <input
                ref={firstInputRef}
                className="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-[#76C12C] focus:border-[#76C12C] transition placeholder:text-gray-400"
                placeholder="Entrez le nom du membre..."
                required
                aria-label="Nom du membre"
              />
            </div>
            <div>
              <label className="font-semibold mb-1 block">Profession</label>
              <input
                className="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-[#76C12C] focus:border-[#76C12C] transition placeholder:text-gray-400"
                placeholder="Profession du membre..."
                aria-label="Profession"
              />
            </div>
            <div>
              <label className="font-semibold mb-1 block">
                Pasteur / Leader
              </label>
              <select className="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-[#76C12C] focus:border-[#76C12C] transition">
                <option>Sélectionner un leader...</option>
              </select>
            </div>
            <div>
              <label className="font-semibold mb-1 block">
                Heure de rendez-vous
              </label>
              <select className="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-[#76C12C] focus:border-[#76C12C] transition">
                <option>Sélectionner une plage horaire...</option>
              </select>
            </div>
            <div>
              <label className="font-semibold mb-1 block">Email</label>
              <input
                className="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-[#76C12C] focus:border-[#76C12C] transition placeholder:text-gray-400"
                placeholder="Adresse email..."
                type="email"
                aria-label="Email"
              />
            </div>
            <div>
              <label className="font-semibold mb-1 block">Adresse</label>
              <input
                className="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-[#76C12C] focus:border-[#76C12C] transition placeholder:text-gray-400"
                placeholder="Adresse du membre..."
                aria-label="Adresse"
              />
            </div>
          </div>
          {/* Colonne 2 */}
          <div className="flex flex-col gap-4">
            <div>
              <label className="font-semibold mb-1 block">Prénom *</label>
              <input
                className="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-[#76C12C] focus:border-[#76C12C] transition placeholder:text-gray-400"
                placeholder="Entrez le prénom du membre..."
                required
                aria-label="Prénom du membre"
              />
            </div>
            <div>
              <label className="font-semibold mb-1 block">
                Catégorie de rendez-vous
              </label>
              <select className="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-[#76C12C] focus:border-[#76C12C] transition">
                <option>Sélectionner la catégorie de rendez-vous...</option>
              </select>
            </div>
            <div>
              <label className="font-semibold mb-1 block">
                Date de rendez-vous
              </label>
              <select className="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-[#76C12C] focus:border-[#76C12C] transition">
                <option>Sélectionner une date de rendez-vous...</option>
              </select>
            </div>
            <div>
              <label className="font-semibold mb-1 block">Téléphone</label>
              <input
                className="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-[#76C12C] focus:border-[#76C12C] transition placeholder:text-gray-400"
                placeholder="Numéro de téléphone..."
                aria-label="Téléphone"
              />
            </div>
            <div>
              <label className="font-semibold mb-1 block">Ville</label>
              <input
                className="w-full border rounded px-3 py-2 focus:ring-2 focus:ring-[#76C12C] focus:border-[#76C12C] transition placeholder:text-gray-400"
                placeholder="Ville du membre..."
                aria-label="Ville"
              />
            </div>
          </div>
          {/* Boutons */}
          <div className="col-span-1 md:col-span-2 flex justify-end gap-4 mt-6">
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
              className="px-6 py-2 bg-[#76C12C] text-white rounded font-semibold hover:bg-[#66a825] transition-colors flex items-center gap-2"
              aria-label="Ajouter le rendez-vous"
            >
              <Plus size={18} /> Ajouter
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AppointmentModal;
