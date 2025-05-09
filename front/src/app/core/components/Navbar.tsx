'use client';

import { LogIn, LogOut, Moon, Sun, User, UserPlus } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useSidebar } from './SidebarProvider';
import Link from 'next/link';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import ThemeSettings from '../../components/ThemeSettings';

interface NavbarProps {
  isAuthenticated: boolean;
  onToggleAuth: () => void;
}

export default function Navbar({ isAuthenticated, onToggleAuth }: NavbarProps) {
  const { isCollapsed } = useSidebar();
  const { user } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="bg-white dark:bg-gray-800 shadow-md flex justify-between items-center transition-all duration-300 border-b border-gray-200 dark:border-gray-700">
      <div className="flex items-center gap-4 p-4">
        {!isCollapsed && (
          <h1 className="text-2xl font-semibold text-purple-600 dark:text-indigo-300">Viixen</h1>
        )}
      </div>

      <div className="flex items-center gap-4 p-4">
        <ThemeSettings />

        <button
          onClick={toggleTheme}
          className="p-2 text-gray-600 dark:text-gray-200 hover:text-purple-600 dark:hover:text-indigo-400 transition rounded-lg hover:bg-purple-50 dark:hover:bg-gray-700"
          title="Alternar tema"
        >
          {theme === 'dark' ? (
            <Sun className="w-6 h-6" title="Mudar para tema sepia" />
          ) : theme === 'light' ? (
            <Moon className="w-6 h-6" title="Mudar para tema escuro" />
          ) : (
            <Sun className="w-6 h-6" title="Mudar para tema claro" />
          )}
        </button>

        {isAuthenticated ? (
          <>
            <Link
              href="/perfil"
              className="p-2 text-gray-600 dark:text-gray-200 hover:text-purple-600 dark:hover:text-indigo-400 transition rounded-lg hover:bg-purple-50 dark:hover:bg-gray-700"
              title="Perfil"
            >
              <User className="w-6 h-6" />
            </Link>
            <button
              onClick={onToggleAuth}
              className="p-2 text-gray-600 dark:text-gray-200 hover:text-purple-600 dark:hover:text-indigo-400 transition rounded-lg hover:bg-purple-50 dark:hover:bg-gray-700"
              title="Sair"
            >
              <LogOut className="w-6 h-6" />
            </button>
          </>
        ) : (
          <>
            <Link
              href="/login"
              className="p-2 text-gray-600 dark:text-gray-200 hover:text-purple-600 dark:hover:text-indigo-400 transition rounded-lg hover:bg-purple-50 dark:hover:bg-gray-700"
              title="Entrar"
            >
              <LogIn className="w-6 h-6" />
            </Link>
            <Link
              href="/registro"
              className="p-2 text-gray-600 dark:text-gray-200 hover:text-purple-600 dark:hover:text-indigo-400 transition rounded-lg hover:bg-purple-50 dark:hover:bg-gray-700"
              title="Registrar"
            >
              <UserPlus className="w-6 h-6" />
            </Link>
          </>
        )}
      </div>
    </header>
  );
}