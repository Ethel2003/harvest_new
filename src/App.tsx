import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import Header from "./components/Layout/Header";
import LoginForm from "./components/Auth/LoginForm";
import Dashboard from "./components/Dashboard/Dashboard";
import MembersList from "./components/Community/MembersList";
import EventsList from "./components/Events/EventsList";
import FormBuilder from "./components/Apps/FormBuilder";
import AppointmentsList from "./components/Secretariat/AppointmentsList";
import Settings from "./components/Settings/Settings";

// Pages
import AddEventPage from "./components/Events/AddEventPage"; // Ajustez les chemins si besoin
import EditMemberPage from "./components/Community/EditMemberPage";
import MemberDetailsWrapper from "./components/Community/MemberDetailsWrapper";
import AvailabilityListPage from "./components/Secretariat/AvailabilityListPage";
import CategoryListPage from "./components/Secretariat/CategoryListPage";

// Ce composant gère l'affichage conditionnel (chargement, login, ou app principale)
const AppContent: React.FC = () => {
  const { user, isLoading } = useAuth();

  // --- LOADER ---
  // Affiche l'écran de chargement si l'authentification est en cours
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-[#72C02C] rounded-full flex items-center justify-center mx-auto mb-4 animate-pulse">
            <span className="text-white font-bold text-xl">CM</span>
          </div>
          <p className="text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  // --- LOGIN ---
  // Affiche le formulaire de connexion si l'utilisateur n'est pas authentifié
  if (!user) {
    return <LoginForm />;
  }

  // --- APPLICATION PRINCIPALE ---
  // Affiche l'application avec ses routes si l'utilisateur est connecté
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="min-h-[calc(100vh-4rem)]">
        <Routes>
          {/* Routes de base */}
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/apps" element={<FormBuilder />} />
          <Route path="/secretariat" element={<AppointmentsList />} />
          <Route path="/secretariat/availabilities" element={<AvailabilityListPage />} />
          <Route path="/secretariat/categories" element={<CategoryListPage  />} />

          {/* Route pour les paramètres */}
          
          <Route path="/settings" element={<Settings />} />

          {/* Routes pour la Communauté (Members) */}
          <Route path="/community" element={<MembersList />} />
          <Route
            path="/community/details/:id"
            element={<MemberDetailsWrapper />}
          />
          <Route
            path="/community/edit/:memberId"
            element={<EditMemberPage />}
          />

          {/* Routes pour les Événements */}
          <Route path="/events" element={<EventsList />} />
          <Route path="/events/add" element={<AddEventPage />} />
          {/* Vous pourriez ajouter ici : <Route path="/events/edit/:eventId" element={<EditEventPage />} /> */}

          {/* Route par défaut : redirige vers le tableau de bord */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </main>
    </div>
  );
};

// Le composant App principal qui fournit le contexte d'authentification et le routeur
function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
