import { MD3LightTheme } from 'react-native-paper';

export const theme = {
  ...MD3LightTheme,
  colors: {
    ...MD3LightTheme.colors,
    primary: '#8B6914',
    primaryContainer: '#F5E6D3',
    secondary: '#6B4E2E',
    secondaryContainer: '#FFF3E0',
    background: '#FFFDF8',
    surface: '#FFFFFF',
    surfaceVariant: '#F5F0EB',
    error: '#BA1A1A',
    onPrimary: '#FFFFFF',
    onPrimaryContainer: '#2E1700',
    onBackground: '#1C1B1F',
    onSurface: '#1C1B1F',
    outline: '#C4B8A8',
  },
  roundness: 12,
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

export const fonts = {
  sanskrit: 'serif',
  body: 'System',
};
