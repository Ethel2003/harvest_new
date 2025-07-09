import React, { useState, useMemo, useEffect } from "react";
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
  Loader2,
  Filter,
  RefreshCw,
} from "lucide-react";
import AddMemberForm from "./AddMemberForm";
import MemberDetailsPage from "./MemberDetailsPage";
import type { MemberType, PaginationMeta } from "../../types";
import { memberService, groupService, tagService, etapeService } from "../../services";

// --- TYPES ET INTERFACES ---
interface FilterState {
  groupes: number[];
  etapes: number[];
  tags: number[];
  search: string;
}

interface LoadingState {
  members: boolean;
  groups: boolean;
  etapes: boolean;
  tags: boolean;
}

// --- COMPOSANT PRINCIPAL ---
const MembersList = () => {
  // États de base
  const [searchTerm, setSearchTerm] = useState("");
  const [resultsPerPage, setResultsPerPage] = useState(10);
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedMembers, setSelectedMembers] = useState<string[]>([]);

  // États pour les filtres
  const [filters, setFilters] = useState<FilterState>({
    groupes: [],
    etapes: [],
    tags: [],
    search: "",
  });

  // États pour les données
  const [members, setMembers] = useState<MemberType[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta>({
    currentPage: 1,
    totalPages: 1,
    totalItems: 0,
    itemsPerPage: 10,
    hasNext: false,
    hasPrevious: false,
  });
  const [groups, setGroups] = useState<any[]>([]);
  const [etapes, setEtapes] = useState<any[]>([]);
  const [tags, setTags] = useState<any[]>([]);

  // États de chargement
  const [loading, setLoading] = useState<LoadingState>({
    members: false,
    groups: false,
    etapes: false,
    tags: false,
  });

  // États pour les menus
  const [showActionDropdown, setShowActionDropdown] = useState(false);
  const [showMemberActions, setShowMemberActions] = useState<string | null>(null);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedMember, setSelectedMember] = useState<MemberType | null>(null);

  // États pour les filtres UI
  const [groupSearchTerm, setGroupSearchTerm] = useState("");
  const [etapeSearchTerm, setEtapeSearchTerm] = useState("");
  const [tagSearchTerm, setTagSearchTerm] = useState("");

  // --- EFFETS ---
  useEffect(() => {
    loadInitialData();
  }, []);

  useEffect(() => {
    loadMembers();
  }, [filters, currentPage, resultsPerPage]);

  // --- FONCTIONS DE CHARGEMENT ---
  const loadInitialData = async () => {
    try {
      setLoading(prev => ({ ...prev, groups: true, etapes: true, tags: true }));
      
      const [groupsResponse, etapesResponse, tagsResponse] = await Promise.all([
        groupService.getGroups(),
        etapeService.getEtapes(),
        tagService.getTags()
      ]);
      console.log("groupsResponse", groupsResponse);
      console.log("etapesResponse", etapesResponse);
      console.log("tagsResponse", tagsResponse);
     
      // Accéder aux données selon la structure de réponse
      setGroups(groupsResponse.data?.data?.groupes || []);
      setEtapes(etapesResponse.data?.results || []);
      setTags(tagsResponse.data?.data || []);
    } catch (error) {
      console.error("Erreur lors du chargement des données initiales:", error);
    } finally {
      setLoading(prev => ({ ...prev, groups: false, etapes: false, tags: false }));
    }
  };

  const loadMembers = async () => {
    try {
      setLoading(prev => ({ ...prev, members: true }));
      
      // Utiliser l'endpoint de filtres combinés si des filtres sont actifs
      if (filters.groupes.length > 0 || filters.etapes.length > 0 || filters.tags.length > 0 || filters.search) {
        const response = await memberService.getMembersWithCombinedFilters({
          ...filters,
          page: currentPage,
          page_size: resultsPerPage,
        });
        setMembers(response.data);
        setPagination(response.pagination);
      } else {
        // Utiliser l'endpoint de base avec pagination
        const response = await memberService.getMembers({
          search: filters.search,
          page: currentPage,
          page_size: resultsPerPage,
        });
        setMembers(response.data);
        setPagination(response.pagination);
      }
    } catch (error) {
      console.error("Erreur lors du chargement des membres:", error);
      setMembers([]);
      setPagination({
        currentPage: 1,
        totalPages: 1,
        totalItems: 0,
        itemsPerPage: resultsPerPage,
        hasNext: false,
        hasPrevious: false,
      });
    } finally {
      setLoading(prev => ({ ...prev, members: false }));
    }
  };

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
      e.target.checked ? members.map((m) => m.id.toString()) : []
    );
  };

  const handleFilterChange = (filterType: keyof FilterState, value: any) => {
    setFilters(prev => ({ ...prev, [filterType]: value }));
    setCurrentPage(1); // Reset à la première page lors d'un changement de filtre
  };

  const handleSearchChange = (value: string) => {
    setSearchTerm(value);
    handleFilterChange('search', value);
  };

  const toggleGroupFilter = (groupId: number) => {
    const newGroups = filters.groupes.includes(groupId)
      ? filters.groupes.filter(id => id !== groupId)
      : [...filters.groupes, groupId];
    handleFilterChange('groupes', newGroups);
  };

  const toggleEtapeFilter = (etapeId: number) => {
    const newEtapes = filters.etapes.includes(etapeId)
      ? filters.etapes.filter(id => id !== etapeId)
      : [...filters.etapes, etapeId];
    handleFilterChange('etapes', newEtapes);
  };

  const toggleTagFilter = (tagId: number) => {
    const newTags = filters.tags.includes(tagId)
      ? filters.tags.filter(id => id !== tagId)
      : [...filters.tags, tagId];
    handleFilterChange('tags', newTags);
  };

  const clearAllFilters = () => {
    setFilters({
      groupes: [],
      etapes: [],
      tags: [],
      search: "",
    });
    setSearchTerm("");
    setGroupSearchTerm("");
    setEtapeSearchTerm("");
    setTagSearchTerm("");
    setCurrentPage(1);
  };

  const refreshData = () => {
    loadMembers();
  };

  const handlePageChange = (newPage: number) => {
    setCurrentPage(newPage);
  };

  const handlePageSizeChange = (newSize: number) => {
    setResultsPerPage(newSize);
    setCurrentPage(1);
  };

  // --- CALCULS ---
  const isAllSelected = members.length > 0 && selectedMembers.length === members.length;

  const hasActiveFilters = filters.groupes.length > 0 || filters.etapes.length > 0 || filters.tags.length > 0 || filters.search;

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
    <div className="min-h-screen bg-[#F8F9FA] font-sans">
      <main className="p-4 sm:p-6 lg:p-8">
        <div className="flex flex-col lg:flex-row gap-6">
          {/* COLONNE GAUCHE */}
          <div className="flex-1">
            <div className="flex justify-between items-center mb-6">
              <div className="flex items-center gap-3">
                <button 
                  onClick={refreshData}
                  disabled={loading.members}
                  className="flex items-center gap-2 px-4 py-2 bg-white text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors shadow-sm font-medium disabled:opacity-50"
                >
                  {loading.members ? (
                    <Loader2 size={18} className="animate-spin" />
                  ) : (
                    <RefreshCw size={18} />
                  )}
                  <span>Actualiser</span>
                </button>
                
                {hasActiveFilters && (
                  <button
                    onClick={clearAllFilters}
                    className="flex items-center gap-2 px-4 py-2 bg-red-50 text-red-600 border border-red-200 rounded-lg hover:bg-red-100 transition-colors shadow-sm font-medium"
                  >
                    <X size={18} />
                    <span>Effacer les filtres</span>
                  </button>
                )}
              </div>
              
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
                    placeholder="Rechercher des membres..."
                    value={searchTerm}
                    onChange={(e) => handleSearchChange(e.target.value)}
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
                      handlePageSizeChange(Number(e.target.value));
                    }}
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#76C12C] focus:outline-none bg-white"
                  >
                    <option value={10}>10 résultats par page</option>
                    <option value={25}>25 résultats par page</option>
                    <option value={50}>50 résultats par page</option>
                  </select>
                </div>
              </div>

              {/* En-têtes du tableau */}
              <div className="px-4 py-3 flex items-center text-xs font-semibold text-gray-500 uppercase bg-gray-50 border-b border-gray-200">
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

              {/* Liste des membres */}
              <div className="divide-y divide-gray-200">
                {loading.members ? (
                  <div className="p-8 text-center">
                    <Loader2 size={32} className="animate-spin mx-auto mb-4 text-[#76C12C]" />
                    <p className="text-gray-600">Chargement des membres...</p>
                  </div>
                ) : members.length === 0 ? (
                  <div className="p-8 text-center">
                    <Users size={48} className="mx-auto mb-4 text-gray-400" />
                    <p className="text-gray-600">
                      {hasActiveFilters 
                        ? "Aucun membre trouvé avec les filtres actuels" 
                        : "Aucun membre trouvé"
                      }
                    </p>
                    {hasActiveFilters && (
                      <button
                        onClick={clearAllFilters}
                        className="mt-2 text-[#76C12C] hover:underline"
                      >
                        Effacer les filtres
                      </button>
                    )}
                  </div>
                ) : (
                  members.map((member) => (
                    <div
                      key={member.id}
                      className={`px-4 py-2 flex items-center transition-colors ${
                        selectedMembers.includes(member.id.toString())
                          ? "bg-green-50"
                          : "hover:bg-gray-50"
                      }`}
                    >
                      <div className="w-10">
                        <input
                          type="checkbox"
                          className="h-5 w-5 rounded-full border-2 border-gray-300 text-[#76C12C] focus:ring-[#76C12C] appearance-none checked:bg-[#76C12C] checked:border-[#76C12C] transition-all"
                          checked={selectedMembers.includes(member.id.toString())}
                          onChange={() => handleSelectMember(member.id.toString())}
                        />
                      </div>
                      <div className="flex-1 flex items-center gap-3">
                        <div className="bg-[#76C12C] w-9 h-9 rounded-full flex items-center justify-center text-white font-bold text-sm flex-shrink-0">
                          {member.nom?.[0]}{member.prenom?.[0]}
                        </div>
                        <div>
                          <div className="font-bold text-sm text-gray-800">
                            {member.nom}{" "}
                            <span className="font-normal">
                              {member.prenom}
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="w-40 text-sm text-gray-600 hidden md:block">
                        {member.telephone}
                      </div>
                      <div className="w-64 text-sm text-gray-600 hidden sm:block">
                        {member.email}
                      </div>
                      <div className="w-12 flex justify-center">
                        <div className="relative">
                          <button
                            onClick={() =>
                              setShowMemberActions(
                                showMemberActions === member.id.toString() ? null : member.id.toString()
                              )
                            }
                            className="p-2 rounded-full hover:bg-gray-200"
                          >
                            <MoreVertical size={18} className="text-gray-500" />
                          </button>
                          {showMemberActions === member.id.toString() && (
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
                  ))
                )}
              </div>

              {/* Pagination */}
              {members.length > 0 && (
                <div className="p-4 flex justify-between items-center border-t border-gray-200">
                  <span className="text-sm text-gray-600">
                    Affiche {members.length} résultats
                  </span>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handlePageChange(Math.max(1, currentPage - 1))}
                      disabled={currentPage === 1}
                      className="p-2 rounded-full hover:bg-gray-200 disabled:opacity-50 flex items-center justify-center w-8 h-8"
                    >
                      <ChevronLeft size={20} />
                    </button>
                    <span className="text-sm text-gray-600">
                      Page {currentPage}
                    </span>
                    <button
                      onClick={() => handlePageChange(currentPage + 1)}
                      disabled={pagination.hasNext === false}
                      className="p-2 rounded-full hover:bg-gray-200 disabled:opacity-50 flex items-center justify-center w-8 h-8"
                    >
                      <ChevronRight size={20} />
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* COLONNE DROITE - FILTRES */}
          <aside className="w-full lg:w-1/4 lg:max-w-xs">
            <div className="space-y-4 sticky top-6">
              {/* Filtre par Groupes */}
              <div className="bg-white rounded-xl shadow-md border border-gray-200">
                <details className="group" open>
                  <summary className="p-4 flex justify-between items-center cursor-pointer list-none">
                    <h3 className="font-semibold text-gray-800 flex items-center gap-2">
                      <Users size={16} />
                      Filtrer par Groupes
                    </h3>
                    {filters.groupes.length > 0 && (
                      <span className="bg-[#76C12C] text-white text-xs px-2 py-1 rounded-full">
                        {filters.groupes.length}
                      </span>
                    )}
                  </summary>
                  <div className="p-4 border-t border-gray-200 max-h-80 overflow-y-auto">
                    {loading.groups ? (
                      <div className="text-center py-4">
                        <Loader2 size={20} className="animate-spin mx-auto text-[#76C12C]" />
                      </div>
                    ) : (
                      <>
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
                          {groups
                            .filter((g) =>
                              g.nom?.toLowerCase().includes(groupSearchTerm.toLowerCase())
                            )
                            .map((group) => (
                              <li key={group.id} className="flex items-center">
                                <input
                                  id={`group-${group.id}`}
                                  type="checkbox"
                                  checked={filters.groupes.includes(group.id)}
                                  onChange={() => toggleGroupFilter(group.id)}
                                  className="h-5 w-5 rounded-full border-2 border-gray-300 text-[#76C12C] focus:ring-[#76C12C] appearance-none checked:bg-[#76C12C] checked:border-[#76C12C] transition-all cursor-pointer"
                                />
                                <label
                                  htmlFor={`group-${group.id}`}
                                  className="ml-3 text-sm text-gray-700 cursor-pointer"
                                >
                                  {group.nom}
                                </label>
                              </li>
                            ))}
                        </ul>
                      </>
                    )}
                  </div>
                </details>
              </div>

              {/* Filtre par Étapes */}
              <div className="bg-white rounded-xl shadow-md border border-gray-200">
                <details className="group">
                  <summary className="p-4 flex justify-between items-center cursor-pointer list-none">
                    <h3 className="font-semibold text-gray-800 flex items-center gap-2">
                      <Check size={16} />
                      Filtrer par Étapes
                    </h3>
                    {filters.etapes.length > 0 && (
                      <span className="bg-[#76C12C] text-white text-xs px-2 py-1 rounded-full">
                        {filters.etapes.length}
                      </span>
                    )}
                  </summary>
                  <div className="p-4 border-t border-gray-200 max-h-80 overflow-y-auto">
                    {loading.etapes ? (
                      <div className="text-center py-4">
                        <Loader2 size={20} className="animate-spin mx-auto text-[#76C12C]" />
                      </div>
                    ) : (
                      <>
                        <div className="relative mb-4">
                          <Search
                            className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                            size={16}
                          />
                          <input
                            type="text"
                            placeholder="Rechercher une étape"
                            value={etapeSearchTerm}
                            onChange={(e) => setEtapeSearchTerm(e.target.value)}
                            className="w-full pl-9 pr-3 py-1.5 border rounded-md text-sm focus:ring-1 focus:ring-green-400 focus:outline-none"
                          />
                        </div>
                        <ul className="space-y-2">
                          {etapes
                            .filter((e) =>
                              e.libelle?.toLowerCase().includes(etapeSearchTerm.toLowerCase())
                            )
                            .map((etape) => (
                              <li key={etape.id} className="flex items-center">
                                <input
                                  id={`etape-${etape.id}`}
                                  type="checkbox"
                                  checked={filters.etapes.includes(etape.id)}
                                  onChange={() => toggleEtapeFilter(etape.id)}
                                  className="h-5 w-5 rounded-full border-2 border-gray-300 text-[#76C12C] focus:ring-[#76C12C] appearance-none checked:bg-[#76C12C] checked:border-[#76C12C] transition-all cursor-pointer"
                                />
                                <label
                                  htmlFor={`etape-${etape.id}`}
                                  className="ml-3 text-sm text-gray-700 cursor-pointer"
                                >
                                  {etape.libelle}
                                </label>
                              </li>
                            ))}
                        </ul>
                      </>
                    )}
                  </div>
                </details>
              </div>

              {/* Filtre par Tags */}
              <div className="bg-white rounded-xl shadow-md border border-gray-200">
                <details className="group">
                  <summary className="p-4 flex justify-between items-center cursor-pointer list-none">
                    <h3 className="font-semibold text-gray-800 flex items-center gap-2">
                      <Tag size={16} />
                      Filtrer par Tags
                    </h3>
                    {filters.tags.length > 0 && (
                      <span className="bg-[#76C12C] text-white text-xs px-2 py-1 rounded-full">
                        {filters.tags.length}
                      </span>
                    )}
                  </summary>
                  <div className="p-4 border-t border-gray-200 max-h-80 overflow-y-auto">
                    {loading.tags ? (
                      <div className="text-center py-4">
                        <Loader2 size={20} className="animate-spin mx-auto text-[#76C12C]" />
                      </div>
                    ) : (
                      <>
                        <div className="relative mb-4">
                          <Search
                            className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                            size={16}
                          />
                          <input
                            type="text"
                            placeholder="Rechercher un tag"
                            value={tagSearchTerm}
                            onChange={(e) => setTagSearchTerm(e.target.value)}
                            className="w-full pl-9 pr-3 py-1.5 border rounded-md text-sm focus:ring-1 focus:ring-green-400 focus:outline-none"
                          />
                        </div>
                        <ul className="space-y-2">
                          {tags
                            .filter((t) =>
                              t.name?.toLowerCase().includes(tagSearchTerm.toLowerCase())
                            )
                            .map((tag) => (
                              <li key={tag.id} className="flex items-center">
                                <input
                                  id={`tag-${tag.id}`}
                                  type="checkbox"
                                  checked={filters.tags.includes(tag.id)}
                                  onChange={() => toggleTagFilter(tag.id)}
                                  className="h-5 w-5 rounded-full border-2 border-gray-300 text-[#76C12C] focus:ring-[#76C12C] appearance-none checked:bg-[#76C12C] checked:border-[#76C12C] transition-all cursor-pointer"
                                />
                                <label
                                  htmlFor={`tag-${tag.id}`}
                                  className="ml-3 text-sm text-gray-700 cursor-pointer"
                                >
                                  {tag.name}
                                </label>
                              </li>
                            ))}
                        </ul>
                      </>
                    )}
                  </div>
                </details>
              </div>
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
