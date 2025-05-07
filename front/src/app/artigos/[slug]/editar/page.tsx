'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../../core/contexts/AuthContext';
import { articlesService } from '../../../core/services/api';
import { Article } from '../../../core/types/models';
import ArticleForm from '../../../core/components/articles/ArticleForm';
import Header from '../../components/Header';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import PermissionGuard from '../../../core/components/auth/PermissionGuard';
import AccessDenied from '../../../core/components/auth/AccessDenied';
import { useNotification } from '../../../core/contexts/NotificationContext';

interface EditarArtigoPageProps {
  params: {
    slug: string;
  };
}

export default function EditarArtigoPage({ params }: EditarArtigoPageProps) {
  const { user } = useAuth();
  const { showNotification } = useNotification();
  const router = useRouter();
  const [article, setArticle] = useState<Article | null>(null);
  const [isLoadingArticle, setIsLoadingArticle] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchArticle = async () => {
      try {
        setIsLoadingArticle(true);
        const data = await articlesService.getArticleBySlug(params.slug);

        if (!data) {
          setError('Artigo não encontrado.');
          showNotification('error', 'Artigo não encontrado.');
          return;
        }

        setArticle(data);
      } catch (err: any) {
        console.error('Erro ao buscar artigo:', err);
        const errorMessage = 'Não foi possível carregar o artigo. Por favor, tente novamente mais tarde.';
        setError(errorMessage);
        showNotification('error', errorMessage);
      } finally {
        setIsLoadingArticle(false);
      }
    };

    fetchArticle();
  }, [params.slug, showNotification]);

  if (isLoadingArticle) {
    return (
      <>
        <Header />
        <div className="container mx-auto px-4 py-8">
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
          </div>
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Header />
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-3xl mx-auto">
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              <p>{error}</p>
              <Link href={`/artigos/${params.slug}`} className="mt-4 inline-flex items-center text-indigo-600 hover:text-indigo-800">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Voltar para o artigo
              </Link>
            </div>
          </div>
        </div>
      </>
    );
  }

  if (!article) {
    return (
      <>
        <Header />
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-3xl mx-auto">
            <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded">
              <p>Artigo não encontrado.</p>
              <Link href="/artigos" className="mt-4 inline-flex items-center text-indigo-600 hover:text-indigo-800">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Voltar para a lista de artigos
              </Link>
            </div>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Header />
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-3xl mx-auto">
          <Link href={`/artigos/${params.slug}`} className="inline-flex items-center text-indigo-600 hover:text-indigo-800 mb-6">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Voltar para o artigo
          </Link>

          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">Editar Artigo</h1>

          <PermissionGuard
            requiredPermission="author"
            resourceOwnerId={article.author_id}
            fallback={
              <AccessDenied
                message="Você não tem permissão para editar este artigo."
                backUrl={`/artigos/${params.slug}`}
                backLabel="Voltar para o artigo"
              />
            }
          >
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
              <ArticleForm
                article={article}
                onSuccess={() => {
                  showNotification('success', 'Artigo atualizado com sucesso!');
                  router.push(`/artigos/${article.slug}`);
                }}
              />
            </div>
          </PermissionGuard>
        </div>
      </div>
    </>
  );
}
