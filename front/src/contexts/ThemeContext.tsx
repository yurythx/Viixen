'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';

// Mantemos os tipos para compatibilidade, mas só usaremos 'dark'
type Theme = 'light' | 'dark' | 'sepia';
type ThemeColor = 'blue' | 'purple' | 'green' | 'red' | 'orange';

interface ThemeContextType {
  theme: Theme;
  themeColor: ThemeColor;
  setTheme: (theme: Theme) => void;
  setThemeColor: (color: ThemeColor) => void;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<Theme>('dark');
  const [themeColor, setThemeColor] = useState<ThemeColor>('blue');

  // Inicializar tema do localStorage ou usar dark como padrão
  useEffect(() => {
    // Executar apenas no cliente para evitar erros de hidratação
    if (typeof window === 'undefined') return;

    // Verificar se há um tema salvo no localStorage
    const savedTheme = localStorage.getItem('theme') as Theme | null;
    const savedColor = localStorage.getItem('themeColor') as ThemeColor | null;

    // Se houver um tema salvo, use-o, caso contrário, mantenha o dark como padrão
    if (savedTheme) {
      setTheme(savedTheme);
    } else {
      // Sempre iniciar com o tema escuro e salvar no localStorage
      localStorage.setItem('theme', 'dark');
    }

    if (savedColor) {
      setThemeColor(savedColor);
    }
  }, []);

  // Aplicar tema ao documento
  useEffect(() => {
    // Executar apenas no cliente para evitar erros de hidratação
    if (typeof window === 'undefined') return;

    const root = document.documentElement;

    // Remover todas as classes de tema
    root.classList.remove('light', 'dark', 'sepia');

    // Adicionar a classe do tema atual
    root.classList.add(theme);

    // Salvar no localStorage
    localStorage.setItem('theme', theme);

    // Atualizar a meta tag theme-color para dispositivos móveis
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
      if (theme === 'dark') {
        metaThemeColor.setAttribute('content', '#1f2937');
      } else if (theme === 'light') {
        metaThemeColor.setAttribute('content', '#ffffff');
      } else if (theme === 'sepia') {
        metaThemeColor.setAttribute('content', '#f8f3e3');
      }
    }
  }, [theme]);

  // Aplicar cor do tema
  useEffect(() => {
    // Executar apenas no cliente para evitar erros de hidratação
    if (typeof window === 'undefined') return;

    const root = document.documentElement;

    // Remover todas as classes de cor
    root.classList.remove('theme-blue', 'theme-purple', 'theme-green', 'theme-red', 'theme-orange');

    // Adicionar a classe da cor atual
    root.classList.add(`theme-${themeColor}`);

    // Salvar no localStorage
    localStorage.setItem('themeColor', themeColor);

    // Remover variáveis existentes para garantir que não haja conflitos
    root.style.removeProperty('--primary-color');
    root.style.removeProperty('--primary-hover');
    root.style.removeProperty('--primary-color-rgb');

    switch (themeColor) {
      case 'blue':
        root.style.setProperty('--primary-color', '#4f46e5');
        root.style.setProperty('--primary-hover', '#4338ca');
        root.style.setProperty('--primary-color-rgb', '79, 70, 229');
        break;
      case 'purple':
        root.style.setProperty('--primary-color', '#8b5cf6');
        root.style.setProperty('--primary-hover', '#7c3aed');
        root.style.setProperty('--primary-color-rgb', '139, 92, 246');
        break;
      case 'green':
        root.style.setProperty('--primary-color', '#10b981');
        root.style.setProperty('--primary-hover', '#059669');
        root.style.setProperty('--primary-color-rgb', '16, 185, 129');
        break;
      case 'red':
        root.style.setProperty('--primary-color', '#ef4444');
        root.style.setProperty('--primary-hover', '#dc2626');
        root.style.setProperty('--primary-color-rgb', '239, 68, 68');
        break;
      case 'orange':
        root.style.setProperty('--primary-color', '#f97316');
        root.style.setProperty('--primary-hover', '#ea580c');
        root.style.setProperty('--primary-color-rgb', '249, 115, 22');
        break;
      default:
        root.style.setProperty('--primary-color', '#4f46e5');
        root.style.setProperty('--primary-hover', '#4338ca');
        root.style.setProperty('--primary-color-rgb', '79, 70, 229');
    }

    // Variáveis CSS definidas com sucesso
  }, [themeColor]);

  // Função de alternância de tema
  const toggleTheme = () => {
    // Alternar entre os temas disponíveis
    if (theme === 'light') {
      setTheme('dark');
    } else if (theme === 'dark') {
      setTheme('sepia');
    } else {
      setTheme('light');
    }
  };

  return (
    <ThemeContext.Provider value={{ theme, themeColor, setTheme, setThemeColor, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);

  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }

  return context;
};
