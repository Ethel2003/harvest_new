import React, { useState } from 'react';
import { statisticsService } from '../../services/statisticsService';

interface TestResult {
  name: string;
  success: boolean;
  data?: any;
  error?: string;
  url?: string;
}

const MemberEvolutionTest: React.FC = () => {
  const [results, setResults] = useState<TestResult[]>([]);
  const [loading, setLoading] = useState(false);

  const runTests = async () => {
    setLoading(true);
    setResults([]);

    const testCases = [
      {
        name: "Sans paramètres",
        filters: undefined as any
      },
      {
        name: "Format daily seulement",
        filters: { format: 'daily' as const }
      },
      {
        name: "Format monthly seulement",
        filters: { format: 'monthly' as const }
      },
      {
        name: "Start date seulement",
        filters: { start_date: '2024-01-01' }
      },
      {
        name: "End date seulement",
        filters: { end_date: '2024-12-31' }
      },
      {
        name: "Start et end date",
        filters: { start_date: '2024-01-01', end_date: '2024-12-31' }
      },
      {
        name: "Tous les paramètres",
        filters: { start_date: '2024-01-01', end_date: '2024-12-31', format: 'daily' as const }
      },
      {
        name: "Dates vides",
        filters: { start_date: '', end_date: '', format: 'daily' as const }
      }
    ];

    const newResults: TestResult[] = [];

    for (const testCase of testCases) {
      try {
        console.log(`🧪 Test: ${testCase.name}`);
        console.log(`📋 Paramètres:`, testCase.filters);

        const response = await statisticsService.getMemberEvolution(testCase.filters);
        
        // Extraire les données de la réponse Django
        const apiData = response.data as any;
        
        if (apiData.success && apiData.data) {
          newResults.push({
            name: testCase.name,
            success: true,
            data: apiData.data,
            url: response.data ? 'URL générée avec succès' : 'Pas d\'URL'
          });
          console.log(`✅ Succès: ${testCase.name} - ${apiData.data.length} points de données`);
        } else {
          newResults.push({
            name: testCase.name,
            success: false,
            error: apiData.error || 'Erreur inconnue',
            url: response.data ? 'URL générée avec succès' : 'Pas d\'URL'
          });
          console.log(`❌ Erreur: ${testCase.name} - ${apiData.error}`);
        }
      } catch (error: any) {
        newResults.push({
          name: testCase.name,
          success: false,
          error: error.message || 'Erreur de connexion',
          url: 'Erreur lors de la génération de l\'URL'
        });
        console.log(`❌ Exception: ${testCase.name} - ${error.message}`);
      }
    }

    setResults(newResults);
    setLoading(false);
  };

  const clearResults = () => {
    setResults([]);
  };

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Test de la méthode getMemberEvolution</h1>
          <p className="text-gray-600">Teste différents scénarios de paramètres pour l'endpoint evolution_membres</p>
        </div>

        {/* Contrôles */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex items-center space-x-4">
            <button
              onClick={runTests}
              disabled={loading}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Tests en cours...' : 'Lancer les tests'}
            </button>
            <button
              onClick={clearResults}
              className="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              Effacer les résultats
            </button>
          </div>
          
          {loading && (
            <div className="mt-4 flex items-center">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
              <span className="text-sm text-gray-600">Exécution des tests...</span>
            </div>
          )}
        </div>

        {/* Résultats */}
        {results.length > 0 && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-gray-900">Résultats des tests</h2>
            
            {results.map((result, index) => (
              <div
                key={index}
                className={`bg-white rounded-lg shadow-sm border border-gray-200 p-6 ${
                  result.success ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'
                }`}
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-medium text-gray-900">{result.name}</h3>
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-medium ${
                      result.success
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {result.success ? '✅ Succès' : '❌ Échec'}
                  </span>
                </div>

                <div className="space-y-2">
                  <div className="text-sm text-gray-600">
                    <strong>URL:</strong> {result.url}
                  </div>
                  
                  {result.success && result.data && (
                    <div className="text-sm text-gray-600">
                      <strong>Données récupérées:</strong> {result.data.length} points
                      {result.data.length > 0 && (
                        <div className="mt-2">
                          <strong>Exemples:</strong>
                          <ul className="list-disc list-inside ml-4">
                            {result.data.slice(0, 3).map((item: any, i: number) => (
                              <li key={i}>
                                {item.date}: {item.value} membres
                              </li>
                            ))}
                            {result.data.length > 3 && (
                              <li>... et {result.data.length - 3} autres points</li>
                            )}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}
                  
                  {!result.success && result.error && (
                    <div className="text-sm text-red-600">
                      <strong>Erreur:</strong> {result.error}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {/* Résumé */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Résumé</h3>
              <div className="grid grid-cols-3 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    {results.length}
                  </div>
                  <div className="text-sm text-gray-600">Tests effectués</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">
                    {results.filter(r => r.success).length}
                  </div>
                  <div className="text-sm text-gray-600">Tests réussis</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-600">
                    {results.filter(r => !r.success).length}
                  </div>
                  <div className="text-sm text-gray-600">Tests échoués</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Instructions */}
        <div className="mt-8 bg-blue-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-4">Instructions</h3>
          <div className="text-sm text-blue-800 space-y-2">
            <p>• Ce composant teste la méthode <code>getMemberEvolution</code> avec différents scénarios de paramètres</p>
            <p>• Les tests vérifient que l'endpoint fonctionne correctement même sans paramètres</p>
            <p>• Chaque test affiche les données récupérées ou l'erreur rencontrée</p>
            <p>• Consultez la console pour plus de détails sur les requêtes effectuées</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MemberEvolutionTest; 