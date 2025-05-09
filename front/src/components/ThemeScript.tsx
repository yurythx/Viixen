'use client';

import { useEffect } from 'react';
import Script from 'next/script';

/**
 * Componente que aplica o tema salvo ou o tema escuro por padrão
 * Usando o componente Script do Next.js para evitar problemas de hidratação
 */
export default function ThemeScript() {
  // Este useEffect será executado apenas no cliente
  useEffect(() => {
    // Verificar se há um tema salvo no localStorage
    const savedTheme = localStorage.getItem('theme');
    
    // Se houver um tema salvo, use-o, caso contrário, use o tema escuro como padrão
    if (savedTheme) {
      document.documentElement.classList.add(savedTheme);
    } else {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    }
  }, []);

  return null;
}
