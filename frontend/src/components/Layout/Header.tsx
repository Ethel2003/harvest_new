import React, { useState } from "react";
// IMPORTER NavLink ET Link
import { NavLink, Link } from "react-router-dom";
import { User, Settings, LogOut, ChevronDown } from "lucide-react";
import { useAuth } from "../../contexts/AuthContext";

//  MODIFIER LA SIGNATURE DU COMPOSANT
const Header: React.FC = () => {
  const { user, logout } = useAuth();
  const [showUserMenu, setShowUserMenu] = useState(false);

  const navItems = [
    { key: "dashboard", label: "TABLEAU DE BORD" },
    { key: "community", label: "COMMUNAUTÉ" },
    { key: "events", label: "ÉVÉNEMENTS" },
    { key: "apps", label: "APPS" },
    { key: "secretariat", label: "SECRÉTARIAT" },
  ];

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <div className="flex-shrink-0 flex items-center">
              <div className="w-8 h-8 bg-[#72C02C] rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">CM</span>
              </div>
              <span className="ml-2 text-xl font-semibold text-gray-900">
                Community Manager
              </span>
            </div>
          </div>

          {/* 4. MODIFIER LA NAVIGATION PRINCIPALE */}
          <nav className="hidden md:flex space-x-8">
            {navItems.map((item) => (
              <NavLink
                key={item.key}
                to={`/${item.key}`}
                className={({ isActive }) =>
                  `px-3 py-2 text-sm font-medium transition-colors duration-200 ${
                    isActive
                      ? "text-[#72C02C] border-b-2 border-[#72C02C]"
                      : "text-gray-600 hover:text-[#72C02C]"
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>

          {/* Menu Utilisateur (avec des modifications mineures) */}
          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
                <User className="w-4 h-4 text-gray-600" />
              </div>
              <span className="text-sm font-medium text-gray-700 hidden sm:block">
                {user?.name}
              </span>
              <ChevronDown className="w-4 h-4 text-gray-500" />
            </button>

            {showUserMenu && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50">
                {/* 5. LE BOUTON "PARAMÈTRES" DEVIENT UN LIEN */}
                <Link
                  to="/settings" // Navigation vers la page des paramètres
                  onClick={() => setShowUserMenu(false)}
                  className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-2"
                >
                  <Settings className="w-4 h-4" />
                  <span>Paramètres</span>
                </Link>
                {/* Le bouton de déconnexion} */}
                <button
                  onClick={() => {
                    setShowUserMenu(false);
                    logout();
                  }}
                  className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center space-x-2"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Déconnexion</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
