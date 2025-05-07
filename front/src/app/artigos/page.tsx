'use client';

import { useEffect, useState } from 'react';
import { FileText, Filter, Clock, Tag, Plus } from 'lucide-react';
import Link from 'next/link';
import Header from './components/Header';
import Hero from './components/Hero';
import FeaturedArticles from './components/FeaturedArticles';
import { Article, PaginatedResponse } from '../core/types/models';
import { articlesService } from '../core/services/api';
import ArticleCard from '../core/components/articles/ArticleCard';
import { useAuth } from '../core/contexts/AuthContext';
import Pagination from '../core/components/ui/Pagination';
import { useNotification } from '../core/contexts/NotificationContext';

export default function ArtigosPage() {
  const { isAuthenticated } = useAuth();
  const { showNotification } = useNotification();
  const [articles, setArticles] = useState<Article[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalArticles, setTotalArticles] = useState(0);

  // Buscar artigos da API
  useEffect(() => {
    const fetchArticles = async () => {
      try {
        setIsLoading(true);
        const paginatedData = await articlesService.getPaginatedArticles(currentPage);

        setArticles(paginatedData.results);
        setTotalArticles(paginatedData.count);

        // Calcular o número total de páginas
        const pages = Math.ceil(paginatedData.count / 10); // Assumindo 10 itens por página
        setTotalPages(pages > 0 ? pages : 1);

        setError(null);

        console.log('Artigos carregados:', paginatedData.results);
        console.log('Total de artigos:', paginatedData.count);
        console.log('Total de páginas:', pages);
      } catch (err: any) {
        console.error('Erro ao buscar artigos:', err);
        const errorMessage = 'Não foi possível carregar os artigos. Por favor, tente novamente mais tarde.';
        setError(errorMessage);
        showNotification('error', errorMessage);

        // Dados de exemplo para desenvolvimento
        setArticles([
          {
            id: 1,
            title: 'Como Criar um Blog com Next.js',
            slug: 'como-criar-um-blog-com-nextjs',
            content: 'Um guia completo para criar um blog moderno usando Next.js, Tailwind CSS e TypeScript.',
            created_at: '2023-08-15',
            comments: [],
            comments_count: 0
          },
          {
            id: 2,
            title: 'Introdução ao TypeScript',
            slug: 'introducao-ao-typescript',
            content: 'Aprenda os conceitos básicos do TypeScript e como ele pode melhorar seu desenvolvimento.',
            created_at: '2023-07-22',
            comments: [],
            comments_count: 0
          },
          {
            id: 3,
            title: 'Tailwind CSS: Guia Definitivo',
            slug: 'tailwind-css-guia-definitivo',
            content: 'Domine o Tailwind CSS e crie interfaces modernas com facilidade.',
            created_at: '2023-06-10',
            comments: [],
            comments_count: 0
          }
        ]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchArticles();
  }, [currentPage, showNotification]);

  // Função para mudar de página
  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Verificar se articles é um array válido
  const articlesArray = Array.isArray(articles) ? articles : [];

  // Filtrar artigos
  const filteredArticles = articlesArray.filter(article => {
    // Se não houver filtro, mostrar todos
    if (filter === 'all') return true;

    // Implementar lógica de filtro específica para sua aplicação
    // Por exemplo, filtrar por categoria
    return article.title.toLowerCase().includes(filter.toLowerCase());
  });

  // Buscar artigos
  const searchedArticles = filteredArticles.filter(article => {
    if (!searchQuery) return true;

    return (
      article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.content.toLowerCase().includes(searchQuery.toLowerCase())
    );
  });

  // Enquanto os artigos estão sendo carregados
  if (isLoading) {
    return (
      <>
        <Header />
        <Hero />
        <div className="container mx-auto px-4 py-8 space-y-8">
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Header />
      <Hero />
      <div className="container mx-auto px-4 py-8 space-y-8">
        <FeaturedArticles />

        <div className="space-y-8">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Todos os Artigos</h1>
            <div className="flex items-center gap-2">
              {isAuthenticated && (
                <Link
                  href="/artigos/novo"
                  className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Novo Artigo
                </Link>
              )}
              <div className="relative">
                <input
                  type="text"
                  placeholder="Buscar artigos..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="px-4 py-2 pr-10 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                />
                <FileText className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              </div>
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-2 flex items-center gap-2">
                <Filter className="w-5 h-5 text-gray-500 dark:text-gray-400" />
                <select
                  value={filter}
                  onChange={(e) => setFilter(e.target.value)}
                  className="bg-transparent border-none text-gray-700 dark:text-gray-300 focus:ring-0"
                >
                  <option value="all">Todos</option>
                  <option value="tecnologia">Tecnologia</option>
                  <option value="programação">Programação</option>
                  <option value="design">Design</option>
                  <option value="mangá">Mangá</option>
                  <option value="cultura">Cultura</option>
                </select>
              </div>
            </div>
          </div>

          {searchedArticles.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500 dark:text-gray-400">Nenhum artigo encontrado.</p>
            </div>
          ) : (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {searchedArticles.map(article => (
                  <ArticleCard key={article.id} article={article} />
                ))}
              </div>

              {/* Paginação */}
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={handlePageChange}
              />

              {/* Informação sobre total de artigos */}
              <div className="text-center mt-4 text-sm text-gray-500 dark:text-gray-400">
                Mostrando {articles.length} de {totalArticles} artigos
              </div>
            </>
          )}
        </div>
      </div>
    </>
  );
}
