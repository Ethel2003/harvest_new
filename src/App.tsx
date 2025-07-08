import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"; // IMPORT
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import Header from "./components/Layout/Header";
import LoginForm from "./components/Auth/LoginForm";
import Dashboard from "./components/Dashboard/Dashboard";
import MembersList from "./components/Community/MembersList";
import EventsList from "./components/Events/EventsList";
import FormBuilder from "./components/Apps/FormBuilder";
import AppointmentsList from "./components/Secretariat/AppointmentsList";
import Settings from "./components/Settings/Settings";
import AddEventPage from "./components/Events/AddEventPage";
import EditMemberPage from "./components/Community/EditMemberPage";
import MemberDetailsPage from "./components/Community/MemberDetailsPage";

// Ce composant contient la logique d'affichage conditionnel (login ou app)
const AppContent: React.FC = () => {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        {/* ... Votre écran de chargement ... */}
      </div>
    );
  }

  if (!user) {
    return <LoginForm />;
  }

  // Si l'utilisateur est connecté, on affiche la structure principale avec les routes
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Le Header n'a plus besoin de onPageChange */}
      <Header />
      <main className="min-h-[calc(100vh-4rem)]">
        <Routes>
          {/* Les routes remplacent votre ancien switch/case */}
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/community" element={<MembersList />} />
          <Route
            path="/community/details/:memberId"
            element={<MemberDetailsPage />}
          />
          <Route path="/events" element={<EventsList />} />
          {/* NOUVELLE ROUTE DÉDIÉE */}
          <Route path="/events/add" element={<AddEventPage />} />
          <Route
            path="/community/edit/:memberId"
            element={<EditMemberPage />}
          />

          <Route path="/apps" element={<FormBuilder />} />
          <Route path="/secretariat" element={<AppointmentsList />} />
          <Route path="/settings" element={<Settings />} />

          {/* Redirection par défaut vers le dashboard */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </main>
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      {/* BrowserRouter doit envelopper tout ce qui utilisera le routage */}
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
