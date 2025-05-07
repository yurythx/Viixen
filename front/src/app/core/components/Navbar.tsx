'use client';

import { LogIn, LogOut, Moon, Sun } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useSidebar } from './SidebarProvider';

interface NavbarProps {
  isAuthenticated: boolean;
  onToggleAuth: () => void;
}

export default function Navbar({ isAuthenticated, onToggleAuth }: NavbarProps) {
  const [darkMode, setDarkMode] = useState(true);
  const { isCollapsed } = useSidebar();

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
      document.documentElement.classList.remove('dark');
      setDarkMode(false);
    } else {
      document.documentElement.classList.add('dark');
      setDarkMode(true);
    }
  }, []);

  const toggleTheme = () => {
    const isDark = !darkMode;
    setDarkMode(isDark);
    if (isDark) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  };

  return (
    <header className={`bg-white dark:bg-gray-800 shadow-md flex justify-between items-center transition-all duration-300 ${isCollapsed ? 'ml-20' : 'ml-80'} border-b border-gray-200 dark:border-gray-700`}>
      <div className="flex items-center gap-4 p-4">
        {!isCollapsed && (
          <h1 className="text-2xl font-semibold text-purple-600 dark:text-indigo-300">Viixen</h1>
        )}
      </div>

      <div className="flex items-center gap-4 p-4">
        <button
          onClick={toggleTheme}
          className="p-2 text-gray-600 dark:text-gray-200 hover:text-purple-600 dark:hover:text-indigo-400 transition rounded-lg hover:bg-purple-50 dark:hover:bg-gray-700"
          title="Alternar tema"
        >
          {darkMode ? <Sun className="w-6 h-6" /> : <Moon className="w-6 h-6" />}
        </button>
        <button
          onClick={onToggleAuth}
          className="p-2 text-gray-600 dark:text-gray-200 hover:text-purple-600 dark:hover:text-indigo-400 transition rounded-lg hover:bg-purple-50 dark:hover:bg-gray-700"
          title={isAuthenticated ? "Sair" : "Entrar"}
        >
          {isAuthenticated ? <LogOut className="w-6 h-6" /> : <LogIn className="w-6 h-6" />}
        </button>
      </div>
    </header>
  );
} 