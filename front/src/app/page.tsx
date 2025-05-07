'use client';

// app/page.tsx
import { useState } from 'react';
import { Plus, FileText, BookOpen } from 'lucide-react';

export default function Home() {
  const [isAuthenticated, setIsAuthenticated] = useState(true);

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Artigos</h1>
        <button
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors"
          onClick={() => {/* Adicionar lógica de criação */}}
        >
          <Plus className="w-5 h-5" />
          Novo Artigo
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Card de Artigo */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Como Criar um Blog com Next.js
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                Um guia completo para criar um blog moderno usando Next.js, Tailwind CSS e TypeScript.
              </p>
              <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
                <span className="flex items-center gap-1">
                  <FileText className="w-4 h-4" />
                  Artigo
                </span>
                <span>5 min de leitura</span>
              </div>
            </div>
          </div>
        </div>

        {/* Card de Artigo */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Introdução ao TypeScript
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                Aprenda os conceitos básicos do TypeScript e como ele pode melhorar seu desenvolvimento.
              </p>
              <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
                <span className="flex items-center gap-1">
                  <FileText className="w-4 h-4" />
                  Artigo
                </span>
                <span>8 min de leitura</span>
              </div>
            </div>
          </div>
        </div>

        {/* Card de Artigo */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Tailwind CSS: Guia Definitivo
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                Domine o Tailwind CSS e crie interfaces modernas com facilidade.
              </p>
              <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
                <span className="flex items-center gap-1">
                  <FileText className="w-4 h-4" />
                  Artigo
                </span>
                <span>6 min de leitura</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}