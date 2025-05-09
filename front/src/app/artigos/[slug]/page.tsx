'use client';

import React, { useEffect, useState } from 'react';
import { Article } from '../../../types/article.types';
import { articlesService } from '../../../services/api';
import { ArrowLeft, Calendar, Edit, Tag, User, Eye, Heart, Share2, Bookmark, BookmarkCheck, MessageSquare } from 'lucide-react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import CommentList from '../../../components/articles/CommentList';
import CommentForm from '../../../components/articles/CommentForm';
import DeleteArticleButton from '../../../components/articles/DeleteArticleButton';
import { useAuth } from '../../../contexts/AuthContext';
import { useNotification } from '../../../contexts/NotificationContext';

interface ArticlePageProps {
  params: {
    slug: string;
  };
}

export default function ArticlePage({ params }: ArticlePageProps) {
  const router = useRouter();
  const { isAuthenticated, user } = useAuth();
  const { showNotification } = useNotification();
  const [article, setArticle] = useState<Article | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isFavorite, setIsFavorite] = useState(false);
  const [viewCount, setViewCount] = useState(0);
  const [isTogglingFavorite, setIsTogglingFavorite] = useState(false);

  const fetchArticle = async () => {
    try {
      setIsLoading(true);
      const data = await articlesService.getArticleBySlug(params.slug);

      if (data) {
        setArticle(data);
        setViewCount(data.views_count || 0);
        setError(null);

        // Incrementar visualizações
        try {
          const viewsResult = await articlesService.incrementViews(data.id, params.slug);
          if (viewsResult && viewsResult.views_count) {
            setViewCount(viewsResult.views_count);
          }
        } catch (viewErr) {
          console.error('Erro ao incrementar visualizações:', viewErr);
        }
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

  // Verificar se o artigo está nos favoritos do usuário
  const checkIfFavorite = async () => {
    if (!isAuthenticated || !article) return;

    try {
      // Verificar se o artigo está nos favoritos
      const favorites = await articlesService.getMyFavorites();
      const isFav = favorites.some(fav => fav.id === article.id);
      setIsFavorite(isFav);
    } catch (err) {
      console.error('Erro ao verificar favoritos:', err);
    }
  };

  // Alternar favorito
  const handleToggleFavorite = async () => {
    if (!isAuthenticated || !article) {
      showNotification('info', 'Você precisa estar logado para favoritar artigos.');
      return;
    }

    try {
      setIsTogglingFavorite(true);
      const result = await articlesService.toggleFavorite(article.id, params.slug);
      setIsFavorite(result.is_favorite);

      showNotification(
        'success',
        result.is_favorite
          ? 'Artigo adicionado aos favoritos!'
          : 'Artigo removido dos favoritos!'
      );
    } catch (err: any) {
      console.error('Erro ao alternar favorito:', err);
      showNotification('error', 'Não foi possível alterar o status de favorito.');
    } finally {
      setIsTogglingFavorite(false);
    }
  };

  // Compartilhar artigo
  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: article?.title || 'Artigo interessante',
          text: 'Confira este artigo interessante',
          url: window.location.href,
        });
      } catch (err) {
        console.error('Erro ao compartilhar:', err);
      }
    } else {
      // Fallback para navegadores que não suportam a API Web Share
      navigator.clipboard.writeText(window.location.href);
      showNotification('success', 'Link copiado para a área de transferência!');
    }
  };

  useEffect(() => {
    fetchArticle();
  }, [params.slug]);

  useEffect(() => {
    if (article && isAuthenticated) {
      checkIfFavorite();
    }
  }, [article, isAuthenticated]);

  // Função para formatar a data
  const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('pt-BR', options);
  };

  if (isLoading) {
    return (
      <div className="flex flex-col justify-center items-center min-h-screen bg-white dark:bg-gray-800 rounded-lg shadow-sm p-8">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-indigo-500"></div>
        <p className="mt-4 text-gray-500 dark:text-gray-400 text-sm">Carregando artigo...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="w-full max-w-[1800px] mx-auto px-3 md:px-6 lg:px-8 py-8">
        <div className="bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-800 text-red-700 dark:text-red-300 px-4 py-5 rounded-lg shadow-sm">
          <p className="font-medium">{error}</p>
          <Link href="/artigos" className="mt-4 inline-flex items-center text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 dark:hover:text-indigo-300">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Voltar para a lista de artigos
          </Link>
        </div>
      </div>
    );
  }

  if (!article) {
    return (
      <div className="w-full max-w-[1800px] mx-auto px-3 md:px-6 lg:px-8 py-8">
        <div className="bg-yellow-100 dark:bg-yellow-900/30 border border-yellow-400 dark:border-yellow-800 text-yellow-700 dark:text-yellow-300 px-4 py-5 rounded-lg shadow-sm">
          <p className="font-medium">Artigo não encontrado.</p>
          <Link href="/artigos" className="mt-4 inline-flex items-center text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 dark:hover:text-indigo-300">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Voltar para a lista de artigos
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full max-w-[1800px] mx-auto px-3 md:px-6 lg:px-8 xl:px-10 py-8">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
        <Link href="/artigos" className="inline-flex items-center text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 dark:hover:text-indigo-300">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Voltar para a lista de artigos
        </Link>

        {isAuthenticated && user && (
          (user as any).is_staff || (user as any).is_superuser || (article.author_id && String(user.id) === String(article.author_id))
        ) && (
          <div className="flex space-x-2">
            <Link
              href={`/artigos/${article.slug}/editar`}
              className="inline-flex items-center px-3 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              <Edit className="w-4 h-4 mr-1 md:mr-2" />
              <span className="hidden md:inline">Editar</span>
              <span className="inline md:hidden">Edit</span>
            </Link>
            <DeleteArticleButton
              slug={article.slug}
              buttonText={window.innerWidth < 768 ? "Del" : "Excluir"}
              className="inline-flex items-center px-3 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            />
          </div>
        )}
      </div>

      {/* Imagem de capa do artigo (simulada ou real) */}
      <div className="mb-6 rounded-lg overflow-hidden shadow-lg">
        <img
          src={article.cover_image || article.image || `https://source.unsplash.com/random/1200x600?sig=${article.id}&${article.title}`}
          alt={article.title}
          className="w-full h-auto object-cover max-h-[400px] md:max-h-[500px]"
        />
      </div>

      <article className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 md:p-6 lg:p-8">
        <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">{article.title}</h1>

        <div className="flex flex-wrap items-center text-gray-500 dark:text-gray-400 mb-6 gap-2 text-sm md:text-base">
          <div className="flex items-center">
            <Calendar className="w-4 h-4 mr-1 flex-shrink-0" />
            <span>{formatDate(article.created_at)}</span>
          </div>

          {article.author && (
            <div className="flex items-center">
              <span className="mx-1 md:mx-2">•</span>
              <User className="w-4 h-4 mr-1 flex-shrink-0" />
              <span className="truncate">Por {article.author.first_name} {article.author.last_name}</span>
            </div>
          )}

          {article.category && (
            <div className="flex items-center">
              <span className="mx-1 md:mx-2">•</span>
              <Tag className="w-4 h-4 mr-1 flex-shrink-0" />
              <span className="text-indigo-600 dark:text-indigo-400 truncate">{article.category.name}</span>
            </div>
          )}

          <div className="flex items-center">
            <span className="mx-1 md:mx-2">•</span>
            <Eye className="w-4 h-4 mr-1 flex-shrink-0" />
            <span>{viewCount} visualizações</span>
          </div>
        </div>

        {/* Barra de ações */}
        <div className="flex flex-wrap items-center justify-end mb-6 gap-2">
          <button
            onClick={handleToggleFavorite}
            disabled={isTogglingFavorite}
            className={`flex items-center gap-1 px-3 py-1 rounded-full text-sm ${
              isFavorite
                ? 'bg-pink-100 text-pink-700 dark:bg-pink-900 dark:text-pink-300'
                : 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
            } hover:opacity-80 transition-colors`}
          >
            {isFavorite ? (
              <BookmarkCheck className="w-4 h-4" />
            ) : (
              <Bookmark className="w-4 h-4" />
            )}
            <span className="hidden sm:inline">{isFavorite ? 'Favoritado' : 'Favoritar'}</span>
          </button>

          <button
            onClick={handleShare}
            className="flex items-center gap-1 px-3 py-1 rounded-full text-sm bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300 hover:opacity-80 transition-colors"
          >
            <Share2 className="w-4 h-4" />
            <span className="hidden sm:inline">Compartilhar</span>
          </button>
        </div>

        <div
          className="prose prose-indigo dark:prose-invert max-w-none prose-img:rounded-lg prose-img:mx-auto prose-headings:text-gray-900 dark:prose-headings:text-white prose-a:text-indigo-600 dark:prose-a:text-indigo-400 prose-p:text-gray-700 dark:prose-p:text-gray-300 prose-li:text-gray-700 dark:prose-li:text-gray-300"
          dangerouslySetInnerHTML={{ __html: article.content }}
        />
      </article>

      <div className="mt-8 bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 md:p-6 lg:p-8">
        <h2 className="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white mb-4 flex items-center">
          <MessageSquare className="w-5 h-5 mr-2 text-indigo-500" />
          Deixe um comentário
        </h2>
        <div className="border border-indigo-100 dark:border-indigo-900/30 rounded-lg p-4 bg-gray-50 dark:bg-gray-800/50">
          <div className="mb-4 bg-indigo-50 dark:bg-indigo-900/20 p-3 rounded-lg text-sm text-gray-600 dark:text-gray-400">
            <p>Você pode comentar mesmo sem estar logado. Basta preencher seu nome e e-mail (opcional).</p>
          </div>
          <CommentForm
            articleId={article.id}
            articleSlug={article.slug}
            onCommentAdded={fetchArticle}
          />
        </div>
      </div>

      {article.comments && article.comments.length > 0 ? (
        <div className="mt-6 bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 md:p-6 lg:p-8">
          <CommentList
            comments={article.comments}
            articleId={article.id}
            articleSlug={article.slug}
            onCommentAdded={fetchArticle}
          />
        </div>
      ) : (
        <div className="mt-6 bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4 md:p-6 text-center">
          <p className="text-gray-500 dark:text-gray-400">Nenhum comentário ainda. Seja o primeiro a comentar!</p>
        </div>
      )}
    </div>
  );
}
