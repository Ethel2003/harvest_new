import React, { useState } from 'react';
import { Users, Building, UserCheck, Calendar, TrendingUp, MoreHorizontal, BarChart3, LineChart } from 'lucide-react';
import StatsCard from './StatsCard';
import MemberEvolutionChart from './MemberEvolutionChart';
import PieChart from './PieChart';
import { DashboardStats, DepartementType, GroupeType } from '../../types';
import { useEffect } from 'react';
import { statisticsService } from '../../services';
import { convertColorToHex } from '../../utils/colorUtils';

const DashboardAdvanced: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [groups, setGroups] = useState<GroupeType | null>(null);
  const [departments, setDepartments] = useState<DepartementType | null>(null);
  const [chartLayout, setChartLayout] = useState<'full' | 'split'>('full');

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await statisticsService.getDashboardStats();
        if (response.data) {
          setStats(response.data);
        }

        const groupResponse = await statisticsService.getGroupStatistics();
        if (groupResponse.data) {
          setGroups(groupResponse.data);
        }

        const departmentResponse = await statisticsService.getDepartmentStatistics();
        if (departmentResponse.data) {
          setDepartments(departmentResponse.data);
        }
      } catch (error) {
        console.error("Erreur lors du chargement des statistiques:", error);
      }
    };
    fetchStats();
  }, []);

  const statsCards = [
    {
      title: 'Nombre de groupes',
      value: stats?.groups || 0,
      icon: Users,
      color: 'bg-purple-500',
      iconColor: 'text-purple-600'
    },
    {
      title: 'Nombre de départements',
      value: stats?.departments || 0,
      icon: Building,
      color: 'bg-orange-500',
      iconColor: 'text-orange-600'
    },
    {
      title: 'Nombre d\'utilisateurs',
      value: stats?.users || 0,
      icon: UserCheck,
      color: 'bg-green-500',
      iconColor: 'text-green-600'
    },
    {
      title: 'Nombre de membres',
      value: stats?.members || 0,
      icon: Users,
      color: 'bg-blue-500',
      iconColor: 'text-blue-600'
    }
  ];

  const groupsData = groups?.data?.groupes?.map(groupe => ({
    name: groupe.nom,
    value: groupe.membres_count,
    color: convertColorToHex(groupe.color)
  })) || []

  const departmentsData = departments?.data?.departements?.map(departement => ({
    name: departement.nom,
    value: departement.membres_count,
    color: convertColorToHex(departement.color)
  })) || []

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Tableau de bord avancé</h1>
        <p className="text-gray-600">Vue d'ensemble de votre communauté avec options de mise en page</p>
      </div>

      {/* Contrôles de mise en page */}
      <div className="mb-6 bg-white rounded-lg p-4 shadow-sm border border-gray-200">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">Options d'affichage</h3>
          <div className="flex items-center space-x-4">
            <label className="flex items-center space-x-2">
              <input
                type="radio"
                name="layout"
                value="full"
                checked={chartLayout === 'full'}
                onChange={(e) => setChartLayout(e.target.value as 'full' | 'split')}
                className="text-blue-600 focus:ring-blue-500"
              />
              <span className="text-sm text-gray-700">Pleine largeur</span>
            </label>
            <label className="flex items-center space-x-2">
              <input
                type="radio"
                name="layout"
                value="split"
                checked={chartLayout === 'split'}
                onChange={(e) => setChartLayout(e.target.value as 'full' | 'split')}
                className="text-blue-600 focus:ring-blue-500"
              />
              <span className="text-sm text-gray-700">Deux colonnes</span>
            </label>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statsCards.map((stat, index) => (
          <StatsCard key={index} {...stat} />
        ))}
      </div>

      {/* Charts Section - Layout dynamique */}
      {chartLayout === 'full' ? (
        // OPTION 1: Full Width
        <div className="mb-8">
          <MemberEvolutionChart 
            title="Évolution des Membres - Vue complète"
            height={450}
            showFilters={true}
            className="w-full"
          />
        </div>
      ) : (
        // OPTION 2: Split Layout
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <MemberEvolutionChart 
              title="Évolution Quotidienne"
              height={350}
              showFilters={false}
            />
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <MemberEvolutionChart 
              title="Évolution Mensuelle"
              height={350}
              showFilters={false}
            />
          </div>
        </div>
      )}

      {/* Pie Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Groups Chart */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Répartition par Groupes</h3>
            <button className="text-gray-400 hover:text-gray-600">
              <MoreHorizontal className="w-5 h-5" />
            </button>
          </div>
          <PieChart data={groupsData} />
        </div>

        {/* Departments Chart */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Répartition par Départements</h3>
            <button className="text-gray-400 hover:text-gray-600">
              <MoreHorizontal className="w-5 h-5" />
            </button>
          </div>
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <PieChart data={departmentsData} />
            </div>
          </div>
        </div>
      </div>

      {/* Section d'informations supplémentaires */}
      <div className="mt-8 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Informations sur l'évolution des membres</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600">
          <div>
            <h4 className="font-medium text-gray-900 mb-2">📊 Données en temps réel</h4>
            <p>L'évolution des membres est calculée en temps réel à partir des dates de création des profils.</p>
          </div>
          <div>
            <h4 className="font-medium text-gray-900 mb-2">📅 Filtres disponibles</h4>
            <p>Vous pouvez filtrer par période et choisir entre un affichage quotidien ou mensuel.</p>
          </div>
          <div>
            <h4 className="font-medium text-gray-900 mb-2">📈 Métriques calculées</h4>
            <p>Le graphique affiche le nombre cumulatif de membres et l'évolution entre les périodes.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardAdvanced; 