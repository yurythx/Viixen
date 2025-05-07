'use client';

import React, { useEffect, useState } from 'react';
import { Article } from '../../core/types/models';
import { articlesService } from '../../core/services/api';
import { ArrowLeft, Calendar, Edit, Tag, User } from 'lucide-react';
import Link from 'next/link';
import CommentList from '../../core/components/articles/CommentList';
import CommentForm from '../../core/components/articles/CommentForm';
import DeleteArticleButton from '../../core/components/articles/DeleteArticleButton';
import { useAuth } from '../../core/contexts/AuthContext';
import { useNotification } from '../../core/contexts/NotificationContext';
import PermissionGuard from '../../core/components/auth/PermissionGuard';

interface ArticlePageProps {
  params: {
    slug: string;
  };
}

export default function ArticlePage({ params }: ArticlePageProps) {
  const { isAuthenticated, user } = useAuth();
  const { showNotification } = useNotification();
  const [article, setArticle] = useState<Article | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchArticle = async () => {
    try {
      setIsLoading(true);
      const data = await articlesService.getArticleBySlug(params.slug);

      if (data) {
        setArticle(data);
        setError(null);
      } else {
        setArticle(null);
        setError('Artigo não encontrado ou ocorreu um erro ao carregar os dados.');
      }
    } catch (err: any) {
      console.error('Erro ao buscar artigo:', err);
      setArticle(null);
      setError('Não foi possível carregar o artigo. Por favor, tente novamente mais tarde.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchArticle();
  }, [params.slug]);

  // Função para formatar a data
  const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('pt-BR', options);
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-8">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          <p>{error}</p>
          <Link href="/artigos" className="mt-4 inline-flex items-center text-indigo-600 hover:text-indigo-800">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Voltar para a lista de artigos
          </Link>
        </div>
      </div>
    );
  }

  if (!article) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-8">
        <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded">
          <p>Artigo não encontrado.</p>
          <Link href="/artigos" className="mt-4 inline-flex items-center text-indigo-600 hover:text-indigo-800">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Voltar para a lista de artigos
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <Link href="/artigos" className="inline-flex items-center text-indigo-600 hover:text-indigo-800">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Voltar para a lista de artigos
        </Link>

        <PermissionGuard
          requiredPermission="author"
          resourceOwnerId={article.author_id}
        >
          <div className="flex space-x-2">
            <Link
              href={`/artigos/${article.slug}/editar`}
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              <Edit className="w-4 h-4 mr-2" />
              Editar
            </Link>
            <DeleteArticleButton slug={article.slug} />
          </div>
        </PermissionGuard>
      </div>

      <article className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">{article.title}</h1>

        <div className="flex flex-wrap items-center text-gray-500 dark:text-gray-400 mb-6 gap-2">
          <div className="flex items-center">
            <Calendar className="w-4 h-4 mr-1" />
            <span>{formatDate(article.created_at)}</span>
          </div>

          {article.author && (
            <div className="flex items-center">
              <span className="mx-2">•</span>
              <User className="w-4 h-4 mr-1" />
              <span>Por {article.author.first_name} {article.author.last_name}</span>
            </div>
          )}

          {article.category && (
            <div className="flex items-center">
              <span className="mx-2">•</span>
              <Tag className="w-4 h-4 mr-1" />
              <span className="text-indigo-600 dark:text-indigo-400">{article.category.name}</span>
            </div>
          )}
        </div>

        <div
          className="prose prose-indigo dark:prose-invert max-w-none"
          dangerouslySetInnerHTML={{ __html: article.content }}
        />
      </article>

      <div className="mt-8">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Deixe um comentário</h2>
        <CommentForm
          articleId={article.id}
          onCommentAdded={fetchArticle}
        />
      </div>

      {article.comments && (
        <CommentList
          comments={article.comments}
          articleId={article.id}
          onCommentAdded={fetchArticle}
        />
      )}
    </div>
  );
}
