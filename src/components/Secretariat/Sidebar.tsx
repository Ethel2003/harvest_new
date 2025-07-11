import React from "react";
import { Link } from "react-router-dom";
import {
  User,
  Settings,
  Calendar,
  ChevronRight,
  Upload,
} from "lucide-react";

interface SidebarProps {
  activeKey: "rendez-vous" | "disponibilites" | "categories";
}

const navItems = [
  {
    key: "rendez-vous",
    label: "Rendez-vous",
    icon: User,
    path: "/secretariat",
  },
  {
    key: "disponibilites",
    label: "Disponibilités",
    icon: Calendar,
    path: "/secretariat/availabilities",
  },
  {
    key: "categories",
    label: "Catégories de Rendez-vous",
    icon: Settings,
    path: "/secretariat/categories",
  },
];

const Sidebar: React.FC<SidebarProps> = ({ activeKey }) => {
  return (
    <aside className="w-full lg:w-72 flex-shrink-0">
      <div className="space-y-6">
        <button className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-[#6c757d] text-white rounded-lg hover:bg-[#5a6268] transition-colors shadow-sm font-medium text-sm">
          <Upload size={16} />
          <span>Exporter une liste de Membre</span>
        </button>
        <div className="bg-white rounded-xl shadow-md border border-gray-200 p-4">
          <div className="flex items-center gap-4 mb-6">
            <div className="w-12 h-12 bg-black rounded-full flex items-center justify-center">
              <User size={28} className="text-white" />
            </div>
            <span className="font-semibold text-gray-800">utilisateur1</span>
          </div>
          <nav className="space-y-2">
            {navItems.map((item) => (
              <Link
                key={item.key}
                to={item.path}
                className={`flex items-center justify-between p-3 rounded-lg text-sm font-medium transition-colors ${
                  activeKey === item.key
                    ? "bg-green-50 text-green-700 border border-green-200 shadow-sm"
                    : "text-gray-600 hover:bg-gray-50"
                }`}
              >
                <div className="flex items-center gap-3">
                  <item.icon
                    size={18}
                    className={activeKey === item.key ? "text-green-600" : "text-gray-400"}
                  />
                  <span>{item.label}</span>
                </div>
                {activeKey === item.key && (
                  <ChevronRight size={16} className="text-green-600" />
                )}
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar; 