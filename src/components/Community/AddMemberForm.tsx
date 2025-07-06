import React from "react";
import { X } from "lucide-react";

interface AddMemberFormProps {
  onClose: () => void;
}

const AddMemberForm: React.FC<AddMemberFormProps> = ({ onClose }) => {
  return (
    <div className="bg-white rounded-xl shadow-lg w-full max-w-2xl">
      <div className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-bold text-gray-900">
            ENREGISTRER UN NOUVEAU MEMBRE
          </h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="w-6 h-6" />
          </button>
        </div>
        <hr className="mb-6" />
        <form className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
          {/* Colonne 1 */}
          <div className="flex flex-col gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Nom *
              </label>
              <input
                type="text"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:border-transparent"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Genre *
              </label>
              <div className="flex items-center gap-6 mt-1">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="genre"
                    value="Homme"
                    className="h-5 w-5 rounded-full border-2 border-gray-300 text-[#76C12C] focus:ring-[#76C12C] appearance-none checked:bg-[#76C12C] checked:border-[#76C12C] transition-all"
                    required
                  />
                  <span className="text-sm">Homme</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="genre"
                    value="Femme"
                    className="h-5 w-5 rounded-full border-2 border-gray-300 text-[#76C12C] focus:ring-[#76C12C] appearance-none checked:bg-[#76C12C] checked:border-[#76C12C] transition-all"
                    required
                  />
                  <span className="text-sm">Femme</span>
                </label>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Nationalité
              </label>
              <input
                type="text"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Situation matrimoniale
              </label>
              <div className="flex items-center gap-6 mt-1">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="situation"
                    value="Célibataire"
                    className="h-5 w-5 rounded-full border-2 border-gray-300 text-[#76C12C] focus:ring-[#76C12C] appearance-none checked:bg-[#76C12C] checked:border-[#76C12C] transition-all"
                  />
                  <span className="text-sm">Célibataire</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="situation"
                    value="Marié(e)"
                    className="h-5 w-5 rounded-full border-2 border-gray-300 text-[#76C12C] focus:ring-[#76C12C] appearance-none checked:bg-[#76C12C] checked:border-[#76C12C] transition-all"
                  />
                  <span className="text-sm">Marié(e)</span>
                </label>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Adresse
              </label>
              <input
                type="text"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:border-transparent"
              />
            </div>
          </div>
          {/* Colonne 2 */}
          <div className="flex flex-col gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Prénom(s) *
              </label>
              <input
                type="text"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:border-transparent"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Date de naissance
              </label>
              <input
                type="date"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:border-transparent"
                placeholder="jj/mm/aaaa"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Profession
              </label>
              <input
                type="text"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Téléphone
              </label>
              <input
                type="tel"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Ville
              </label>
              <input
                type="text"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Ajouter une image
              </label>
              <input
                type="file"
                accept="image/*"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:border-transparent file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:bg-gray-100 file:text-gray-700"
              />
            </div>
          </div>
          {/* Boutons bas de formulaire */}
          <div className="col-span-1 md:col-span-2 flex justify-end gap-4 mt-6">
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-2 rounded-lg bg-red-600 text-white font-semibold hover:bg-red-700 transition-colors"
            >
              Fermer
            </button>
            <button
              type="submit"
              className="px-6 py-2 rounded-lg bg-green-600 text-white font-semibold hover:bg-green-700 transition-colors"
            >
              Enregistrer
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddMemberForm;
