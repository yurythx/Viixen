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
      <body className={`${inter.className} bg-purple-50 dark:bg-gray-900`}>
        <ClientLayout>{children}</ClientLayout>
      </body>
    </html>
  );
}