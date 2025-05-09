// app/layout.tsx
import './core/styles/globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import ClientLayout from './core/components/ClientLayout';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Viixen',
  description: 'Plataforma de gerenciamento de conteúdo',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <head>
        {/* Script para aplicar o tema salvo ou o tema escuro por padrão */}
        <script dangerouslySetInnerHTML={{
          __html: `
            (function() {
              // Verificar se há um tema salvo no localStorage
              const savedTheme = localStorage.getItem('theme');
              // Se houver um tema salvo, use-o, caso contrário, use o tema escuro como padrão
              if (savedTheme) {
                document.documentElement.classList.add(savedTheme);
              } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('theme', 'dark');
              }
            })();
          `
        }} />
      </head>
      <body className={`${inter.className} bg-purple-50 dark:bg-gray-900`}>
        <ClientLayout>{children}</ClientLayout>
      </body>
    </html>
  );
}