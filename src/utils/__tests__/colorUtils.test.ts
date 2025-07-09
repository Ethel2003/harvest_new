import {
  convertColorToHex,
  getColorByIndex,
  getRandomColor,
  getColorByName,
  getContrastColor,
  darkenColor,
  lightenColor,
  getColorWithAlpha,
  isValidHexColor,
  generateColorFromString,
  COLOR_PALETTE,
  DEFAULT_COLORS
} from '../colorUtils';

describe('Color Utils', () => {
  describe('convertColorToHex', () => {
    it('should convert numeric string values to hex colors', () => {
      expect(convertColorToHex('1')).toBe('#FF6B6B');
      expect(convertColorToHex('2')).toBe('#4ECDC4');
      expect(convertColorToHex('5')).toBe('#FFEAA7');
    });

    it('should return hex colors unchanged', () => {
      expect(convertColorToHex('#FF0000')).toBe('#FF0000');
      expect(convertColorToHex('#00FF00')).toBe('#00FF00');
      expect(convertColorToHex('#0000FF')).toBe('#0000FF');
    });

    it('should handle null and undefined values', () => {
      expect(convertColorToHex(null)).toBe(DEFAULT_COLORS.primary);
      expect(convertColorToHex(undefined)).toBe(DEFAULT_COLORS.primary);
      expect(convertColorToHex('')).toBe(DEFAULT_COLORS.primary);
    });

    it('should handle numeric values', () => {
      expect(convertColorToHex(1)).toBe('#FF6B6B');
      expect(convertColorToHex(2)).toBe('#4ECDC4');
      expect(convertColorToHex(5)).toBe('#FFEAA7');
    });

    it('should handle values outside the palette range', () => {
      const result1 = convertColorToHex('999');
      const result2 = convertColorToHex('abc');
      
      expect(result1).toMatch(/^#[0-9A-Fa-f]{6}$/);
      expect(result2).toMatch(/^#[0-9A-Fa-f]{6}$/);
    });

    it('should use custom fallback color', () => {
      expect(convertColorToHex(null, '#CUSTOM')).toBe('#CUSTOM');
      expect(convertColorToHex(undefined, '#CUSTOM')).toBe('#CUSTOM');
    });
  });

  describe('getColorByIndex', () => {
    it('should return colors from palette by index', () => {
      expect(getColorByIndex(1)).toBe('#FF6B6B');
      expect(getColorByIndex(2)).toBe('#4ECDC4');
      expect(getColorByIndex(5)).toBe('#FFEAA7');
    });

    it('should return default color for invalid index', () => {
      expect(getColorByIndex(999)).toBe(DEFAULT_COLORS.primary);
      expect(getColorByIndex(0)).toBe(DEFAULT_COLORS.primary);
      expect(getColorByIndex(-1)).toBe(DEFAULT_COLORS.primary);
    });
  });

  describe('getColorByName', () => {
    it('should generate consistent colors for same names', () => {
      const color1 = getColorByName('Groupe A');
      const color2 = getColorByName('Groupe A');
      expect(color1).toBe(color2);
    });

    it('should generate different colors for different names', () => {
      const color1 = getColorByName('Groupe A');
      const color2 = getColorByName('Groupe B');
      expect(color1).not.toBe(color2);
    });

    it('should return default color for empty names', () => {
      expect(getColorByName('')).toBe(DEFAULT_COLORS.primary);
    });

    it('should generate valid hex colors', () => {
      const color = getColorByName('Test Name');
      expect(color).toMatch(/^#[0-9A-Fa-f]{6}$/);
    });
  });

  describe('getRandomColor', () => {
    it('should return a color from the palette', () => {
      const color = getRandomColor();
      const paletteValues = Object.values(COLOR_PALETTE);
      expect(paletteValues).toContain(color);
    });

    it('should return valid hex color', () => {
      const color = getRandomColor();
      expect(color).toMatch(/^#[0-9A-Fa-f]{6}$/);
    });
  });

  describe('getContrastColor', () => {
    it('should return black for light backgrounds', () => {
      expect(getContrastColor('#FFFFFF')).toBe('#000000');
      expect(getContrastColor('#FF6B6B')).toBe('#000000');
      expect(getContrastColor('#FFEAA7')).toBe('#000000');
    });

    it('should return white for dark backgrounds', () => {
      expect(getContrastColor('#000000')).toBe('#FFFFFF');
      expect(getContrastColor('#1F2937')).toBe('#FFFFFF');
      expect(getContrastColor('#374151')).toBe('#FFFFFF');
    });
  });

  describe('darkenColor', () => {
    it('should darken colors by specified amount', () => {
      const original = '#FF6B6B';
      const darkened = darkenColor(original, 30);
      
      // The darkened color should be darker than the original
      expect(darkened).toMatch(/^#[0-9A-Fa-f]{6}$/);
      expect(darkened).not.toBe(original);
    });

    it('should handle edge cases', () => {
      expect(darkenColor('#000000', 50)).toBe('#000000'); // Can't darken black
      expect(darkenColor('#FFFFFF', 0)).toBe('#FFFFFF'); // No change
    });
  });

  describe('lightenColor', () => {
    it('should lighten colors by specified amount', () => {
      const original = '#FF6B6B';
      const lightened = lightenColor(original, 30);
      
      // The lightened color should be lighter than the original
      expect(lightened).toMatch(/^#[0-9A-Fa-f]{6}$/);
      expect(lightened).not.toBe(original);
    });

    it('should handle edge cases', () => {
      expect(lightenColor('#FFFFFF', 50)).toBe('#FFFFFF'); // Can't lighten white
      expect(lightenColor('#000000', 0)).toBe('#000000'); // No change
    });
  });

  describe('getColorWithAlpha', () => {
    it('should add transparency to colors', () => {
      const result = getColorWithAlpha('#FF6B6B', 0.5);
      expect(result).toBe('rgba(255, 107, 107, 0.5)');
    });

    it('should handle different alpha values', () => {
      expect(getColorWithAlpha('#FF0000', 0)).toBe('rgba(255, 0, 0, 0)');
      expect(getColorWithAlpha('#00FF00', 1)).toBe('rgba(0, 255, 0, 1)');
      expect(getColorWithAlpha('#0000FF', 0.3)).toBe('rgba(0, 0, 255, 0.3)');
    });
  });

  describe('isValidHexColor', () => {
    it('should validate correct hex colors', () => {
      expect(isValidHexColor('#FF0000')).toBe(true);
      expect(isValidHexColor('#00FF00')).toBe(true);
      expect(isValidHexColor('#0000FF')).toBe(true);
      expect(isValidHexColor('#123456')).toBe(true);
      expect(isValidHexColor('#abcdef')).toBe(true);
      expect(isValidHexColor('#ABC')).toBe(true); // 3-digit hex
    });

    it('should reject invalid hex colors', () => {
      expect(isValidHexColor('FF0000')).toBe(false); // Missing #
      expect(isValidHexColor('#GG0000')).toBe(false); // Invalid characters
      expect(isValidHexColor('#FF00')).toBe(false); // Wrong length
      expect(isValidHexColor('#FF00000')).toBe(false); // Wrong length
      expect(isValidHexColor('')).toBe(false);
      expect(isValidHexColor('#')).toBe(false);
    });
  });

  describe('generateColorFromString', () => {
    it('should generate consistent colors for same strings', () => {
      const color1 = generateColorFromString('test');
      const color2 = generateColorFromString('test');
      expect(color1).toBe(color2);
    });

    it('should generate different colors for different strings', () => {
      const color1 = generateColorFromString('test1');
      const color2 = generateColorFromString('test2');
      expect(color1).not.toBe(color2);
    });

    it('should generate valid hex colors', () => {
      const color = generateColorFromString('test string');
      expect(color).toMatch(/^#[0-9A-Fa-f]{6}$/);
    });
  });

  describe('COLOR_PALETTE', () => {
    it('should contain valid hex colors', () => {
      Object.values(COLOR_PALETTE).forEach(color => {
        expect(color).toMatch(/^#[0-9A-Fa-f]{6}$/);
      });
    });

    it('should have 30 colors', () => {
      expect(Object.keys(COLOR_PALETTE)).toHaveLength(30);
    });

    it('should have string keys from 1 to 30', () => {
      const keys = Object.keys(COLOR_PALETTE);
      for (let i = 1; i <= 30; i++) {
        expect(keys).toContain(String(i));
      }
    });
  });

  describe('DEFAULT_COLORS', () => {
    it('should contain valid hex colors', () => {
      Object.values(DEFAULT_COLORS).forEach(color => {
        expect(color).toMatch(/^#[0-9A-Fa-f]{6}$/);
      });
    });

    it('should have expected color keys', () => {
      const expectedKeys = ['primary', 'secondary', 'success', 'warning', 'danger', 'info', 'light', 'dark'];
      expectedKeys.forEach(key => {
        expect(DEFAULT_COLORS).toHaveProperty(key);
      });
    });
  });
}); 