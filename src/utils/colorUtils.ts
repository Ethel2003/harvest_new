/**
 * Utilitaire pour la gestion des couleurs
 * Convertit les valeurs numériques de couleur du backend en codes couleur hexadécimaux
 */

// Palette de couleurs prédéfinies pour les groupes et départements
export const COLOR_PALETTE = {
  // Couleurs vives et modernes
  '1': '#FF6B6B',   // Rouge corail
  '2': '#4ECDC4',   // Turquoise
  '3': '#45B7D1',   // Bleu ciel
  '4': '#96CEB4',   // Vert menthe
  '5': '#FFEAA7',   // Jaune doux
  '6': '#DDA0DD',   // Prune
  '7': '#98D8C8',   // Vert sauge
  '8': '#F7DC6F',   // Jaune doré
  '9': '#BB8FCE',   // Violet lavande
  '10': '#85C1E9',  // Bleu clair
  '11': '#F8C471',  // Orange doux
  '12': '#82E0AA',  // Vert pomme
  '13': '#F1948A',  // Rose saumon
  '14': '#85C1E9',  // Bleu ciel
  '15': '#F7DC6F',  // Jaune doré
  '16': '#D7BDE2',  // Violet clair
  '17': '#A9DFBF',  // Vert pastel
  '18': '#FAD7A0',  // Orange pastel
  '19': '#AED6F1',  // Bleu pastel
  '20': '#F9E79F',  // Jaune pastel
  
  // Couleurs supplémentaires pour plus de variété
  '21': '#E8DAEF',  // Violet très clair
  '22': '#D5F4E6',  // Vert très clair
  '23': '#FDEBD0',  // Orange très clair
  '24': '#D6EAF8',  // Bleu très clair
  '25': '#FCF3CF',  // Jaune très clair
  '26': '#D2B4DE',  // Violet moyen
  '27': '#A2D9CE',  // Vert moyen
  '28': '#F8C471',  // Orange moyen
  '29': '#85C1E9',  // Bleu moyen
  '30': '#F7DC6F',  // Jaune moyen
} as const;

// Couleurs par défaut pour les cas non définis
export const DEFAULT_COLORS = {
  primary: '#3B82F6',    // Bleu principal
  secondary: '#6B7280',  // Gris secondaire
  success: '#10B981',    // Vert succès
  warning: '#F59E0B',    // Orange avertissement
  danger: '#EF4444',     // Rouge danger
  info: '#06B6D4',       // Cyan info
  light: '#F3F4F6',      // Gris clair
  dark: '#1F2937',       // Gris foncé
} as const;

/**
 * Convertit une valeur de couleur (string ou number) en code couleur hexadécimal
 * @param colorValue - La valeur de couleur du backend (peut être un string ou number)
 * @param fallbackColor - Couleur de fallback si la conversion échoue
 * @returns Le code couleur hexadécimal
 */
export function convertColorToHex(
  colorValue: string | number | null | undefined,
  fallbackColor: string = DEFAULT_COLORS.primary
): string {
  // Si la valeur est null, undefined ou vide, retourner la couleur de fallback
  if (!colorValue) {
    return fallbackColor;
  }

  // Convertir en string pour la cohérence
  const colorString = String(colorValue).trim();

  // Si c'est déjà un code hexadécimal valide, le retourner tel quel
  if (isValidHexColor(colorString)) {
    return colorString;
  }

  // Si c'est une valeur numérique dans notre palette, la convertir
  if (COLOR_PALETTE[colorString as keyof typeof COLOR_PALETTE]) {
    return COLOR_PALETTE[colorString as keyof typeof COLOR_PALETTE];
  }

  // Si c'est un nombre, essayer de le mapper à notre palette
  const numericValue = parseInt(colorString, 10);
  if (!isNaN(numericValue)) {
    // Utiliser le modulo pour mapper à notre palette
    const paletteKey = String((numericValue % Object.keys(COLOR_PALETTE).length) + 1);
    if (COLOR_PALETTE[paletteKey as keyof typeof COLOR_PALETTE]) {
      return COLOR_PALETTE[paletteKey as keyof typeof COLOR_PALETTE];
    }
  }

  // Si rien ne fonctionne, générer une couleur basée sur la valeur
  return generateColorFromString(colorString);
}

/**
 * Vérifie si une chaîne est un code couleur hexadécimal valide
 * @param color - La chaîne à vérifier
 * @returns true si c'est un code hexadécimal valide
 */
export function isValidHexColor(color: string): boolean {
  const hexColorRegex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/;
  return hexColorRegex.test(color);
}

/**
 * Génère une couleur basée sur une chaîne de caractères
 * @param str - La chaîne de base
 * @returns Un code couleur hexadécimal
 */
export function generateColorFromString(str: string): string {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  
  // Générer des couleurs plus douces et harmonieuses
  const hue = Math.abs(hash) % 360;
  const saturation = 60 + (Math.abs(hash) % 20); // 60-80%
  const lightness = 50 + (Math.abs(hash) % 20);  // 50-70%
  
  return hslToHex(hue, saturation, lightness);
}

/**
 * Convertit HSL en hexadécimal
 * @param h - Teinte (0-360)
 * @param s - Saturation (0-100)
 * @param l - Luminosité (0-100)
 * @returns Code couleur hexadécimal
 */
export function hslToHex(h: number, s: number, l: number): string {
  s /= 100;
  l /= 100;

  const c = (1 - Math.abs(2 * l - 1)) * s;
  const x = c * (1 - Math.abs((h / 60) % 2 - 1));
  const m = l - c / 2;
  let r = 0, g = 0, b = 0;

  if (0 <= h && h < 60) {
    r = c; g = x; b = 0;
  } else if (60 <= h && h < 120) {
    r = x; g = c; b = 0;
  } else if (120 <= h && h < 180) {
    r = 0; g = c; b = x;
  } else if (180 <= h && h < 240) {
    r = 0; g = x; b = c;
  } else if (240 <= h && h < 300) {
    r = x; g = 0; b = c;
  } else if (300 <= h && h < 360) {
    r = c; g = 0; b = x;
  }

  const rHex = Math.round((r + m) * 255).toString(16).padStart(2, '0');
  const gHex = Math.round((g + m) * 255).toString(16).padStart(2, '0');
  const bHex = Math.round((b + m) * 255).toString(16).padStart(2, '0');

  return `#${rHex}${gHex}${bHex}`;
}

/**
 * Obtient une couleur contrastée (noir ou blanc) pour un fond donné
 * @param backgroundColor - La couleur de fond
 * @returns '#000000' pour les fonds clairs, '#FFFFFF' pour les fonds foncés
 */
export function getContrastColor(backgroundColor: string): string {
  // Convertir la couleur hex en RGB
  const hex = backgroundColor.replace('#', '');
  const r = parseInt(hex.substr(0, 2), 16);
  const g = parseInt(hex.substr(2, 2), 16);
  const b = parseInt(hex.substr(4, 2), 16);
  
  // Calculer la luminance relative
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  
  // Retourner noir ou blanc selon la luminance
  return luminance > 0.5 ? '#000000' : '#FFFFFF';
}

/**
 * Assombrit une couleur
 * @param color - La couleur à assombrir
 * @param amount - Le pourcentage d'assombrissement (0-100)
 * @returns La couleur assombrie
 */
export function darkenColor(color: string, amount: number = 20): string {
  const hex = color.replace('#', '');
  const r = parseInt(hex.substr(0, 2), 16);
  const g = parseInt(hex.substr(2, 2), 16);
  const b = parseInt(hex.substr(4, 2), 16);
  
  const factor = 1 - (amount / 100);
  const newR = Math.round(r * factor);
  const newG = Math.round(g * factor);
  const newB = Math.round(b * factor);
  
  return `#${newR.toString(16).padStart(2, '0')}${newG.toString(16).padStart(2, '0')}${newB.toString(16).padStart(2, '0')}`;
}

/**
 * Éclaircit une couleur
 * @param color - La couleur à éclaircir
 * @param amount - Le pourcentage d'éclaircissement (0-100)
 * @returns La couleur éclaircie
 */
export function lightenColor(color: string, amount: number = 20): string {
  const hex = color.replace('#', '');
  const r = parseInt(hex.substr(0, 2), 16);
  const g = parseInt(hex.substr(2, 2), 16);
  const b = parseInt(hex.substr(4, 2), 16);
  
  const factor = 1 + (amount / 100);
  const newR = Math.min(255, Math.round(r * factor));
  const newG = Math.min(255, Math.round(g * factor));
  const newB = Math.min(255, Math.round(b * factor));
  
  return `#${newR.toString(16).padStart(2, '0')}${newG.toString(16).padStart(2, '0')}${newB.toString(16).padStart(2, '0')}`;
}

/**
 * Obtient une couleur avec transparence
 * @param color - La couleur de base
 * @param alpha - Le niveau de transparence (0-1)
 * @returns La couleur avec transparence au format rgba
 */
export function getColorWithAlpha(color: string, alpha: number = 0.1): string {
  const hex = color.replace('#', '');
  const r = parseInt(hex.substr(0, 2), 16);
  const g = parseInt(hex.substr(2, 2), 16);
  const b = parseInt(hex.substr(4, 2), 16);
  
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

/**
 * Obtient une couleur de la palette par index
 * @param index - L'index de la couleur (1-30)
 * @returns La couleur de la palette ou une couleur par défaut
 */
export function getColorByIndex(index: number): string {
  const key = String(index);
  return COLOR_PALETTE[key as keyof typeof COLOR_PALETTE] || DEFAULT_COLORS.primary;
}

/**
 * Obtient une couleur aléatoire de la palette
 * @returns Une couleur aléatoire de la palette
 */
export function getRandomColor(): string {
  const keys = Object.keys(COLOR_PALETTE);
  const randomKey = keys[Math.floor(Math.random() * keys.length)];
  return COLOR_PALETTE[randomKey as keyof typeof COLOR_PALETTE];
}

/**
 * Obtient une couleur basée sur le nom (pour la cohérence)
 * @param name - Le nom de l'élément
 * @returns Une couleur basée sur le nom
 */
export function getColorByName(name: string): string {
  if (!name) return DEFAULT_COLORS.primary;
  
  // Générer une couleur basée sur le nom pour la cohérence
  return generateColorFromString(name.toLowerCase());
}

// Export des types pour TypeScript
export type ColorPaletteKey = keyof typeof COLOR_PALETTE;
export type DefaultColorKey = keyof typeof DEFAULT_COLORS; 