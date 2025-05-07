'use client';

import { ReactNode, useState, useEffect } from 'react';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import { SidebarProvider, useSidebar } from './SidebarProvider';
import { AuthProvider, useAuth } from '../contexts/AuthContext';
import { NotificationProvider } from '../contexts/NotificationContext';
import ErrorBoundary from './ErrorBoundary';

interface ClientLayoutProps {
  children: ReactNode;
}

function LayoutContent({ children }: ClientLayoutProps) {
  const { isCollapsed } = useSidebar();
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <div className="flex min-h-screen bg-gray-900">
      <Sidebar
        isAuthenticated={isAuthenticated}
        user={user ? {
          name: user.first_name ? `${user.first_name} ${user.last_name}` : user.username,
          email: user.email
        } : null}
      />
      <div className={`flex-1 flex flex-col bg-purple-50 dark:bg-gray-900 transition-all duration-300 ${isCollapsed ? 'ml-20' : 'ml-80'}`}>
        <Navbar
          isAuthenticated={isAuthenticated}
          onToggleAuth={() => isAuthenticated ? logout() : null}
        />
        <main className="flex-1">
          <div className="max-w-7xl mx-auto p-6">
            {children}
          </div>
        </main>
        <footer className="bg-white dark:bg-gray-800 shadow-md border-t border-gray-200 dark:border-gray-700">
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
    <ErrorBoundary>
      <AuthProvider>
        <NotificationProvider>
          <SidebarProvider>
            <LayoutContent>{children}</LayoutContent>
          </SidebarProvider>
        </NotificationProvider>
      </AuthProvider>
    </ErrorBoundary>
  );
}