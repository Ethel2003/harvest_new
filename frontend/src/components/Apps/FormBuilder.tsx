import React, { useState, useMemo } from "react";
import {
  FileText,
  ClipboardList,
  BookMarked,
  Users,
  Building,
  Tag,
  ChevronLeft,
  ChevronRight,
  Plus,
  Eye,
  Edit,
  Trash2,
  Save,
} from "lucide-react";

// --- TYPES (Tirés de votre code de base) ---
interface FormField {
  id: string;
  type: "text" | "email" | "select" | "checkbox" | "textarea";
  label: string;
  required: boolean;
  options?: string[];
}
interface Form {
  id: string;
  name: string;
  description: string;
  fields: FormField[];
  createdAt: string;
  submissions: number;
}

// --- CONFIGURATION CENTRALE DES APPLICATIONS ---
// Ceci est le "cerveau" qui rend la page dynamique.
const APPS_CONFIG = [
  {
    id: "formulaire",
    title: "FORMULAIRE",
    subtitle: "Gestion de Formulaire",
    icon: FileText,
    placeholders: {
      nameLabel: "Nom du formulaire",
      name: "Entrez le nom du formulaire",
      descriptionLabel: "Description",
      description: "Entrez une description pour le formulaire",
    },
    columns: ["NOM", "CHAMPS", "SOUMISSIONS", "CRÉÉ LE"],
  },
  {
    id: "sondage",
    title: "SONDAGE",
    subtitle: "Gérer les Sondages",
    icon: ClipboardList,
    placeholders: {
      nameLabel: "Nom du sondage",
      name: "Entrez le nom du sondage",
      descriptionLabel: "Objectif",
      description: "Quel est l'objectif de ce sondage ?",
    },
    columns: ["NOM", "OBJECTIF", "DATE DE CRÉATION"],
  },
  {
    id: "secretariat",
    title: "SÉCRÉTARIAT",
    subtitle: "Gérer les rendez-vous",
    icon: BookMarked,
    placeholders: {
      nameLabel: "Type de rendez-vous",
      name: "Ex: Entretien, Suivi, ...",
      descriptionLabel: "Détails",
      description: "Détails ou instructions",
    },
    columns: ["TYPE DE RDV", "DÉTAILS", "CRÉÉ LE"],
  },
  // Vous pouvez ajouter d'autres apps ici comme Groupes, Départements, Tags...
];

// --- DONNÉES DE SIMULATION ---
const mockData: {
  formulaire: Form[];
  sondage: {
    id: string;
    name: string;
    description: string;
    createdAt: string;
  }[];
  secretariat: any[];
} = {
  formulaire: [
    {
      id: "1",
      name: "Inscription événement",
      description: "Formulaire d'inscription pour les événements",
      fields: [{ id: "1", type: "text", label: "Nom", required: true }],
      createdAt: "2024-01-15",
      submissions: 24,
    },
    {
      id: "2",
      name: "Feedback satisfaction",
      description: "Formulaire de retour d'expérience",
      fields: [{ id: "1", type: "text", label: "Nom", required: false }],
      createdAt: "2024-01-20",
      submissions: 12,
    },
  ],
  sondage: [
    {
      id: "1",
      name: "Satisfaction Culte",
      description: "Mesurer la satisfaction après le culte.",
      createdAt: "2024-05-01",
    },
  ],
  secretariat: [],
};

// --- COMPOSANT PRINCIPAL ---
const FormBuilder: React.FC = () => {
  // --- ÉTAT GLOBAL DE LA PAGE ---
  const [activeApp, setActiveApp] = useState("formulaire");

  // --- ÉTATS SPÉCIFIQUES AU CRÉATEUR DE FORMULAIRES (de votre code) ---
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingForm, setEditingForm] = useState<Form | null>(null);
  const [formFields, setFormFields] = useState<FormField[]>([]);
  const [formName, setFormName] = useState("");
  const [formDescription, setFormDescription] = useState("");

  // --- DONNÉES DYNAMIQUES BASÉES SUR L'APP ACTIVE ---
  const currentAppConfig = APPS_CONFIG.find((app) => app.id === activeApp);
  const currentData: (Form | typeof mockData["sondage"][number] | any)[] =
    (mockData as any)[activeApp] || [];

  // --- LOGIQUE DU CRÉATEUR DE FORMULAIRES (de votre code) ---
  const addField = (type: FormField["type"]) => {
    const newField: FormField = {
      id: Date.now().toString(),
      type,
      label: `Nouveau champ ${type}`,
      required: false,
      options: type === "select" ? ["Option 1", "Option 2"] : undefined,
    };
    setFormFields([...formFields, newField]);
  };
  const updateField = (id: string, updates: Partial<FormField>) => {
    setFormFields(
      formFields.map((field) =>
        field.id === id ? { ...field, ...updates } : field
      )
    );
  };
  const removeField = (id: string) => {
    setFormFields(formFields.filter((field) => field.id !== id));
  };
  const getFieldTypeLabel = (type: string) => {
    switch (type) {
      case "text":
        return "Texte";
      case "email":
        return "Email";
      case "select":
        return "Liste déroulante";
      case "checkbox":
        return "Case à cocher";
      case "textarea":
        return "Zone de texte";
      default:
        return type;
    }
  };

  // --- GESTION DES ACTIONS ---
  const handleCreateClick = () => {
    if (activeApp === "formulaire") {
      // Pour les formulaires, on ouvre la modale de création complexe
      setEditingForm(null);
      setFormName("");
      setFormDescription("");
      setFormFields([]);
      setShowCreateModal(true);
    } else {
      // Pour les autres "apps", on peut imaginer une logique de création simple
      alert(
        `Logique de création à implémenter pour : ${currentAppConfig?.title}`
      );
    }
  };

  return (
    <div className="min-h-screen bg-[#F8F9FA] p-4 sm:p-6 lg:p-8 font-sans">
      {/* Section des cartes d'applications */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6 mb-8">
        {APPS_CONFIG.map((app) => (
          <div
            key={app.id}
            onClick={() => setActiveApp(app.id)}
            className={`bg-white rounded-lg p-4 text-center cursor-pointer transition-all duration-200 border ${
              activeApp === app.id
                ? "border-green-500 shadow-lg scale-105"
                : "border-gray-200 shadow-sm hover:shadow-md"
            }`}
          >
            <div className="w-12 h-12 bg-gray-100 rounded-md flex items-center justify-center mx-auto mb-3">
              <app.icon className="text-gray-600" size={24} />
            </div>
            <p className="text-sm font-semibold text-gray-800">{app.title}</p>
            <p className="text-xs text-gray-500">{app.subtitle}</p>
          </div>
        ))}
      </div>

      {/* Section principale avec le formulaire simple et la liste */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          {currentAppConfig && (
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 h-full">
              <form
                className="space-y-4"
                onSubmit={(e) => {
                  e.preventDefault();
                  handleCreateClick();
                }}
              >
                <div>
                  <label className="text-sm font-medium text-gray-600">
                    {currentAppConfig.placeholders.nameLabel}
                  </label>
                  <input
                    type="text"
                    placeholder={currentAppConfig.placeholders.name}
                    className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-1 focus:ring-green-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600">
                    {currentAppConfig.placeholders.descriptionLabel}
                  </label>
                  <textarea
                    placeholder={currentAppConfig.placeholders.description}
                    rows={4}
                    className="mt-1 w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-1 focus:ring-green-500 focus:outline-none"
                  />
                </div>
                <button
                  type="submit"
                  className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                >
                  Créer
                </button>
              </form>
            </div>
          )}
        </div>
        <div className="lg:col-span-2">
          {currentAppConfig && (
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 h-full">
              <div className="flex justify-end mb-4">
                <select className="px-3 py-1.5 border border-gray-300 rounded-full text-sm focus:ring-1 focus:ring-green-500 focus:outline-none">
                  <option>5 résultats par page</option>
                </select>
              </div>
              <div
                className={`grid ${
                  activeApp === "formulaire" ? "grid-cols-4" : "grid-cols-3"
                } gap-4 px-4 py-2 text-xs font-semibold text-gray-500 uppercase border-b`}
              >
                {currentAppConfig.columns.map((col) => (
                  <div key={col}>{col}</div>
                ))}
              </div>
              <div className="min-h-[200px]">
                {currentData.length > 0 ? (
                  currentData.map((item: Form | typeof mockData["sondage"][number]) => (
                    <div
                      key={item.id}
                      className={`grid ${
                        activeApp === "formulaire"
                          ? "grid-cols-4"
                          : "grid-cols-3"
                      } gap-4 px-4 py-3 border-b text-sm items-center`}
                    >
                      <span>{item.name}</span>
                      {activeApp === "formulaire" ? (
                        <>
                          <span>{item.fields.length} champ(s)</span>
                          <span>{item.submissions}</span>
                        </>
                      ) : (
                        <span className="truncate">{item.description}</span>
                      )}
                      <span>{item.createdAt}</span>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-16 text-gray-400">
                    Aucune donnée à afficher.
                  </div>
                )}
              </div>
              <div className="flex justify-center items-center gap-4 mt-6">
                <div className="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center font-bold text-sm">
                  1
                </div>
                <div className="flex gap-2">
                  <button className="w-8 h-8 border rounded-full flex items-center justify-center text-gray-400 hover:bg-gray-100">
                    <ChevronLeft size={16} />
                  </button>
                  <button className="w-8 h-8 border rounded-full flex items-center justify-center text-gray-400 hover:bg-gray-100">
                    <ChevronRight size={16} />
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* La Modale de création de formulaire complexe (votre code original) */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900">
                  Créer un formulaire
                </h3>
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ×
                </button>
              </div>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Form Builder */}
                <div>
                  <div className="mb-6">
                    <h4 className="text-md font-semibold text-gray-900 mb-4">
                      Configuration
                    </h4>
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Nom du formulaire
                        </label>
                        <input
                          type="text"
                          value={formName}
                          onChange={(e) => setFormName(e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#72C02C] focus:border-transparent"
                          placeholder="Nom du formulaire"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Description
                        </label>
                        <textarea
                          value={formDescription}
                          onChange={(e) => setFormDescription(e.target.value)}
                          rows={3}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#72C02C] focus:border-transparent"
                          placeholder="Description du formulaire"
                        />
                      </div>
                    </div>
                  </div>
                  <div className="mb-6">
                    <h4 className="text-md font-semibold text-gray-900 mb-4">
                      Ajouter des champs
                    </h4>
                    <div className="grid grid-cols-2 gap-2">
                      {[
                        { type: "text", label: "Texte" },
                        { type: "email", label: "Email" },
                        { type: "select", label: "Liste" },
                        { type: "checkbox", label: "Case" },
                        { type: "textarea", label: "Zone de texte" },
                      ].map((fieldType) => (
                        <button
                          key={fieldType.type}
                          onClick={() =>
                            addField(fieldType.type as FormField["type"])
                          }
                          className="p-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                        >
                          {fieldType.label}
                        </button>
                      ))}
                    </div>
                  </div>
                  <div>
                    <h4 className="text-md font-semibold text-gray-900 mb-4">
                      Champs du formulaire
                    </h4>
                    <div className="space-y-3">
                      {formFields.map((field) => (
                        <div
                          key={field.id}
                          className="border border-gray-200 rounded-lg p-3"
                        >
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-gray-700">
                              {getFieldTypeLabel(field.type)}
                            </span>
                            <button
                              onClick={() => removeField(field.id)}
                              className="text-red-600 hover:text-red-800"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </div>
                          <input
                            type="text"
                            value={field.label}
                            onChange={(e) =>
                              updateField(field.id, { label: e.target.value })
                            }
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#72C02C] focus:border-transparent mb-2"
                            placeholder="Libellé du champ"
                          />
                          <label className="flex items-center space-x-2">
                            <input
                              type="checkbox"
                              checked={field.required}
                              onChange={(e) =>
                                updateField(field.id, {
                                  required: e.target.checked,
                                })
                              }
                              className="rounded border-gray-300 text-[#72C02C] focus:ring-[#72C02C]"
                            />
                            <span className="text-sm text-gray-600">
                              Champ requis
                            </span>
                          </label>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
                {/* Preview */}
                <div>
                  <h4 className="text-md font-semibold text-gray-900 mb-4">
                    Aperçu
                  </h4>
                  <div className="bg-gray-50 rounded-lg p-4 min-h-[400px]">
                    <div className="bg-white rounded-lg p-6">
                      <h5 className="text-lg font-semibold text-gray-900 mb-2">
                        {formName || "Nouveau formulaire"}
                      </h5>
                      <p className="text-gray-600 text-sm mb-6">
                        {formDescription || "Description du formulaire"}
                      </p>
                      <div className="space-y-4">
                        {formFields.map((field) => (
                          <div key={field.id}>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                              {field.label}
                              {field.required && (
                                <span className="text-red-500">*</span>
                              )}
                            </label>
                            {field.type === "text" && (
                              <input
                                type="text"
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                                disabled
                              />
                            )}
                            {field.type === "email" && (
                              <input
                                type="email"
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                                disabled
                              />
                            )}
                            {field.type === "select" && (
                              <select
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                                disabled
                              >
                                <option>Sélectionnez une option</option>
                              </select>
                            )}
                            {field.type === "checkbox" && (
                              <label className="flex items-center space-x-2">
                                <input
                                  type="checkbox"
                                  className="rounded border-gray-300"
                                  disabled
                                />
                                <span className="text-sm text-gray-600">
                                  Option
                                </span>
                              </label>
                            )}
                            {field.type === "textarea" && (
                              <textarea
                                rows={3}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                                disabled
                              />
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex justify-end space-x-3 mt-6 pt-6 border-t">
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                >
                  Annuler
                </button>
                <button className="flex items-center space-x-2 px-4 py-2 bg-[#72C02C] text-white rounded-lg hover:bg-[#5da021] transition-colors">
                  <Save className="w-4 h-4" />
                  <span>Enregistrer</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FormBuilder;
