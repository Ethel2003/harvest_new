import React from 'react';
import { Users, Building, UserCheck, Calendar, TrendingUp, MoreHorizontal } from 'lucide-react';
import StatsCard from './StatsCard';
import MemberEvolutionChart from './MemberEvolutionChart';
import PieChart from './PieChart';
import { DashboardStats, DepartementType, GroupeType } from '../../types';
import { useEffect, useState } from 'react';
import { statisticsService } from '../../services';
import { convertColorToHex } from '../../utils/colorUtils';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [groups, setGroups] = useState<GroupeType | null>(null);
  const [departments, setDepartments] = useState<DepartementType | null>(null);


  useEffect(() => {
    const fetchStats = async () => {
      try {
        // Récupérer les statistiques du tableau de bord
        const response = await statisticsService.getDashboardStats();
        
        if (response.data) {
          setStats(response.data);
        }

        // Récupérer les statistiques des groupes
        const groupResponse = await statisticsService.getGroupStatistics();
   
        if (groupResponse.data) {
          setGroups(groupResponse.data);
        }

        // Récupérer les statistiques des départements
        const departmentResponse = await statisticsService.getDepartmentStatistics();
        
        if (departmentResponse.data) {
          setDepartments(departmentResponse.data);
        }
      } catch (error) {
        console.error("Erreur lors du chargement des statistiques:", error);
        // Vous pouvez ajouter ici une gestion d'erreur plus sophistiquée
        // comme afficher un message d'erreur à l'utilisateur
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
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Tableau de bord</h1>
        <p className="text-gray-600">Vue d'ensemble de votre communauté</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statsCards.map((stat, index) => (
          <StatsCard key={index} {...stat} />
        ))}
      </div>

      {/* OPTION 1: Member Evolution Chart - Full Width (recommandé) */}
      <div className="mb-8">
        <MemberEvolutionChart 
          title="Évolution des Membres"
          height={400}
          showFilters={true}
          className="w-full"
        />
      </div>

      {/* OPTION 2: Charts Section avec deux colonnes (alternative) */}
      {/* 
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <MemberEvolutionChart 
            title="Évolution des Membres"
            height={300}
            showFilters={true}
          />
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Autre graphique</h3>
          <p className="text-gray-500">Espace pour un autre graphique</p>
        </div>
      </div>
      */}

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
            
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;