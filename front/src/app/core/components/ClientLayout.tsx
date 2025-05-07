'use client';

import { ReactNode, useState } from 'react';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import { SidebarProvider, useSidebar } from './SidebarProvider';

interface ClientLayoutProps {
  children: ReactNode;
}

function LayoutContent({ children }: ClientLayoutProps) {
  const { isCollapsed } = useSidebar();
  const [isAuthenticated, setIsAuthenticated] = useState(true);

  return (
    <div className="flex min-h-screen bg-gray-900">
      <Sidebar 
        isAuthenticated={isAuthenticated}
        user={{
          name: 'Usuário Teste',
          email: 'usuario@teste.com'
        }}
      />
      <div className="flex-1 flex flex-col bg-purple-50 dark:bg-gray-900">
        <Navbar 
          isAuthenticated={isAuthenticated}
          onToggleAuth={() => setIsAuthenticated(!isAuthenticated)}
        />
        <main className={`flex-1 transition-all duration-300 ${isCollapsed ? 'ml-20' : 'ml-80'}`}>
          <div className="max-w-7xl mx-auto p-6">
            {children}
          </div>
        </main>
        <footer className={`bg-white dark:bg-gray-800 shadow-md transition-all duration-300 ${isCollapsed ? 'ml-20' : 'ml-80'} border-t border-gray-200 dark:border-gray-700`}>
          <div className="max-w-7xl mx-auto p-4">
            <p className="text-center text-gray-600 dark:text-gray-300">© 2024 Viixen. Todos os direitos reservados.</p>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default function ClientLayout({ children }: ClientLayoutProps) {
  return (
    <SidebarProvider>
      <LayoutContent>{children}</LayoutContent>
    </SidebarProvider>
  );
} 