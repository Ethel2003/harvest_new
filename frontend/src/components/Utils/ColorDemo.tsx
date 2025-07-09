import React, { useState } from 'react';
import {
  convertColorToHex,
  getColorByIndex,
  getRandomColor,
  getColorByName,
  getContrastColor,
  darkenColor,
  lightenColor,
  getColorWithAlpha,
  COLOR_PALETTE,
  DEFAULT_COLORS
} from '../../utils/colorUtils';

const ColorDemo: React.FC = () => {
  const [testValue, setTestValue] = useState('1');
  const [testName, setTestName] = useState('Groupe A');

  const handleTestConversion = () => {
    const result = convertColorToHex(testValue);
    console.log(`Conversion de "${testValue}" vers: ${result}`);
    alert(`Conversion de "${testValue}" vers: ${result}`);
  };

  const handleTestNameColor = () => {
    const result = getColorByName(testName);
    console.log(`Couleur pour "${testName}": ${result}`);
    alert(`Couleur pour "${testName}": ${result}`);
  };

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Démonstration des Utilitaires de Couleur</h1>

        {/* Section de test de conversion */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Test de Conversion de Couleur</h2>
          <div className="flex gap-4 items-end">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Valeur à convertir:
              </label>
              <input
                type="text"
                value={testValue}
                onChange={(e) => setTestValue(e.target.value)}
                className="border border-gray-300 rounded-md px-3 py-2 w-32"
                placeholder="1, 2, 3..."
              />
            </div>
            <button
              onClick={handleTestConversion}
              className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
            >
              Tester la conversion
            </button>
          </div>
        </div>

        {/* Section de test de couleur par nom */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Test de Couleur par Nom</h2>
          <div className="flex gap-4 items-end">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nom de l'élément:
              </label>
              <input
                type="text"
                value={testName}
                onChange={(e) => setTestName(e.target.value)}
                className="border border-gray-300 rounded-md px-3 py-2 w-48"
                placeholder="Nom du groupe/département"
              />
            </div>
            <button
              onClick={handleTestNameColor}
              className="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600"
            >
              Tester la couleur par nom
            </button>
          </div>
        </div>

        {/* Palette de couleurs */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Palette de Couleurs Prédéfinies</h2>
          <div className="grid grid-cols-10 gap-2">
            {Object.entries(COLOR_PALETTE).map(([key, color]) => (
              <div key={key} className="text-center">
                <div
                  className="w-12 h-12 rounded-lg mx-auto mb-1 border border-gray-300"
                  style={{ backgroundColor: color }}
                />
                <span className="text-xs text-gray-600">{key}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Couleurs par défaut */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Couleurs par Défaut</h2>
          <div className="grid grid-cols-4 gap-4">
            {Object.entries(DEFAULT_COLORS).map(([key, color]) => (
              <div key={key} className="text-center">
                <div
                  className="w-16 h-16 rounded-lg mx-auto mb-2 border border-gray-300"
                  style={{ backgroundColor: color }}
                />
                <span className="text-sm font-medium text-gray-700">{key}</span>
                <div className="text-xs text-gray-500">{color}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Exemples d'utilisation */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Exemples d'Utilisation</h2>
          <div className="space-y-4">
            <div className="p-4 border border-gray-200 rounded-lg">
              <h3 className="font-medium mb-2">Conversion de valeurs numériques:</h3>
              <div className="grid grid-cols-5 gap-2">
                {['1', '2', '3', '4', '5'].map(value => {
                  const color = convertColorToHex(value);
                  return (
                    <div key={value} className="text-center">
                      <div
                        className="w-12 h-12 rounded-lg mx-auto mb-1 border border-gray-300"
                        style={{ backgroundColor: color }}
                      />
                      <span className="text-xs text-gray-600">{value} → {color}</span>
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="p-4 border border-gray-200 rounded-lg">
              <h3 className="font-medium mb-2">Couleurs par nom:</h3>
              <div className="grid grid-cols-4 gap-2">
                {['Groupe A', 'Département B', 'Équipe C', 'Section D'].map(name => {
                  const color = getColorByName(name);
                  return (
                    <div key={name} className="text-center">
                      <div
                        className="w-12 h-12 rounded-lg mx-auto mb-1 border border-gray-300"
                        style={{ backgroundColor: color }}
                      />
                      <span className="text-xs text-gray-600">{name}</span>
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="p-4 border border-gray-200 rounded-lg">
              <h3 className="font-medium mb-2">Variations de couleur:</h3>
              <div className="grid grid-cols-4 gap-2">
                {(() => {
                  const baseColor = '#FF6B6B';
                  return [
                    { name: 'Original', color: baseColor },
                    { name: 'Assombri', color: darkenColor(baseColor, 30) },
                    { name: 'Éclairci', color: lightenColor(baseColor, 30) },
                    { name: 'Transparent', color: getColorWithAlpha(baseColor, 0.3) }
                  ];
                })().map(({ name, color }) => (
                  <div key={name} className="text-center">
                    <div
                      className="w-12 h-12 rounded-lg mx-auto mb-1 border border-gray-300"
                      style={{ backgroundColor: color }}
                    />
                    <span className="text-xs text-gray-600">{name}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Documentation */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4 text-blue-900">Documentation</h2>
          <div className="space-y-2 text-blue-800">
            <p><strong>convertColorToHex(value):</strong> Convertit une valeur numérique en code couleur hexadécimal</p>
            <p><strong>getColorByName(name):</strong> Génère une couleur cohérente basée sur un nom</p>
            <p><strong>getColorByIndex(index):</strong> Obtient une couleur de la palette par index</p>
            <p><strong>getRandomColor():</strong> Retourne une couleur aléatoire de la palette</p>
            <p><strong>getContrastColor(color):</strong> Retourne noir ou blanc selon la luminosité</p>
            <p><strong>darkenColor(color, amount):</strong> Assombrit une couleur</p>
            <p><strong>lightenColor(color, amount):</strong> Éclaircit une couleur</p>
            <p><strong>getColorWithAlpha(color, alpha):</strong> Ajoute de la transparence</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ColorDemo; 