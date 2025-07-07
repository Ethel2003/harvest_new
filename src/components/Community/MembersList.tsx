import React, { useState, useMemo } from "react";
import {
  Search,
  Plus,
  Upload,
  MoreVertical,
  Eye,
  Edit,
  Trash2,
  Tag,
  Users,
  Building,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Check,
  X,
} from "lucide-react";
import AddMemberForm from "./AddMemberForm";
import MemberDetailsPage from "./MemberDetailsPage";
import type { MemberType } from "../../types";

// --- FONCTIONS UTILITAIRES ---
// Pour générer une grande quantité de données fictives
const generateMockMembers = (count: number) => {
  const members = [];
  const lastNames = [
    "ABDOU",
    "MARTIN",
    "BERNARD",
    "THOMAS",
    "PETIT",
    "ROBERT",
    "RICHARD",
    "DURAND",
  ];
  const firstNames = [
    "Naomi",
    "Lucas",
    "Léa",
    "Hugo",
    "Chloé",
    "Louis",
    "Manon",
    "Gabriel",
  ];
  const groups = [
    "FR Parakletos",
    "FR Agneau de Dieu",
    "FR Le Véritable",
    "FR Oméga",
    "FR Admirable",
    "FR Le Fidèle",
    "FR Amen",
    "FR Lion de la tribu de Juda",
    "Groupe Test",
    "FR Le Rocher",
    "FR Prince de paix",
    "FR Fils de David",
    "FR Alpha",
  ];
  const colors = [
    "bg-pink-400",
    "bg-teal-400",
    "bg-gray-400",
    "bg-blue-400",
    "bg-green-400",
    "bg-orange-400",
  ];

  for (let i = 1; i <= count; i++) {
    const lastName = lastNames[i % lastNames.length] + (i > 10 ? ` ${i}` : "");
    const firstName = firstNames[i % firstNames.length];
    members.push({
      id: i.toString(),
      name: lastName,
      firstName: firstName,
      email: `${firstName.toLowerCase()}.${lastName
        .toLowerCase()
        .replace(" ", "")}@example.com`,
      phone: `+33 6 ${String(i).padStart(2, "0")} ${String(i + 1).padStart(
        2,
        "0"
      )} ${String(i + 2).padStart(2, "0")} ${String(i + 3).padStart(2, "0")}`,
      group: groups[i % groups.length],
      stage: "Membre",
      tags: [],
      initials: `${lastName[0]}${firstName[0]}`,
      color: colors[i % colors.length],
    });
  }
  return members;
};
// Logique pour générer les boutons de pagination
const generatePaginationItems = (currentPage: number, totalPages: number) => {
  const delta = 2;
  const range = [];
  for (
    let i = Math.max(2, currentPage - delta);
    i <= Math.min(totalPages - 1, currentPage + delta);
    i++
  ) {
    range.push(i);
  }
  if (currentPage - delta > 2) {
    range.unshift("...");
  }
  if (currentPage + delta < totalPages - 1) {
    range.push("...");
  }
  range.unshift(1);
  if (totalPages > 1) {
    range.push(totalPages);
  }
  return [...new Set(range)]; // Enlève les doublons si totalPages est petit
};

// --- COMPOSANT PRINCIPAL ---

// Définition du type pour un membre

const MembersList = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [resultsPerPage, setResultsPerPage] = useState(10);
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedMembers, setSelectedMembers] = useState<string[]>([]);

  // Filtres
  const [selectedGroups, setSelectedGroups] = useState<string[]>([]);
  const [groupSearchTerm, setGroupSearchTerm] = useState("");

  // Menus
  const [showActionDropdown, setShowActionDropdown] = useState(false);
  const [showMemberActions, setShowMemberActions] = useState<string | null>(
    null
  );

  // --- DONNÉES ---
  const MOCK_MEMBERS = useMemo(() => generateMockMembers(652), []); // Génère 652 membres pour avoir 66 pages
  const MOCK_GROUPS = [
    "FR Parakletos",
    "FR Agneau de Dieu",
    "FR Le Véritable",
    "FR Oméga",
    "FR Admirable",
    "FR Le Fidèle",
    "FR Amen",
    "FR Lion de la tribu de Juda",
    "Groupe Test",
    "FR Le Rocher",
    "FR Prince de paix",
    "FR Fils de David",
    "FR Alpha",
  ];

  // --- LOGIQUE DE FILTRAGE ET PAGINATION ---
  const filteredMembers = useMemo(() => {
    return MOCK_MEMBERS.filter((member) => {
      const searchString =
        `${member.name} ${member.firstName} ${member.email}`.toLowerCase();
      const matchesSearch = searchString.includes(searchTerm.toLowerCase());
      const matchesGroups =
        selectedGroups.length === 0 || selectedGroups.includes(member.group);
      return matchesSearch && matchesGroups;
    });
  }, [searchTerm, selectedGroups, MOCK_MEMBERS]);

  const totalPages = Math.ceil(filteredMembers.length / resultsPerPage);
  const paginatedMembers = useMemo(() => {
    return filteredMembers.slice(
      (currentPage - 1) * resultsPerPage,
      currentPage * resultsPerPage
    );
  }, [filteredMembers, currentPage, resultsPerPage]);

  const paginationItems = generatePaginationItems(currentPage, totalPages);

  // --- HANDLERS ---
  const handleSelectMember = (memberId: string) => {
    setSelectedMembers((prev) =>
      prev.includes(memberId)
        ? prev.filter((id) => id !== memberId)
        : [...prev, memberId]
    );
  };
  const handleSelectAll = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedMembers(
      e.target.checked ? paginatedMembers.map((m) => m.id) : []
    );
  };
  const toggleGroupFilter = (group: string) => {
    setSelectedGroups((prev) =>
      prev.includes(group) ? prev.filter((g) => g !== group) : [...prev, group]
    );
  };

  const isAllSelected =
    paginatedMembers.length > 0 &&
    selectedMembers.length === paginatedMembers.length;

  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedMember, setSelectedMember] = useState<MemberType | null>(null);

  // Si un membre est sélectionné pour voir les détails, on affiche la page de détails
  if (selectedMember) {
    return (
      <MemberDetailsPage
        member={selectedMember}
        onBack={() => setSelectedMember(null)}
      />
    );
  }

  return (
    <div className="min-h-screen bg-[#F8F9FA] font-sans ">
      <main className="p-4 sm:p-6 lg:p-8">
        <div className="flex flex-col lg:flex-row gap-6 ">
          {/* COLONNE GAUCHE */}
          <div className="flex-1 ">
            <div className="flex justify-between items-center mb-6">
              {/* Style du bouton "Importer" mis à jour */}
              <button className="flex items-center gap-2 px-4 py-2 bg-white text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors shadow-sm font-medium">
                <Upload size={18} />
                <span>Importer une liste de Membre</span>
              </button>
              <button
                onClick={() => setShowAddModal(true)}
                className="flex items-center gap-2 px-4 py-2 bg-[#76C12C] text-white rounded-lg hover:bg-[#66a825] transition-colors shadow-sm font-medium"
              >
                <Plus size={18} />
                <span>Ajouter un membre</span>
              </button>
            </div>

            <div className="bg-white rounded-xl shadow-md border border-gray-200">
              <div className="p-4 flex justify-between items-center border-b border-gray-200">
                <div className="relative w-full max-w-sm">
                  <Search
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                    size={18}
                  />
                  <input
                    type="text"
                    placeholder="Filter..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:outline-none"
                  />
                </div>
                <div className="flex items-center gap-4">
                  <div className="relative">
                    <button
                      onClick={() => setShowActionDropdown(!showActionDropdown)}
                      disabled={selectedMembers.length === 0}
                      className="px-4 py-2 bg-[#28A745] text-white rounded-lg flex items-center gap-2 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                    >
                      <span>Action...</span>
                      <ChevronDown size={16} />
                    </button>
                    {showActionDropdown && (
                      <div className="absolute right-0 mt-2 w-56 bg-white rounded-md shadow-lg border z-10">
                        <ul className="py-1 text-sm text-gray-700">
                          <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center gap-3">
                            <Tag size={16} className="text-gray-400" />
                            Associer un tag
                          </li>
                          <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center gap-3">
                            <Check size={16} className="text-gray-400" />
                            Associer une étape
                          </li>
                          <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center gap-3">
                            <Building size={16} className="text-gray-400" />
                            Insérer dans un département
                          </li>
                          <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center gap-3">
                            <Users size={16} className="text-gray-400" />
                            Insérer dans un groupe
                          </li>
                        </ul>
                      </div>
                    )}
                  </div>
                  <select
                    value={resultsPerPage}
                    onChange={(e) => {
                      setResultsPerPage(Number(e.target.value));
                      setCurrentPage(1);
                    }}
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:outline-none bg-white"
                  >
                    <option value="10">10 results per page</option>
                    <option value="25">25 results per page</option>
                    <option value="50">50 results per page</option>
                  </select>
                </div>
              </div>

              <div className="  px-4 py-3 flex items-center text-xs font-semibold text-gray-500 uppercase bg-gray-50 border-b border-gray-200">
                <div className="w-10">
                  <input
                    type="checkbox"
                    className="h-5 w-5 rounded-full border-2 border-gray-300 text-[#76C12C] focus:ring-[#76C12C] appearance-none checked:bg-[#76C12C] checked:border-[#76C12C] transition-all"
                    onChange={handleSelectAll}
                    checked={isAllSelected}
                  />
                </div>
                <div className="flex-1">Nom & Prénom</div>
                <div className="w-40 hidden md:block">Téléphone</div>
                <div className="w-64 hidden sm:block">Email</div>
                <div className="w-12"></div>
              </div>

              <div className="divide-y divide-gray-200">
                {paginatedMembers.map((member) => (
                  <div
                    key={member.id}
                    className={`px-4 py-2 flex items-center transition-colors ${
                      selectedMembers.includes(member.id)
                        ? "bg-green-50"
                        : "hover:bg-gray-50"
                    }`}
                  >
                    <div className="w-10">
                      <input
                        type="checkbox"
                        className="h-5 w-5 rounded-full border-2 border-gray-300 text-[#76C12C] focus:ring-[#76C12C] appearance-none checked:bg-[#76C12C] checked:border-[#76C12C] transition-all"
                        checked={selectedMembers.includes(member.id)}
                        onChange={() => handleSelectMember(member.id)}
                      />
                    </div>
                    <div className="flex-1 flex items-center gap-3">
                      <div
                        className={`${member.color} w-9 h-9 rounded-full flex items-center justify-center text-white font-bold text-sm flex-shrink-0`}
                      >
                        {member.initials}
                      </div>
                      <div>
                        <div className="font-bold text-sm text-gray-800">
                          {member.name}{" "}
                          <span className="font-normal">
                            {member.firstName}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="w-40 text-sm text-gray-600 hidden md:block">
                      {member.phone}
                    </div>
                    <div className="w-64 text-sm text-gray-600 hidden sm:block">
                      {member.email}
                    </div>
                    <div className="w-12 flex justify-center">
                      <div className="relative">
                        <button
                          onClick={() =>
                            setShowMemberActions(
                              showMemberActions === member.id ? null : member.id
                            )
                          }
                          className="p-2 rounded-full hover:bg-gray-200"
                        >
                          <MoreVertical size={18} className="text-gray-500" />
                        </button>
                        {showMemberActions === member.id && (
                          <div className="absolute right-0 mt-2 w-56 bg-white rounded-md shadow-lg border z-10">
                            <ul className="py-1 text-sm text-gray-700 divide-y divide-gray-100">
                              <li
                                className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-start gap-3"
                                onClick={() => {
                                  setSelectedMember(member);
                                  setShowMemberActions(null);
                                }}
                              >
                                <Eye size={16} className="text-green-500 mt-1" />
                                <div>
                                  <p>Voir</p>
                                  <p className="text-xs text-gray-400">
                                    Voir les détails du membre
                                  </p>
                                </div>
                              </li>
                              <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-start gap-3">
                                <Edit
                                  size={16}
                                  className="text-blue-500 mt-1"
                                />
                                <div>
                                  <p>Modifier</p>
                                  <p className="text-xs text-gray-400">
                                    Modifier les détails du membre
                                  </p>
                                </div>
                              </li>
                              <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-start gap-3 text-red-600">
                                <Trash2 size={16} className="mt-1" />
                                <div>
                                  <p>Supprimer</p>
                                  <p className="text-xs text-gray-400">
                                    Supprimer le membre de la liste
                                  </p>
                                </div>
                              </li>
                            </ul>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Pagination Améliorée */}
              {totalPages > 0 && (
                <div className="p-4 flex justify-between items-center border-t border-gray-200">
                  <span className="text-sm text-gray-600">
                    Affiche {paginatedMembers.length} sur{" "}
                    {filteredMembers.length} résultats
                  </span>
                  <div className="flex items-center gap-1">
                    <button
                      onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                      disabled={currentPage === 1}
                      className="p-2 rounded-full hover:bg-gray-200 disabled:opacity-50 flex items-center justify-center w-8 h-8"
                    >
                      <ChevronLeft size={20} />
                    </button>
                    {paginationItems.map((item, index) =>
                      typeof item === "number" ? (
                        <button
                          key={index}
                          onClick={() => setCurrentPage(item)}
                          className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-colors ${
                            currentPage === item
                              ? "bg-[#76C12C] text-white"
                              : "hover:bg-gray-200"
                          }`}
                        >
                          {item}
                        </button>
                      ) : (
                        <span key={index} className="px-2 text-gray-500">
                          ...
                        </span>
                      )
                    )}
                    <button
                      onClick={() =>
                        setCurrentPage((p) => Math.min(totalPages, p + 1))
                      }
                      disabled={currentPage === totalPages}
                      className="p-2 rounded-full hover:bg-gray-200 disabled:opacity-50 flex items-center justify-center w-8 h-8"
                    >
                      <ChevronRight size={20} />
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* COLONNE DROITE */}
          <aside className="w-full lg:w-1/4 lg:max-w-xs ">
            <div className="space-y-4 sticky top-6">
              {/* Filtre par Groupes Amélioré */}
              <div className="bg-white rounded-xl shadow-md border border-gray-200">
                <details className="group" open>
                  <summary className="p-4 flex justify-between items-center cursor-pointer list-none">
                    <h3 className="font-semibold text-gray-800">
                      Filtrer par Groupes
                    </h3>
                    <button
                      onClick={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        setSelectedGroups([]);
                        setGroupSearchTerm("");
                      }}
                      className="p-1 rounded-full hover:bg-gray-200"
                    >
                      <X size={16} className="text-gray-400" />
                    </button>
                  </summary>
                  <div className="p-4 border-t border-gray-200 max-h-80 overflow-y-auto">
                    <div className="relative mb-4">
                      <Search
                        className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                        size={16}
                      />
                      <input
                        type="text"
                        placeholder="Rechercher un groupe"
                        value={groupSearchTerm}
                        onChange={(e) => setGroupSearchTerm(e.target.value)}
                        className="w-full pl-9 pr-3 py-1.5 border rounded-md text-sm focus:ring-1 focus:ring-green-400 focus:outline-none"
                      />
                    </div>
                    <ul className="space-y-2">
                      {MOCK_GROUPS.filter((g) =>
                        g.toLowerCase().includes(groupSearchTerm.toLowerCase())
                      ).map((item) => (
                        <li key={item} className="flex items-center">
                          <input
                            id={`group-${item}`}
                            type="checkbox"
                            checked={selectedGroups.includes(item)}
                            onChange={() => toggleGroupFilter(item)}
                            className="
                              h-5 w-5
                              rounded-full
                              border-2 border-gray-300
                              text-[#76C12C]
                              focus:ring-[#76C12C]
                              appearance-none
                              checked:bg-[#76C12C]
                              checked:border-[#76C12C]
                              transition-all
                              cursor-pointer
                            "
                          />
                          <label
                            htmlFor={`group-${item}`}
                            className="ml-3 text-sm text-gray-700 cursor-pointer"
                          >
                            {item}
                          </label>
                        </li>
                      ))}
                    </ul>
                  </div>
                </details>
              </div>

              {/* Autres filtres (structure simple) */}
              {["Etapes", "Tags"].map((filterType) => (
                <div
                  key={filterType}
                  className="bg-white rounded-xl shadow-md border border-gray-200"
                >
                  <details className="group">
                    <summary className="p-4 flex justify-between items-center cursor-pointer list-none">
                      <h3 className="font-semibold text-gray-800">
                        Filtrer par {filterType}
                      </h3>
                      <Plus
                        size={20}
                        className="text-gray-500 group-open:rotate-45 transition-transform"
                      />
                    </summary>
                    <div className="p-4 border-t border-gray-200">
                      <p className="text-sm text-gray-500">
                        Contenu du filtre à implémenter.
                      </p>
                    </div>
                  </details>
                </div>
              ))}
            </div>
          </aside>
        </div>
      </main>

      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <AddMemberForm onClose={() => setShowAddModal(false)} />
        </div>
      )}
    </div>
  );
};

export default MembersList;
