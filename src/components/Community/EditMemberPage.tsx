import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, Upload } from "lucide-react";
import { MemberType } from "../../types"; // Assurez-vous que ce chemin est correct

// --- COPIE COMPLÈTE DE LA FONCTION DE GÉNÉRATION ---
// Cette fonction est maintenant la même que dans MembersList.tsx
const generateMockMembers = (count: number): MemberType[] => {
  const members: MemberType[] = [];
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
      // Ajout des champs manquants pour correspondre au formulaire
      genre: i % 2 === 0 ? "femme" : "homme",
      dateNaissance: `199${i % 10}-0${(i % 9) + 1}-0${(i % 9) + 1}`,
      nationalite: "Française",
      profession: "Développeur",
      situationMatrimoniale: i % 2 === 0 ? "celibataire" : "marie",
      ville: "Paris",
      adresse: `Rue de l'exemple, ${i}`,
    });
  }
  return members;
};

// On crée la liste qui sera utilisée pour la recherche
const MOCK_MEMBERS = generateMockMembers(652);

const EditMemberPage: React.FC = () => {
  const navigate = useNavigate();
  const { memberId } = useParams<{ memberId: string }>();

  const [formData, setFormData] = useState<Partial<MemberType>>({});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (memberId) {
      const memberToEdit = MOCK_MEMBERS.find((m) => m.id === memberId);
      if (memberToEdit) {
        setFormData(memberToEdit);
      } else {
        alert("Membre non trouvé !");
        navigate("/community");
      }
      setIsLoading(false);
    }
  }, [memberId, navigate]);

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleRadioChange = (
    name: string,
    value: "homme" | "femme" | "celibataire" | "marie"
  ) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log(`Données sauvegardées pour le membre ${memberId}:`, formData);
    alert("Modifications enregistrées !");
    navigate("/community");
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        Chargement des données du membre...
      </div>
    );
  }

  return (
    <div className="bg-gray-100 min-h-screen">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <h1 className="text-xl font-semibold text-gray-900">
              Modifier les infos du membre
            </h1>
            <button
              onClick={() => navigate("/community")}
              className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 transition-colors"
            >
              <ArrowLeft size={16} className="mr-2" /> Retour
            </button>
          </div>
        </div>
      </div>

      {/* Formulaire complet */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <form
          onSubmit={handleSubmit}
          className="bg-white rounded-lg shadow-sm border border-gray-200"
        >
          <div className="p-8">
            <div className="space-y-8">
              {/* Ligne Nom et Prénom */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <label
                    htmlFor="name"
                    className="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Nom <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name || ""}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    required
                  />
                </div>
                <div>
                  <label
                    htmlFor="firstName"
                    className="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Prénom(s) <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    id="firstName"
                    name="firstName"
                    value={formData.firstName || ""}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                    required
                  />
                </div>
              </div>

              {/* Ligne Genre et Date de naissance */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-4">
                    Genre <span className="text-red-500">*</span>
                  </label>
                  <div className="flex space-x-6">
                    <label className="flex items-center cursor-pointer">
                      <input
                        type="radio"
                        name="genre"
                        value="homme"
                        checked={formData.genre === "homme"}
                        onChange={() => handleRadioChange("genre", "homme")}
                        className="h-4 w-4 text-green-600"
                      />
                      <span className="ml-2 text-sm text-gray-700">Homme</span>
                    </label>
                    <label className="flex items-center cursor-pointer">
                      <input
                        type="radio"
                        name="genre"
                        value="femme"
                        checked={formData.genre === "femme"}
                        onChange={() => handleRadioChange("genre", "femme")}
                        className="h-4 w-4 text-green-600"
                      />
                      <span className="ml-2 text-sm text-gray-700">Femme</span>
                    </label>
                  </div>
                </div>
                <div>
                  <label
                    htmlFor="dateNaissance"
                    className="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Date de naissance
                  </label>
                  <input
                    type="date"
                    id="dateNaissance"
                    name="dateNaissance"
                    value={formData.dateNaissance || ""}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
              </div>

              {/* Ligne Nationalité et Profession */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <label
                    htmlFor="nationalite"
                    className="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Nationalité
                  </label>
                  <input
                    type="text"
                    id="nationalite"
                    name="nationalite"
                    value={formData.nationalite || ""}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
                <div>
                  <label
                    htmlFor="profession"
                    className="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Profession
                  </label>
                  <input
                    type="text"
                    id="profession"
                    name="profession"
                    value={formData.profession || ""}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
              </div>

              {/* Ligne Situation matrimoniale et Téléphone */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-4">
                    Situation matrimoniale
                  </label>
                  <div className="flex space-x-6">
                    <label className="flex items-center cursor-pointer">
                      <input
                        type="radio"
                        name="situationMatrimoniale"
                        value="celibataire"
                        checked={
                          formData.situationMatrimoniale === "celibataire"
                        }
                        onChange={() =>
                          handleRadioChange(
                            "situationMatrimoniale",
                            "celibataire"
                          )
                        }
                        className="h-4 w-4 text-green-600"
                      />
                      <span className="ml-2 text-sm text-gray-700">
                        Célibataire
                      </span>
                    </label>
                    <label className="flex items-center cursor-pointer">
                      <input
                        type="radio"
                        name="situationMatrimoniale"
                        value="marie"
                        checked={formData.situationMatrimoniale === "marie"}
                        onChange={() =>
                          handleRadioChange("situationMatrimoniale", "marie")
                        }
                        className="h-4 w-4 text-green-600"
                      />
                      <span className="ml-2 text-sm text-gray-700">
                        Marié(e)
                      </span>
                    </label>
                  </div>
                </div>
                <div>
                  <label
                    htmlFor="phone"
                    className="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Téléphone
                  </label>
                  <input
                    type="tel"
                    id="phone"
                    name="phone"
                    value={formData.phone || ""}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
              </div>

              {/* Ligne Email et Ville */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <label
                    htmlFor="email"
                    className="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email || ""}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
                <div>
                  <label
                    htmlFor="ville"
                    className="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Ville
                  </label>
                  <input
                    type="text"
                    id="ville"
                    name="ville"
                    value={formData.ville || ""}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
              </div>

              {/* Ligne Adresse */}
              <div>
                <label
                  htmlFor="adresse"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Adresse
                </label>
                <textarea
                  id="adresse"
                  name="adresse"
                  value={formData.adresse || ""}
                  onChange={handleInputChange}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg resize-none"
                />
              </div>

              {/* Bouton de soumission */}
              <div className="flex justify-end pt-6">
                <button
                  type="submit"
                  className="px-8 py-2 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700"
                >
                  Enregistrer les modifications
                </button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EditMemberPage;
