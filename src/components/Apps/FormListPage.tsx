import React, { useState } from "react";
import {
  FileText,
  Plus,
  Search,
  ChevronLeft,
  ChevronRight,
  Hash,
  ListChecks,
  MessageSquare,
  Edit2,
  Trash2,
} from "lucide-react";

// Types pour la simulation
type Form = {
  id: number;
  name: string;
  description: string;
  fields: { type: string; count: number }[];
  submissions: number;
  createdAt: string;
};

/**
 * Page de gestion complète pour les Formulaires.
 * Structure : formulaire de création à gauche, liste riche à droite.
 */
const FormListPage: React.FC = () => {
  // Données de simulation avec plus de détails pour un affichage riche
  const [forms, setForms] = useState<Form[]>([
    {
      id: 1,
      name: "Inscription Événement Annuel",
      description:
        "Recueillir les inscriptions pour notre conférence annuelle.",
      fields: [
        { type: "Nom", count: 2 },
        { type: "Email", count: 1 },
        { type: "Liste", count: 1 },
      ],
      submissions: 128,
      createdAt: "15/01/2024",
    },
    {
      id: 2,
      name: "Feedback Post-Culte",
      description: "Sondage de satisfaction après chaque service du dimanche.",
      fields: [
        { type: "Note", count: 1 },
        { type: "Texte", count: 1 },
      ],
      submissions: 76,
      createdAt: "03/02/2024",
    },
  ]);

  const [searchTerm, setSearchTerm] = useState("");

  const handleCreate = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const newForm: Form = {
      id: Date.now(),
      name: formData.get("name") as string,
      description: formData.get("description") as string,
      fields: [],
      submissions: 0,
      createdAt: new Date().toLocaleDateString("fr-FR"),
    };
    setForms((prev) => [newForm, ...prev]);
    e.currentTarget.reset();
  };

  return (
    <div className="min-h-screen bg-[#F8F9FA] p-4 sm:p-6 lg:p-8 font-sans">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">
          Gestion des Formulaires
        </h1>
        <p className="text-gray-500 mt-1">
          Créez, personnalisez et analysez des formulaires pour toutes vos
          interactions.
        </p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Colonne de Gauche : Formulaire de Création */}
        <aside className="lg:col-span-1">
          <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200 sticky top-6">
            <h2 className="text-lg font-semibold text-gray-700 mb-4">
              Créer un nouveau formulaire
            </h2>
            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label
                  htmlFor="name"
                  className="block text-sm font-medium text-gray-600 mb-1"
                >
                  Nom du formulaire
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  placeholder="Ex: Formulaire de contact"
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-green-500 focus:outline-none"
                  required
                />
              </div>
              <div>
                <label
                  htmlFor="description"
                  className="block text-sm font-medium text-gray-600 mb-1"
                >
                  Description
                </label>
                <textarea
                  id="description"
                  name="description"
                  placeholder="A quoi servira ce formulaire ?"
                  rows={4}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-green-500 focus:outline-none"
                />
              </div>
              <p className="text-xs text-gray-400 pt-2">
                Après la création, vous pourrez ajouter des champs personnalisés
                (texte, email, listes, etc.).
              </p>
              <button
                type="submit"
                className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors shadow font-semibold"
              >
                <Plus size={18} />
                Créer et Personnaliser
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
                  placeholder="Rechercher un formulaire..."
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
                    <th className="px-6 py-3 text-left">Nom</th>
                    <th className="px-6 py-3 text-left">Champs</th>
                    <th className="px-6 py-3 text-center">Soumissions</th>
                    <th className="px-6 py-3 text-left">Créé le</th>
                    <th className="px-6 py-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {forms.length > 0 ? (
                    forms.map((form) => (
                      <tr
                        key={form.id}
                        className="hover:bg-gray-50/50 transition-colors"
                      >
                        <td className="px-6 py-4">
                          <p className="font-semibold text-gray-800">
                            {form.name}
                          </p>
                          <p className="text-gray-500 text-xs truncate max-w-xs">
                            {form.description}
                          </p>
                        </td>
                        <td className="px-6 py-4">
                          {/* Surprise ! Un affichage riche des champs */}
                          <div className="flex flex-wrap gap-1">
                            {form.fields.map((field) => (
                              <span
                                key={field.type}
                                className="inline-flex items-center gap-1 text-xs bg-gray-100 text-gray-700 px-2 py-0.5 rounded-full"
                              >
                                {field.type}{" "}
                                <span className="font-bold">{field.count}</span>
                              </span>
                            ))}
                          </div>
                        </td>
                        <td className="px-6 py-4 text-center font-mono text-gray-700">
                          {form.submissions}
                        </td>
                        <td className="px-6 py-4 text-gray-500">
                          {form.createdAt}
                        </td>
                        <td className="px-6 py-4 text-right">
                          <div className="flex justify-end gap-2">
                            <button className="p-3 text-blue-600 rounded-full transition-colors duration-200 hover:bg-blue-100 hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-200">
                              <Edit2 size={16} />
                            </button>
                            <button className="p-3 text-red-600 rounded-full transition-colors duration-200 hover:bg-blue-100 hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-200">
                              <Trash2 size={16} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={5} className="text-center py-20 px-6">
                        <div className="mx-auto w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                          <FileText size={48} className="text-gray-400" />
                        </div>
                        <h3 className="font-semibold text-lg text-gray-700">
                          Aucun formulaire pour l'instant
                        </h3>
                        <p className="text-gray-500 text-sm mt-1">
                          Commencez par créer votre premier formulaire en
                          utilisant le panneau de gauche.
                        </p>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            <div className="p-4 flex justify-center items-center gap-4 border-t border-gray-200">
              <div className="flex gap-2">
                <button className="w-8 h-8 border rounded-full flex items-center justify-center text-gray-500 hover:bg-gray-100">
                  <ChevronLeft size={16} />
                </button>
                <div className="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center font-bold text-sm">
                  1
                </div>
                <button className="w-8 h-8 border rounded-full flex items-center justify-center text-gray-500 hover:bg-gray-100">
                  <ChevronRight size={16} />
                </button>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default FormListPage;
