import React, { useState } from "react";
import {
  User,
  Bell,
  Shield,
  Palette,
  Globe,
  Save,
  Camera,
  Eye,
  EyeOff,
  Check,
  X,
} from "lucide-react";

// --- SOUS-COMPOSANTS POUR UNE STRUCTURE IMPECCABLE ---

/**
 * SectionCard : Un composant réutilisable pour chaque bloc de paramètres.
 * Design premium avec animations et effets visuels.
 */
type SectionCardProps = {
  title: string;
  description: string;
  children: React.ReactNode;
};
const SectionCard: React.FC<SectionCardProps> = ({
  title,
  description,
  children,
}) => (
  <div className="bg-white rounded-2xl shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300 backdrop-blur-sm">
    <div className="p-8 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-white rounded-t-2xl">
      <h3 className="text-xl font-bold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600 leading-relaxed">{description}</p>
    </div>
    <div className="p-8 space-y-8">{children}</div>
  </div>
);

/**
 * CustomToggle : Un interrupteur stylé et moderne avec animations fluides.
 */
const CustomToggle: React.FC<{
  label: string;
  description: string;
  defaultChecked?: boolean;
}> = ({ label, description, defaultChecked = false }) => {
  const [isChecked, setIsChecked] = useState(defaultChecked);

  return (
    <div className="flex items-center justify-between p-4 rounded-xl bg-gray-50 hover:bg-gray-100 transition-all duration-200">
      <div className="flex-1">
        <h4 className="text-base font-semibold text-gray-900 mb-1">{label}</h4>
        <p className="text-sm text-gray-600">{description}</p>
      </div>
      <label className="relative inline-flex items-center cursor-pointer ml-4">
        <input
          type="checkbox"
          className="sr-only peer"
          checked={isChecked}
          onChange={(e) => setIsChecked(e.target.checked)}
        />
        <div className="w-14 h-7 bg-gray-300 rounded-full peer peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-emerald-300/50 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border after:rounded-full after:h-6 after:w-6 after:transition-all after:shadow-md peer-checked:bg-gradient-to-r peer-checked:from-emerald-500 peer-checked:to-green-600"></div>
      </label>
    </div>
  );
};

/**
 * InputField : Champ de saisie premium avec focus states
 */
const InputField: React.FC<{
  label: string;
  type?: string;
  placeholder?: string;
  defaultValue?: string;
  disabled?: boolean;
  className?: string;
}> = ({
  label,
  type = "text",
  placeholder,
  defaultValue,
  disabled,
  className = "",
}) => (
  <div className={className}>
    <label className="block text-sm font-semibold text-gray-700 mb-2">
      {label}
    </label>
    <input
      type={type}
      placeholder={placeholder}
      defaultValue={defaultValue}
      disabled={disabled}
      className="w-full px-4 py-3 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200 bg-white disabled:bg-gray-50 disabled:text-gray-500 hover:border-gray-300"
    />
  </div>
);

/**
 * SelectField : Menu déroulant premium
 */
const SelectField: React.FC<{
  label: string;
  options: string[];
  className?: string;
}> = ({ label, options, className = "" }) => (
  <div className={className}>
    <label className="block text-sm font-semibold text-gray-700 mb-2">
      {label}
    </label>
    <select className="w-full px-4 py-3 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200 bg-white hover:border-gray-300">
      {options.map((option, index) => (
        <option key={index}>{option}</option>
      ))}
    </select>
  </div>
);

/**
 * PasswordField : Champ mot de passe avec toggle visibilité
 */
const PasswordField: React.FC<{
  label: string;
  placeholder?: string;
  className?: string;
}> = ({ label, placeholder, className = "" }) => {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className={className}>
      <label className="block text-sm font-semibold text-gray-700 mb-2">
        {label}
      </label>
      <div className="relative">
        <input
          type={showPassword ? "text" : "password"}
          placeholder={placeholder}
          className="w-full px-4 py-3 pr-12 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200 bg-white hover:border-gray-300"
        />
        <button
          type="button"
          onClick={() => setShowPassword(!showPassword)}
          className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 transition-colors"
        >
          {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
        </button>
      </div>
    </div>
  );
};

// --- COMPOSANT PRINCIPAL DE LA PAGE PARAMÈTRES ---
const Settings: React.FC = () => {
  const [activeTab, setActiveTab] = useState("profile");
  const [isSaving, setIsSaving] = useState(false);

  const tabs = [
    {
      id: "profile",
      label: "Mon Profil",
      icon: User,
      color: "from-green-500 to-emerald-600",
    },
    {
      id: "security",
      label: "Sécurité",
      icon: Shield,
      color: "from-green-500 to-emerald-500",
    },
    {
      id: "notifications",
      label: "Notifications",
      icon: Bell,
      color: "from-green-500 to-emerald-600",
    },
    {
      id: "appearance",
      label: "Apparence",
      icon: Palette,
      color: "from-green-500 to-emerald-500",
    },
    {
      id: "general",
      label: "Général",
      icon: Globe,
      color: "from-green-500 to-emerald-600",
    },
  ];

  const handleSave = () => {
    setIsSaving(true);
    setTimeout(() => setIsSaving(false), 2000);
  };

  // Fonction pour afficher le contenu de l'onglet actif
  const renderContent = () => {
    switch (activeTab) {
      case "profile":
        return (
          <SectionCard
            title="Informations Personnelles"
            description="Mettez à jour vos informations de contact et votre profil professionnel."
          >
            <div className="flex items-center gap-6 mb-8">
              <div className="relative">
                <div className="w-24 h-24 bg-gradient-to-r from-emerald-400 to-green-600 rounded-full flex items-center justify-center shadow-lg">
                  <User size={40} className="text-white" />
                </div>
                <button className="absolute -bottom-2 -right-2 w-8 h-8 bg-white rounded-full shadow-lg border-2 border-gray-100 flex items-center justify-center hover:bg-gray-50 transition-colors">
                  <Camera size={16} className="text-gray-600" />
                </button>
              </div>
              <div>
                <h4 className="text-lg font-semibold text-gray-900">
                  Photo de profil
                </h4>
                <p className="text-gray-600 text-sm mb-3">
                  Ajoutez une photo professionnelle
                </p>
                <button className="px-4 py-2 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 transition-colors font-medium">
                  Changer la photo
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <InputField label="Nom complet" defaultValue="Administrateur" />
              <InputField
                label="Adresse email"
                type="email"
                defaultValue="admin@communitymanager.com"
                disabled
              />
              <InputField
                label="Numéro de téléphone"
                type="tel"
                placeholder="+33 1 23 45 67 89"
              />
              <InputField
                label="Titre professionnel"
                placeholder="Community Manager"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Biographie
              </label>
              <textarea
                placeholder="Parlez-nous de vous..."
                rows={4}
                className="w-full px-4 py-3 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200 bg-white hover:border-gray-300 resize-none"
              />
            </div>
          </SectionCard>
        );

      case "security":
        return (
          <div className="space-y-6">
            <SectionCard
              title="Modification du mot de passe"
              description="Maintenez votre compte sécurisé avec un mot de passe fort."
            >
              <div className="space-y-6">
                <PasswordField
                  label="Mot de passe actuel"
                  placeholder="Entrez votre mot de passe actuel"
                />
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <PasswordField
                    label="Nouveau mot de passe"
                    placeholder="Nouveau mot de passe"
                  />
                  <PasswordField
                    label="Confirmer le nouveau mot de passe"
                    placeholder="Confirmez le mot de passe"
                  />
                </div>
                <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
                  <h5 className="font-semibold text-blue-900 mb-2">
                    Conseils pour un mot de passe sécurisé :
                  </h5>
                  <ul className="text-sm text-blue-800 space-y-1">
                    <li>• Au moins 8 caractères</li>
                    <li>• Mélange de lettres majuscules et minuscules</li>
                    <li>• Inclure des chiffres et des symboles</li>
                  </ul>
                </div>
              </div>
            </SectionCard>

            <SectionCard
              title="Authentification à deux facteurs"
              description="Renforcez la sécurité de votre compte avec la 2FA."
            >
              <div className="flex items-center justify-between p-4 border border-gray-200 rounded-xl">
                <div>
                  <h4 className="font-semibold text-gray-900">
                    Authentification à deux facteurs
                  </h4>
                  <p className="text-sm text-gray-600">
                    Ajouter une couche de sécurité supplémentaire
                  </p>
                </div>
                <button className="px-4 py-2 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 transition-colors font-medium">
                  Activer
                </button>
              </div>
            </SectionCard>
          </div>
        );

      case "notifications":
        return (
          <SectionCard
            title="Préférences de notifications"
            description="Contrôlez quand et comment vous souhaitez être informé."
          >
            <div className="space-y-4">
              <CustomToggle
                label="Nouveaux membres"
                description="Recevoir une notification lors de l'arrivée d'un nouveau membre"
                defaultChecked
              />
              <CustomToggle
                label="Événements à venir"
                description="Rappels pour les événements que vous suivez"
                defaultChecked
              />
              <CustomToggle
                label="Rendez-vous"
                description="Notifications pour les rendez-vous confirmés ou annulés"
              />
              <CustomToggle
                label="Résumé hebdomadaire"
                description="Un récapitulatif de l'activité de la semaine par email"
              />
              <CustomToggle
                label="Notifications push"
                description="Recevoir des notifications directement sur votre appareil"
                defaultChecked
              />
              <CustomToggle
                label="Notifications par SMS"
                description="Recevoir des alertes importantes par SMS"
              />
            </div>
          </SectionCard>
        );

      case "appearance":
        return (
          <SectionCard
            title="Personnalisation de l'interface"
            description="Adaptez l'apparence de l'application à vos préférences."
          >
            <div className="space-y-8">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-4">
                  Thème de l'application
                </label>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {[
                    {
                      name: "Clair",
                      preview: "bg-white border-2 border-gray-200",
                    },
                    {
                      name: "Sombre",
                      preview: "bg-gray-900 border-2 border-gray-700",
                    },
                    {
                      name: "Système",
                      preview:
                        "bg-gradient-to-r from-white to-gray-900 border-2 border-gray-400",
                    },
                  ].map((theme) => (
                    <div key={theme.name} className="relative">
                      <input
                        type="radio"
                        name="theme"
                        id={theme.name}
                        className="sr-only peer"
                        defaultChecked={theme.name === "Clair"}
                      />
                      <label
                        htmlFor={theme.name}
                        className="block p-4 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors peer-checked:ring-2 peer-checked:ring-emerald-500"
                      >
                        <div
                          className={`w-full h-16 rounded-lg mb-3 ${theme.preview}`}
                        ></div>
                        <p className="text-sm font-medium text-center">
                          {theme.name}
                        </p>
                      </label>
                    </div>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <SelectField
                  label="Taille de police"
                  options={["Petite", "Normale", "Grande"]}
                />
                <SelectField
                  label="Densité d'affichage"
                  options={["Compacte", "Normale", "Confortable"]}
                />
              </div>
            </div>
          </SectionCard>
        );

      case "general":
        return (
          <SectionCard
            title="Paramètres généraux"
            description="Configurez les options de base de votre compte et de l'application."
          >
            <div className="space-y-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <SelectField
                  label="Langue de l'interface"
                  options={["Français", "English", "Español", "Deutsch"]}
                />
                <SelectField
                  label="Format de date"
                  options={["jj/mm/aaaa", "mm/jj/aaaa", "aaaa-mm-jj"]}
                />
                <SelectField
                  label="Fuseau horaire"
                  options={["Europe/Paris", "UTC", "America/New_York"]}
                />
                <SelectField
                  label="Format d'heure"
                  options={["24 heures", "12 heures (AM/PM)"]}
                />
              </div>

              <div className="border-t border-gray-200 pt-6">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">
                  Gestion des données
                </h4>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 border border-gray-200 rounded-xl">
                    <div>
                      <h5 className="font-medium text-gray-900">
                        Exporter mes données
                      </h5>
                      <p className="text-sm text-gray-600">
                        Télécharger toutes vos données personnelles
                      </p>
                    </div>
                    <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors font-medium">
                      Exporter
                    </button>
                  </div>

                  <div className="flex items-center justify-between p-4 border border-red-200 rounded-xl bg-red-50">
                    <div>
                      <h5 className="font-medium text-red-900">
                        Supprimer mon compte
                      </h5>
                      <p className="text-sm text-red-700">
                        Action irréversible - toutes vos données seront
                        supprimées
                      </p>
                    </div>
                    <button className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors font-medium">
                      Supprimer
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </SectionCard>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 p-4 sm:p-6 lg:p-8 font-sans">
      <div className="max-w-7xl mx-auto">
        <header className="mb-12 text-center">
          <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent mb-4">
            Paramètres
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Personnalisez votre expérience et gérez les préférences de votre
            compte
          </p>
        </header>

        <div className="flex flex-col xl:flex-row gap-8">
          {/* Navigation latérale */}
          <aside className="xl:w-80 xl:flex-shrink-0">
            <nav className="sticky top-8 bg-white rounded-2xl shadow-lg border border-gray-100 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-6">
                Navigation
              </h2>
              <div className="space-y-2">
                {tabs.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center gap-4 px-4 py-3 rounded-xl text-left font-medium transition-all duration-200 ${
                      activeTab === tab.id
                        ? `bg-gradient-to-r ${tab.color} text-white shadow-lg transform scale-105`
                        : "text-gray-700 hover:bg-gray-50 hover:text-gray-900"
                    }`}
                  >
                    <tab.icon className="w-5 h-5 flex-shrink-0" />
                    <span>{tab.label}</span>
                  </button>
                ))}
              </div>
            </nav>
          </aside>

          {/* Contenu principal */}
          <main className="flex-1 space-y-8">
            <div className="animate-fadeIn">{renderContent()}</div>

            {/* Bouton de sauvegarde global */}
            <div className="flex justify-end pt-8">
              <button
                onClick={handleSave}
                disabled={isSaving}
                className="flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-xl hover:from-emerald-600 hover:to-green-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed font-semibold text-lg"
              >
                {isSaving ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    Sauvegarde en cours...
                  </>
                ) : (
                  <>
                    <Save size={20} />
                    Enregistrer les modifications
                  </>
                )}
              </button>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
};

export default Settings;
