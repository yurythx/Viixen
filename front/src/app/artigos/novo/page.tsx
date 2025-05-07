'use client';

import { useRouter } from 'next/navigation';
import ArticleForm from '../../core/components/articles/ArticleForm';
import Header from '../components/Header';
import PermissionGuard from '../../core/components/auth/PermissionGuard';
import AccessDenied from '../../core/components/auth/AccessDenied';
import { useNotification } from '../../core/contexts/NotificationContext';

export default function NovoArtigoPage() {
  const router = useRouter();
  const { showNotification } = useNotification();

  return (
    <>
      <Header />
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">Novo Artigo</h1>

          <PermissionGuard
            requiredPermission="authenticated"
            redirectTo="/login?redirect=/artigos/novo"
            fallback={
              <AccessDenied
                message="Você precisa estar logado para criar um artigo."
                backUrl="/artigos"
                backLabel="Voltar para a lista de artigos"
                loginUrl="/login?redirect=/artigos/novo"
              />
            }
          >
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
              <ArticleForm
                onSuccess={() => {
                  showNotification('success', 'Artigo criado com sucesso!');
                  router.push('/artigos');
                }}
              />
            </div>
          </PermissionGuard>
        </div>
      </div>
    </>
  );
}
