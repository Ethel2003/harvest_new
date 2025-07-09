import React, { useState, useEffect } from 'react';
import { statisticsService } from '../../services/statisticsService';
import { convertColorToHex } from '../../utils/colorUtils';

// Types pour les données d'évolution des membres
interface MemberEvolutionData {
  date: string;
  value: number;
}

interface MemberEvolutionChartProps {
  className?: string;
  title?: string;
  height?: number;
  showFilters?: boolean;
}

const MemberEvolutionChart: React.FC<MemberEvolutionChartProps> = ({
  className = '',
  title = 'Évolution des Membres',
  height = 400,
  showFilters = true
}) => {
  const [data, setData] = useState<MemberEvolutionData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    start_date: '',
    end_date: '',
    period: 'daily' as 'daily' | 'monthly'
  });

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Préparer les filtres en excluant les valeurs vides
      const requestFilters: any = {};
      
      if (filters.period) {
        requestFilters.period = filters.period;
      }
      
      if (filters.start_date && filters.start_date.trim() !== '') {
        requestFilters.start_date = filters.start_date;
      }
      
      if (filters.end_date && filters.end_date.trim() !== '') {
        requestFilters.end_date = filters.end_date;
      }
      
      // Appeler l'API avec les filtres préparés
      const response = await statisticsService.getMemberEvolution(Object.keys(requestFilters).length > 0 ? requestFilters : undefined);
      
      // La réponse de l'API Django a la structure { success: boolean, data: [...], error?: string }
      const apiData = response.data as any;
      
      if (apiData.success && apiData.data) {
        setData(apiData.data);
      } else {
        setError(apiData.error || 'Erreur lors de la récupération des données');
      }
    } catch (err) {
      setError('Erreur de connexion au serveur');
      console.error('Erreur lors de la récupération de l\'évolution des membres:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [filters]);

  const handleFilterChange = (key: string, value: string) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleFormatChange = (period: 'daily' | 'monthly') => {
    setFilters(prev => ({
      ...prev,
      period
    }));
  };

  const resetFilters = () => {
    setFilters({
      start_date: '',
      end_date: '',
      period: 'daily'
    });
  };



  if (loading) {
    return (
      <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">Chargement des données...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="text-red-500 text-lg mb-2">⚠️ Erreur</div>
            <div className="text-gray-600 mb-4">{error}</div>
            <button
              onClick={fetchData}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
            >
              Réessayer
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
        
        {showFilters && (
          <div className="flex items-center space-x-4">
            {/* Format selector */}
            <div className="flex items-center space-x-2">
              <label className="text-sm text-gray-600">Format:</label>
              <select
                value={filters.period}
                onChange={(e) => handleFormatChange(e.target.value as 'daily' | 'monthly')}
                className="px-3 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="daily">Quotidien</option>
                <option value="monthly">Mensuel</option>
              </select>
            </div>

            {/* Date filters */}
            <div className="flex items-center space-x-2">
              <input
                type="date"
                value={filters.start_date}
                onChange={(e) => handleFilterChange('start_date', e.target.value)}
                className="px-3 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Date début"
              />
              <span className="text-gray-500">à</span>
              <input
                type="date"
                value={filters.end_date}
                onChange={(e) => handleFilterChange('end_date', e.target.value)}
                className="px-3 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Date fin"
              />
            </div>

            {/* Reset button */}
            <button
              onClick={resetFilters}
              className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800 transition-colors"
            >
              Réinitialiser
            </button>
          </div>
        )}
      </div>

      {data.length === 0 ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="text-gray-500 text-lg mb-2">📊 Aucune donnée</div>
            <div className="text-gray-400">Aucune donnée d'évolution disponible pour cette période</div>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          {/* Statistiques rapides */}
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="bg-blue-50 p-3 rounded-lg">
              <div className="text-sm text-blue-600 font-medium">Total Membres</div>
              <div className="text-2xl font-bold text-blue-800">
                {data.length > 0 ? data[data.length - 1].value : 0}
              </div>
            </div>
            <div className="bg-green-50 p-3 rounded-lg">
              <div className="text-sm text-green-600 font-medium">Nouveaux (période)</div>
              <div className="text-2xl font-bold text-green-800">
                {data.length > 1 ? data[data.length - 1].value - data[0].value : 0}
              </div>
            </div>
            <div className="bg-purple-50 p-3 rounded-lg">
              <div className="text-sm text-purple-600 font-medium">Points de données</div>
              <div className="text-2xl font-bold text-purple-800">{data.length}</div>
            </div>
          </div>

          {/* Affichage des données en tableau */}
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border border-gray-200 rounded-lg">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Nombre de Membres
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Évolution
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {data.map((item, index) => {
                  const previousValue = index > 0 ? data[index - 1].value : 0;
                  const evolution = item.value - previousValue;
                  const evolutionColor = evolution > 0 ? 'text-green-600' : evolution < 0 ? 'text-red-600' : 'text-gray-500';
                  const evolutionIcon = evolution > 0 ? '↗' : evolution < 0 ? '↘' : '→';
                  
                  return (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm text-gray-900 font-medium">
                        {item.date}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-900">
                        <span className="font-semibold">{item.value}</span> membres
                      </td>
                      <td className={`px-4 py-3 text-sm ${evolutionColor}`}>
                        {evolutionIcon} {evolution > 0 ? '+' : ''}{evolution}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Informations supplémentaires */}
          <div className="text-xs text-gray-500 text-center">
            {filters.period === 'daily' ? 'Données quotidiennes' : 'Données mensuelles'}
            {filters.start_date && filters.end_date && (
              <span> • Période: {filters.start_date} à {filters.end_date}</span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default MemberEvolutionChart; 