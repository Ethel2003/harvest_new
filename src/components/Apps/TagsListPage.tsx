import React, { useState } from "react";
import {
  Tag,
  Plus,
  Search,
  ChevronLeft,
  ChevronRight,
  Edit2,
  Trash2,
} from "lucide-react";

/**
 * Page de gestion complète pour les Tags.
 * Structure : formulaire à gauche, liste à droite.
 */
const TagsListPage: React.FC = () => {
  const [tags, setTags] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState("");

  // Handlers d'action pour éviter l'erreur de compilation
  const handleEdit = (tag: any) => {
    alert(`Édition du tag : ${tag.name}`);
  };
  const handleDelete = (tag: any) => {
    alert(`Suppression du tag : ${tag.name}`);
  };

  const handleCreate = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const newTag = {
      id: Date.now(),
      name: formData.get("name"),
      description: formData.get("description"),
      createdAt: new Date().toLocaleDateString("fr-FR"),
    };
    setTags((prev) => [...prev, newTag]);
    e.currentTarget.reset();
  };

  return (
    <div className="min-h-screen bg-[#F8F9FA] p-4 sm:p-6 lg:p-8 font-sans">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Gestion des Tags</h1>
        <p className="text-gray-500 mt-1">
          Créez et organisez vos tags pour catégoriser membres et contenus.
        </p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Colonne de Gauche : Formulaire de Création */}
        <aside className="lg:col-span-1">
          <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200 sticky top-6">
            <h2 className="text-lg font-semibold text-gray-700 mb-4">
              Ajouter un tag
            </h2>
            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label
                  htmlFor="name"
                  className="block text-sm font-medium text-gray-600 mb-1"
                >
                  Nom du tag
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  placeholder="Ex: VIP, Nouveau membre, Donateur..."
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-green-500 focus:outline-none"
                  required
                />
              </div>
              <div>
                <label
                  htmlFor="description"
                  className="block text-sm font-medium text-gray-600 mb-1"
                >
                  Description (optionnel)
                </label>
                <textarea
                  id="description"
                  name="description"
                  placeholder="A quoi sert ce tag ?"
                  rows={4}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-green-500 focus:outline-none"
                />
              </div>
              <button
                type="submit"
                className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors shadow font-semibold"
              >
                <Plus size={18} />
                Créer
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
                  placeholder="Rechercher un tag..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
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
                    <th className="px-6 py-3 text-left">Description</th>
                    <th className="px-6 py-3 text-left">Date de création</th>
                    <th className="px-6 py-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {tags.length > 0 ? (
                    tags.map((tag) => (
                      <tr key={tag.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 font-medium text-gray-800">
                          <span className="inline-block px-2 py-1 bg-gray-200 text-gray-800 rounded-md text-xs">
                            {tag.name}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-gray-600">
                          {tag.description}
                        </td>
                        <td className="px-6 py-4 text-gray-500">
                          {tag.createdAt}
                        </td>
                        <td className="px-6 py-4 text-right">
                          <div className="flex justify-end items-center gap-1">
                            <button
                              className="p-3 text-blue-600 rounded-full transition-colors duration-200 hover:bg-blue-100 hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-200"
                              aria-label={`Modifier le tag ${tag.name}`}
                              onClick={() => handleEdit(tag)}
                            >
                              <Edit2 size={16} />
                            </button>
                            <button
                              className="p-3 text-red-600 rounded-full transition-colors duration-200 hover:bg-red-100 hover:text-red-600 focus:outline-none focus:ring-2 focus:ring-red-200"
                              aria-label={`Supprimer le tag ${tag.name}`}
                              onClick={() => handleDelete(tag)}
                            >
                              <Trash2 size={16} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={4} className="text-center py-16 px-6">
                        <div className="mx-auto w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                          <Tag size={40} className="text-gray-400" />
                        </div>
                        <h3 className="font-semibold text-gray-700">
                          Aucun tag trouvé
                        </h3>
                        <p className="text-gray-500 text-xs mt-1">
                          Créez votre premier tag en utilisant le formulaire à
                          gauche.
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

export default TagsListPage;
