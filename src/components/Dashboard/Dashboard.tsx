import React from 'react';
import { Users, Building, UserCheck, Calendar, TrendingUp, MoreHorizontal } from 'lucide-react';
import StatsCard from './StatsCard';
import LineChart from './LineChart';
import PieChart from './PieChart';

const Dashboard: React.FC = () => {
  const stats = [
    {
      title: 'Nombre de groupes',
      value: 13,
      icon: Users,
      color: 'bg-purple-500',
      iconColor: 'text-purple-600'
    },
    {
      title: 'Nombre de départements',
      value: 13,
      icon: Building,
      color: 'bg-orange-500',
      iconColor: 'text-orange-600'
    },
    {
      title: 'Nombre d\'utilisateurs',
      value: 1,
      icon: UserCheck,
      color: 'bg-green-500',
      iconColor: 'text-green-600'
    },
    {
      title: 'Nombre de membres',
      value: 656,
      icon: Users,
      color: 'bg-blue-500',
      iconColor: 'text-blue-600'
    }
  ];

  const newMembersData = [
    { date: '30 Jun', value: 0 },
    { date: 'Jul \'25', value: 1 },
    { date: '02 Jul', value: 2 },
    { date: '03 Jul', value: 3 },
    { date: '04 Jul', value: 4 },
    { date: '05 Jul', value: 5 },
    { date: '06 Jul', value: 4 }
  ];

  const groupsData = [
    { name: 'FR Paralelos', value: 16.7, color: '#4ade80' },
    { name: 'FR Agneau de Dieu', value: 16.7, color: '#22c55e' },
    { name: 'FR Le Véritable', value: 11.1, color: '#16a34a' },
    { name: 'FR Oméga', value: 11.1, color: '#15803d' },
    { name: 'FR Admirable', value: 11.1, color: '#166534' },
    { name: 'FR La Fidèle', value: 11.1, color: '#14532d' },
    { name: 'FR Amen', value: 11.1, color: '#365314' },
    { name: 'FR Lion de la tribu de Juda', value: 8.3, color: '#fbbf24' },
    { name: 'Groupe Test', value: 19.4, color: '#6b7280' },
    { name: 'FR Le Rocher', value: 11.1, color: '#ef4444' },
    { name: 'FR Prince de paix', value: 11.1, color: '#3b82f6' },
    { name: 'FR Fils de David', value: 11.1, color: '#06b6d4' },
    { name: 'FR Alpha', value: 11.1, color: '#8b5cf6' }
  ];

  const departmentsData = [
    { name: 'Conciergerie', value: 100, color: '#22c55e' }
  ];

  const departmentsList = [
    'Conciergerie', 'Santé divine', 'Coordination', 'DSIT', 'MHI', 'Entretien',
    'Accueil', 'Chorale', 'MFI', 'MFI', 'Audiovisuel', 'Intégration', 'Communication'
  ];

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Tableau de bord</h1>
        <p className="text-gray-600">Vue d'ensemble de votre communauté</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, index) => (
          <StatsCard key={index} {...stat} />
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* New Members Chart */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Nouveaux membres</h3>
            <button className="text-gray-400 hover:text-gray-600">
              <MoreHorizontal className="w-5 h-5" />
            </button>
          </div>
          <LineChart data={newMembersData} />
        </div>

        {/* Empty space for balance */}
        <div></div>
      </div>

      {/* Pie Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Groups Chart */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Groupes</h3>
            <button className="text-gray-400 hover:text-gray-600">
              <MoreHorizontal className="w-5 h-5" />
            </button>
          </div>
          <PieChart data={groupsData} />
        </div>

        {/* Departments Chart */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Départements</h3>
            <button className="text-gray-400 hover:text-gray-600">
              <MoreHorizontal className="w-5 h-5" />
            </button>
          </div>
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <PieChart data={departmentsData} />
            </div>
            <div className="ml-6 space-y-2">
              {departmentsList.map((dept, index) => (
                <div key={index} className="flex items-center space-x-2 text-sm">
                  <div className="w-3 h-3 rounded-full bg-green-500"></div>
                  <span className="text-gray-700">{dept}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;