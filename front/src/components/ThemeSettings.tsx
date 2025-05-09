'use client';

import { useState, useEffect } from 'react';
import { Moon, Sun, Settings, Check } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';

export default function ThemeSettings() {
  const { theme, themeColor, setThemeColor, setTheme } = useTheme();
  const [isOpen, setIsOpen] = useState(false);
  const [selectedColor, setSelectedColor] = useState(themeColor);
  const [showFeedback, setShowFeedback] = useState(false);

  // Atualizar o estado local quando o themeColor mudar
  useEffect(() => {
    setSelectedColor(themeColor);
  }, [themeColor]);

  const toggleOpen = () => {
    setIsOpen(!isOpen);
  };

  // Função para aplicar a cor com feedback visual
  const applyThemeColor = (color: 'blue' | 'purple' | 'green' | 'red' | 'orange') => {
    setSelectedColor(color);
    setThemeColor(color);

    // Mostrar feedback visual
    setShowFeedback(true);
    setTimeout(() => {
      setShowFeedback(false);
    }, 1500);
  };

  return (
    <div className="relative">
      <button
        onClick={toggleOpen}
        className="p-2 rounded-full bg-gray-800 hover:bg-gray-700 border border-gray-700 shadow-lg transition-all hover:shadow-xl hover:scale-105 group"
        aria-label="Personalizar tema"
        title="Personalizar tema"
      >
        <Settings className="w-5 h-5 text-gray-300 group-hover:text-white transition-colors" />
      </button>

      {/* Feedback de tema aplicado */}
      {showFeedback && (
        <div className="fixed top-4 right-4 bg-gray-800 text-white px-4 py-2 rounded-lg shadow-lg z-50 animate-fade-in-out">
          <div className="flex items-center space-x-2">
            <Check className="w-4 h-4 text-green-400" />
            <span>
              {selectedColor !== themeColor
                ? `Cor do tema atualizada para ${selectedColor}`
                : theme === 'dark'
                  ? 'Tema escuro aplicado'
                  : theme === 'light'
                    ? 'Tema claro aplicado'
                    : 'Tema sepia aplicado'}
            </span>
          </div>
        </div>
      )}

      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 bg-gray-800 rounded-lg shadow-lg p-4 z-50 border border-gray-700">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-medium text-white">Personalização</h3>
            <button
              onClick={() => setIsOpen(false)}
              className="text-gray-400 hover:text-gray-300 transition-colors"
            >
              ×
            </button>
          </div>

          <div className="space-y-4">
            {/* Informação sobre o tema atual */}
            <div className="bg-gray-700/50 p-2 rounded-lg text-xs text-gray-300 flex items-start space-x-2">
              {theme === 'dark' ? (
                <Moon className="w-4 h-4 mt-0.5 flex-shrink-0" />
              ) : theme === 'light' ? (
                <Sun className="w-4 h-4 mt-0.5 flex-shrink-0" />
              ) : (
                <Settings className="w-4 h-4 mt-0.5 flex-shrink-0" />
              )}
              <p>
                {theme === 'dark'
                  ? 'Modo escuro ativado para melhor experiência visual.'
                  : theme === 'light'
                    ? 'Modo claro ativado.'
                    : 'Modo sepia ativado para leitura confortável.'}
              </p>
            </div>

            {/* Seleção de tema */}
            <div className="mb-4">
              <h4 className="text-sm font-medium text-gray-300 mb-3">Tema</h4>
              <div className="grid grid-cols-3 gap-2">
                <button
                  onClick={() => {
                    setTheme('light');
                    setShowFeedback(true);
                    setTimeout(() => setShowFeedback(false), 1500);
                  }}
                  className={`px-3 py-2 rounded-md flex items-center justify-center transition-all ${
                    theme === 'light'
                      ? 'bg-gray-600 text-white'
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                >
                  <Sun className="w-4 h-4 mr-2" />
                  <span className="text-xs">Claro</span>
                  {theme === 'light' && <Check className="w-3 h-3 ml-1" />}
                </button>
                <button
                  onClick={() => {
                    setTheme('dark');
                    setShowFeedback(true);
                    setTimeout(() => setShowFeedback(false), 1500);
                  }}
                  className={`px-3 py-2 rounded-md flex items-center justify-center transition-all ${
                    theme === 'dark'
                      ? 'bg-gray-600 text-white'
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                >
                  <Moon className="w-4 h-4 mr-2" />
                  <span className="text-xs">Escuro</span>
                  {theme === 'dark' && <Check className="w-3 h-3 ml-1" />}
                </button>
                <button
                  onClick={() => {
                    setTheme('sepia');
                    setShowFeedback(true);
                    setTimeout(() => setShowFeedback(false), 1500);
                  }}
                  className={`px-3 py-2 rounded-md flex items-center justify-center transition-all ${
                    theme === 'sepia'
                      ? 'bg-gray-600 text-white'
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                >
                  <Settings className="w-4 h-4 mr-2" />
                  <span className="text-xs">Sepia</span>
                  {theme === 'sepia' && <Check className="w-3 h-3 ml-1" />}
                </button>
              </div>
            </div>

            {/* Seleção de cor */}
            <div>
              <h4 className="text-sm font-medium text-gray-300 mb-3">Cor do Tema</h4>
              <div className="grid grid-cols-5 gap-3">
                <button
                  onClick={() => applyThemeColor('blue')}
                  className={`w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center transition-transform ${
                    selectedColor === 'blue' ? 'ring-2 ring-offset-2 ring-blue-500 dark:ring-offset-gray-800 scale-110' : 'hover:scale-105'
                  }`}
                  aria-label="Tema azul"
                  style={{ backgroundColor: '#4f46e5' }}
                >
                  {selectedColor === 'blue' && <Check className="w-5 h-5 text-white" />}
                </button>
                <button
                  onClick={() => applyThemeColor('purple')}
                  className={`w-10 h-10 rounded-full bg-purple-600 flex items-center justify-center transition-transform ${
                    selectedColor === 'purple' ? 'ring-2 ring-offset-2 ring-purple-500 dark:ring-offset-gray-800 scale-110' : 'hover:scale-105'
                  }`}
                  aria-label="Tema roxo"
                  style={{ backgroundColor: '#8b5cf6' }}
                >
                  {selectedColor === 'purple' && <Check className="w-5 h-5 text-white" />}
                </button>
                <button
                  onClick={() => applyThemeColor('green')}
                  className={`w-10 h-10 rounded-full bg-green-600 flex items-center justify-center transition-transform ${
                    selectedColor === 'green' ? 'ring-2 ring-offset-2 ring-green-500 dark:ring-offset-gray-800 scale-110' : 'hover:scale-105'
                  }`}
                  aria-label="Tema verde"
                  style={{ backgroundColor: '#10b981' }}
                >
                  {selectedColor === 'green' && <Check className="w-5 h-5 text-white" />}
                </button>
                <button
                  onClick={() => applyThemeColor('red')}
                  className={`w-10 h-10 rounded-full bg-red-600 flex items-center justify-center transition-transform ${
                    selectedColor === 'red' ? 'ring-2 ring-offset-2 ring-red-500 dark:ring-offset-gray-800 scale-110' : 'hover:scale-105'
                  }`}
                  aria-label="Tema vermelho"
                  style={{ backgroundColor: '#ef4444' }}
                >
                  {selectedColor === 'red' && <Check className="w-5 h-5 text-white" />}
                </button>
                <button
                  onClick={() => applyThemeColor('orange')}
                  className={`w-10 h-10 rounded-full bg-orange-600 flex items-center justify-center transition-transform ${
                    selectedColor === 'orange' ? 'ring-2 ring-offset-2 ring-orange-500 dark:ring-offset-gray-800 scale-110' : 'hover:scale-105'
                  }`}
                  aria-label="Tema laranja"
                  style={{ backgroundColor: '#f97316' }}
                >
                  {selectedColor === 'orange' && <Check className="w-5 h-5 text-white" />}
                </button>
              </div>

              <div className="mt-3 text-xs text-gray-400 text-center">
                Clique em uma cor para aplicar ao tema
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
