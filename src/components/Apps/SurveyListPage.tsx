import React, { useState } from "react";
import {
  ClipboardList,
  Plus,
  Search,
  ChevronLeft,
  ChevronRight,
  Percent,
  Edit2,
  Trash2,
} from "lucide-react";

// Types pour la simulation
type Survey = {
  id: number;
  name: string;
  description: string;
  responses: number;
  totalInvited: number;
  createdAt: string;
};

/**
 * Page de gestion complète pour les Sondages.
 * Structure : formulaire à gauche, liste visuelle à droite.
 */
const SurveyListPage: React.FC = () => {
  // Données de simulation pour un affichage riche
  const [surveys, setSurveys] = useState<Survey[]>([
    {
      id: 1,
      name: "Satisfaction Culte du Dimanche",
      description: "Mesurer l'appréciation générale du service.",
      responses: 82,
      totalInvited: 150,
      createdAt: "01/05/2024",
    },
    {
      id: 2,
      name: "Idées pour le prochain séminaire",
      description: "Recueillir les thèmes préférés de la communauté.",
      responses: 45,
      totalInvited: 200,
      createdAt: "15/04/2024",
    },
  ]);

  const [searchTerm, setSearchTerm] = useState("");

  const handleCreate = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const newSurvey: Survey = {
      id: Date.now(),
      name: formData.get("name") as string,
      description: formData.get("description") as string,
      responses: 0,
      totalInvited: 0,
      createdAt: new Date().toLocaleDateString("fr-FR"),
    };
    setSurveys((prev) => [newSurvey, ...prev]);
    e.currentTarget.reset();
  };

  // Fonction pour calculer le pourcentage et la couleur de la barre
  const getProgressDetails = (responses: number, total: number) => {
    if (total === 0) return { percent: 0, color: "bg-gray-200" };
    const percent = Math.round((responses / total) * 100);
    if (percent < 30) return { percent, color: "bg-yellow-400" };
    if (percent < 70) return { percent, color: "bg-blue-500" };
    return { percent, color: "bg-green-500" };
  };

  return (
    <div className="min-h-screen bg-[#F8F9FA] p-4 sm:p-6 lg:p-8 font-sans">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">
          Gestion des Sondages
        </h1>
        <p className="text-gray-500 mt-1">
          Créez des sondages, collectez des réponses et analysez les résultats.
        </p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Colonne de Gauche : Formulaire de Création */}
        <aside className="lg:col-span-1">
          <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200 sticky top-6">
            <h2 className="text-lg font-semibold text-gray-700 mb-4">
              Lancer un nouveau sondage
            </h2>
            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label
                  htmlFor="name"
                  className="block text-sm font-medium text-gray-600 mb-1"
                >
                  Nom du sondage
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  placeholder="Ex: Qualité de l'accueil"
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-green-500 focus:outline-none"
                  required
                />
              </div>
              <div>
                <label
                  htmlFor="description"
                  className="block text-sm font-medium text-gray-600 mb-1"
                >
                  Objectif du sondage
                </label>
                <textarea
                  id="description"
                  name="description"
                  placeholder="Quel est le but de ce sondage ?"
                  rows={4}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-green-500 focus:outline-none"
                />
              </div>
              <p className="text-xs text-gray-400 pt-2">
                Les questions du sondage pourront être ajoutées après sa
                création.
              </p>
              <button
                type="submit"
                className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors shadow font-semibold"
              >
                <Plus size={18} />
                Créer le sondage
              </button>
            </form>
          </div>
        </aside>

        {/* Colonne de Droite : Liste */}
        <main className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow-md border border-gray-200">
            <div className="p-4 flex justify-between items-center border-b border-gray-200">
              <div className="relative w-full max-w-xs">
                <Search
                  className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                  size={18}
                />
                <input
                  type="text"
                  placeholder="Rechercher un sondage..."
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none"
                />
              </div>
              <select className="px-3 py-2 border border-gray-300 rounded-full text-sm focus:ring-1 focus:ring-green-500 focus:outline-none bg-white">
                <option>5 résultats par page</option>
              </select>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 text-xs text-gray-500 uppercase">
                  <tr>
                    <th className="px-6 py-3 text-left w-2/5">
                      Nom du Sondage
                    </th>
                    <th className="px-6 py-3 text-left w-2/5">
                      Taux de Réponse
                    </th>
                    <th className="px-6 py-3 text-left w-1/5">Créé le</th>
                    <th className="px-6 py-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {surveys.length > 0 ? (
                    surveys.map((survey) => {
                      const { percent, color } = getProgressDetails(
                        survey.responses,
                        survey.totalInvited
                      );
                      return (
                        <tr
                          key={survey.id}
                          className="hover:bg-gray-50/50 transition-colors"
                        >
                          <td className="px-6 py-4">
                            <p className="font-semibold text-gray-800">
                              {survey.name}
                            </p>
                            <p className="text-gray-500 text-xs truncate max-w-xs">
                              {survey.description}
                            </p>
                          </td>
                          <td className="px-6 py-4">
                            {/* La surprise : une barre de progression visuelle ! */}
                            <div className="flex items-center gap-3">
                              <div className="w-full bg-gray-200 rounded-full h-2">
                                <div
                                  className={`${color} h-2 rounded-full`}
                                  style={{ width: `${percent}%` }}
                                ></div>
                              </div>
                              <span className="font-semibold text-gray-700 w-12 text-right">
                                {percent}%
                              </span>
                            </div>
                            <p className="text-xs text-gray-400 mt-1">
                              {survey.responses} / {survey.totalInvited}{" "}
                              réponses
                            </p>
                          </td>
                          <td className="px-6 py-4 text-gray-500">
                            {survey.createdAt}
                          </td>
                          <td className="px-6 py-4 text-right">
                            <div className="flex justify-end gap-2">
                              <button className="p-3 text-blue-600 rounded-full transition-colors duration-200 hover:bg-blue-100 hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-200">
                                <Edit2 size={16} />
                              </button>
                              <button  className="p-3 text-red-600 rounded-full transition-colors duration-200 hover:bg-red-100 hover:text-red-600 focus:outline-none focus:ring-2 focus:ring-red-200">
                                <Trash2 size={16} />
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })
                  ) : (
                    <tr>
                      <td colSpan={4} className="text-center py-20 px-6">
                        <div className="mx-auto w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                          <ClipboardList size={48} className="text-gray-400" />
                        </div>
                        <h3 className="font-semibold text-lg text-gray-700">
                          Aucun sondage en cours
                        </h3>
                        <p className="text-gray-500 text-sm mt-1">
                          Lancez votre premier sondage pour recueillir de
                          précieux avis.
                        </p>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            <div className="p-4 flex justify-center items-center gap-4 border-t border-gray-200">
              {/* Pagination */}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default SurveyListPage;
