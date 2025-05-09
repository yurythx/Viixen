'use client';

import { useEffect, useState } from 'react';
import { FileText, Filter, Clock, Tag, Plus, Edit, Trash2, MessageSquare } from 'lucide-react';
import Link from 'next/link';
import { Article } from '../../types/models';
import { articlesService } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';
import Pagination from '../../components/ui/Pagination';
import { useNotification } from '../../contexts/NotificationContext';
import DeleteArticleButton from '../../components/articles/DeleteArticleButton';
import './styles/ArticleGallery.css';

export default function ArtigosPage() {
  const { isAuthenticated, user } = useAuth();
  const { showNotification } = useNotification();
  const [articles, setArticles] = useState<Article[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalArticles, setTotalArticles] = useState(0);

  // Estado para armazenar os artigos categorizados
  const [articlesData, setArticlesData] = useState<{
    recentes: Article[];
    populares: Article[];
    destaques: Article[];
  }>({
    recentes: [],
    populares: [],
    destaques: []
  });

  // Buscar artigos da API
  useEffect(() => {
    const fetchArticles = async () => {
      try {
        setIsLoading(true);
        const paginatedData = await articlesService.getPaginatedArticles(currentPage);

        const articlesResult = paginatedData.results;
        setArticles(articlesResult);
        setTotalArticles(paginatedData.count);

        // Calcular o número total de páginas
        const pages = Math.ceil(paginatedData.count / 10); // Assumindo 10 itens por página
        setTotalPages(pages > 0 ? pages : 1);

        // Categorizar os artigos
        const recentes: Article[] = [];
        const populares: Article[] = [];
        const destaques: Article[] = [];

        articlesResult.forEach(article => {
          // Gerar uma cor aleatória para cada artigo
          const color = `#${Math.floor(Math.random()*16777215).toString(16)}`;
          article.color = color;

          // Categorização baseada em critérios
          // Artigos recentes: criados nos últimos 30 dias
          const thirtyDaysAgo = new Date();
          thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
          const articleDate = new Date(article.created_at);

          if (articleDate > thirtyDaysAgo) {
            recentes.push(article);
          }

          // Artigos populares: com mais visualizações ou comentários
          if (article.comments_count && article.comments_count > 0) {
            populares.push(article);
          }

          // Artigos em destaque: marcados como destaque ou aleatórios
          if (article.featured) {
            destaques.push(article);
          }
        });

        // Garantir que cada categoria tenha pelo menos alguns artigos
        // Se não houver artigos suficientes, adicionar alguns aleatórios
        if (recentes.length === 0) {
          recentes.push(...articlesResult.slice(0, 3));
        }

        if (populares.length === 0) {
          populares.push(...articlesResult.slice(0, 3));
        }

        if (destaques.length === 0) {
          destaques.push(...articlesResult.slice(0, 3));
        }

        setArticlesData({
          recentes,
          populares,
          destaques
        });

        setError(null);
      } catch (err: any) {
        console.error('Erro ao buscar artigos:', err);
        const errorMessage = 'Não foi possível carregar os artigos. Por favor, tente novamente mais tarde.';
        setError(errorMessage);
        showNotification('error', errorMessage);

        // Dados de exemplo para desenvolvimento
        const mockArticles = [
          {
            id: 1,
            title: 'Como Criar um Blog com Next.js',
            slug: 'como-criar-um-blog-com-nextjs',
            content: 'Um guia completo para criar um blog moderno usando Next.js, Tailwind CSS e TypeScript.',
            created_at: '2023-08-15',
            comments: [],
            comments_count: 0,
            color: '#6366f1'
          },
          {
            id: 2,
            title: 'Introdução ao TypeScript',
            slug: 'introducao-ao-typescript',
            content: 'Aprenda os conceitos básicos do TypeScript e como ele pode melhorar seu desenvolvimento.',
            created_at: '2023-07-22',
            comments: [],
            comments_count: 0,
            color: '#8b5cf6'
          },
          {
            id: 3,
            title: 'Tailwind CSS: Guia Definitivo',
            slug: 'tailwind-css-guia-definitivo',
            content: 'Domine o Tailwind CSS e crie interfaces modernas com facilidade.',
            created_at: '2023-06-10',
            comments: [],
            comments_count: 0,
            color: '#ec4899'
          },
          {
            id: 4,
            title: 'React Hooks: Guia Completo',
            slug: 'react-hooks-guia-completo',
            content: 'Aprenda a usar todos os hooks do React para criar componentes funcionais poderosos.',
            created_at: '2023-05-15',
            comments: [],
            comments_count: 2,
            color: '#f59e0b'
          },
          {
            id: 5,
            title: 'Desenvolvimento Full Stack com Next.js',
            slug: 'desenvolvimento-full-stack-nextjs',
            content: 'Como criar aplicações completas usando Next.js para front-end e back-end.',
            created_at: '2023-04-20',
            comments: [],
            comments_count: 5,
            featured: true,
            color: '#10b981'
          }
        ];

        setArticles(mockArticles);

        // Categorizar os artigos de exemplo
        setArticlesData({
          recentes: mockArticles.slice(0, 3),
          populares: [mockArticles[3], mockArticles[4], mockArticles[0]],
          destaques: [mockArticles[4], mockArticles[2], mockArticles[1]]
        });
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

  // Função para lidar com a exclusão de um artigo
  const handleArticleDeleted = () => {
    // Recarregar os artigos
    const fetchArticles = async () => {
      try {
        setIsLoading(true);
        const paginatedData = await articlesService.getPaginatedArticles(currentPage);
        setArticles(paginatedData.results);
        setTotalArticles(paginatedData.count);

        // Recategorizar os artigos
        // (código similar ao do useEffect)
        // ...

        showNotification('success', 'Artigo excluído com sucesso!');
      } catch (err) {
        console.error('Erro ao recarregar artigos:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchArticles();
  };

  // Verificar se articles é um array válido
  const articlesArray = Array.isArray(articles) ? articles : [];

  // Função auxiliar para filtrar artigos por categoria
  const filterArticleByCategory = (article: any) => {
    if (filter === 'all') return true;

    // Verificar se o artigo tem categoria
    if (article.category) {
      // Verificar pelo slug da categoria
      if (article.category.slug && article.category.slug.toLowerCase() === filter.toLowerCase()) {
        return true;
      }

      // Verificar pelo nome da categoria
      if (article.category.name && article.category.name.toLowerCase() === filter.toLowerCase()) {
        return true;
      }
    }

    // Verificar se o título ou conteúdo contém a palavra-chave do filtro
    if (article.title && article.title.toLowerCase().includes(filter.toLowerCase())) {
      return true;
    }

    if (article.content && article.content.toLowerCase().includes(filter.toLowerCase())) {
      return true;
    }

    return false;
  };

  // Aplicar filtro às categorias
  const filteredArticlesData = {
    recentes: articlesData.recentes.filter(filterArticleByCategory),
    populares: articlesData.populares.filter(filterArticleByCategory),
    destaques: articlesData.destaques.filter(filterArticleByCategory)
  };

  // Função auxiliar para buscar artigos
  const searchArticle = (article: any) => {
    if (!searchQuery) return true;

    const query = searchQuery.toLowerCase();

    // Buscar no título
    if (article.title && article.title.toLowerCase().includes(query)) {
      return true;
    }

    // Buscar no conteúdo
    if (article.content && article.content.toLowerCase().includes(query)) {
      return true;
    }

    // Buscar na categoria
    if (article.category) {
      if (article.category.name && article.category.name.toLowerCase().includes(query)) {
        return true;
      }

      if (article.category.slug && article.category.slug.toLowerCase().includes(query)) {
        return true;
      }
    }

    // Buscar no autor
    if (article.author) {
      if ((article.author as any).username && (article.author as any).username.toLowerCase().includes(query)) {
        return true;
      }

      if ((article.author as any).name && (article.author as any).name.toLowerCase().includes(query)) {
        return true;
      }
    }

    return false;
  };

  // Aplicar busca às categorias filtradas
  const searchedArticlesData = {
    recentes: filteredArticlesData.recentes.filter(searchArticle),
    populares: filteredArticlesData.populares.filter(searchArticle),
    destaques: filteredArticlesData.destaques.filter(searchArticle)
  };

  // Para compatibilidade com o código existente
  const filteredArticles = articlesArray.filter(filterArticleByCategory);

  // Usamos o resultado para exibir a contagem total de artigos filtrados
  const totalFilteredArticles = filteredArticles.length;

  // Enquanto os artigos estão sendo carregados
  if (isLoading) {
    return (
      <>
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
      <div className="container-fluid w-full max-w-[1800px] mx-auto px-3 md:px-6 lg:px-8 xl:px-10 py-8 space-y-8 dark:bg-gray-900">

        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
          <h1 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">Biblioteca de Artigos</h1>
          <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
            {isAuthenticated && (
              <Link
                href="/artigos/novo"
                className="inline-flex items-center px-3 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                <Plus className="w-4 h-4 mr-1" />
                Novo
              </Link>
            )}
            <div className="relative flex-1 md:flex-none">
              <input
                type="text"
                placeholder="Buscar artigos..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full px-3 py-2 pr-8 text-sm rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
              <FileText className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-2 flex items-center gap-1 text-sm">
              <Filter className="w-4 h-4 text-gray-500 dark:text-gray-400" />
              <select
                value={filter}
                onChange={(e) => {
                  setFilter(e.target.value);
                  // Resetar a busca quando mudar o filtro
                  if (searchQuery) {
                    setSearchQuery('');
                  }
                }}
                className="bg-transparent border-none text-gray-700 dark:text-gray-300 focus:ring-0 text-sm"
              >
                <option value="all">Todos</option>
                <option value="tecnologia">Tecnologia</option>
                <option value="programação">Programação</option>
                <option value="design">Design</option>
                <option value="mangá">Mangá</option>
                <option value="cultura">Cultura</option>
                <option value="anime">Anime</option>
                <option value="games">Games</option>
              </select>
            </div>
          </div>
        </div>

        {error && (
          <div className="bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-800 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg shadow-sm" role="alert">
            <span className="block sm:inline font-medium">{error}</span>
          </div>
        )}

        {isLoading ? (
          <div className="flex flex-col justify-center items-center h-64 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
            <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-indigo-500"></div>
            <p className="mt-4 text-gray-500 dark:text-gray-400 text-sm">Carregando artigos...</p>
          </div>
        ) : (
          <>
            <div className="article-gallery">
              <main className="article-gallery-container">
                {searchedArticlesData.recentes.length > 0 && (
                  <section className="article-section">
                    <header>
                      <h1>Artigos Recentes</h1>
                    </header>
                    {searchedArticlesData.recentes.map(article => (
                      <div key={article.id} className="article-card-wrapper">
                        <Link href={`/artigos/${article.slug}`}>
                          <article className="article-card" style={{"--avarage-color": article.color} as React.CSSProperties}>
                            <figure className="article-figure">
                              <img
                                src={article.cover_image || article.image || `https://source.unsplash.com/random/300x200?sig=${article.id}&${article.title}`}
                                alt={article.title}
                              />
                              <div className="article-info">
                                {article.category && (
                                  <span className="article-category">
                                    <Tag className="w-3 h-3" /> {article.category.name}
                                  </span>
                                )}

                                <div>
                                  <h2 className="article-title">{article.title}</h2>
                                  <p className="article-excerpt">{article.content ? article.content.replace(/<[^>]*>/g, '').substring(0, 150) + '...' : 'Sem conteúdo disponível'}</p>
                                </div>

                                {article.author && (
                                  <div className="article-author">
                                    <div className="article-author-avatar-placeholder">A</div>
                                    <span>{(article.author as any).username || 'Autor'}</span>
                                  </div>
                                )}

                                <div className="article-meta">
                                  <span className="article-meta-item">
                                    <Clock className="w-4 h-4" /> {new Date(article.created_at).toLocaleDateString('pt-BR')}
                                  </span>
                                  <span className="article-meta-item">
                                    <MessageSquare className="w-4 h-4" /> {article.comments_count && article.comments_count > 0 ?
                                      `${article.comments_count} comentário${article.comments_count > 1 ? 's' : ''}` :
                                      'Sem comentários'}
                                  </span>
                                  {(article as any).views && (
                                    <span className="article-meta-item">
                                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4">
                                        <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" />
                                        <circle cx="12" cy="12" r="3" />
                                      </svg> {(article as any).views} visualizaç{(article as any).views > 1 ? 'ões' : 'ão'}
                                    </span>
                                  )}
                                </div>
                              </div>
                            </figure>
                          </article>
                        </Link>
                        {isAuthenticated && user && (
                          (user as any).is_staff || (user as any).is_superuser || (article.author_id && String(user.id) === String(article.author_id))
                        ) && (
                          <div className="article-actions">
                            <Link href={`/artigos/${article.slug}/editar`} className="edit-button">
                              <Edit className="w-4 h-4" />
                            </Link>
                            <DeleteArticleButton
                              slug={article.slug}
                              className="delete-button"
                              showIcon={true}
                              buttonText=""
                              onDelete={handleArticleDeleted}
                            />
                          </div>
                        )}
                      </div>
                    ))}
                  </section>
                )}

                {searchedArticlesData.populares.length > 0 && (
                  <section className="article-section">
                    <header>
                      <h1>Artigos Populares</h1>
                    </header>
                    {searchedArticlesData.populares.map(article => (
                      <div key={article.id} className="article-card-wrapper">
                        <Link href={`/artigos/${article.slug}`}>
                          <article className="article-card" style={{"--avarage-color": article.color} as React.CSSProperties}>
                            <figure className="article-figure">
                              <img
                                src={article.cover_image || article.image || `https://source.unsplash.com/random/300x200?sig=${article.id}&${article.title}`}
                                alt={article.title}
                              />
                              <div className="article-info">
                                {article.category && (
                                  <span className="article-category">
                                    <Tag className="w-3 h-3" /> {article.category.name}
                                  </span>
                                )}

                                <div>
                                  <h2 className="article-title">{article.title}</h2>
                                  <p className="article-excerpt">{article.content ? article.content.replace(/<[^>]*>/g, '').substring(0, 150) + '...' : 'Sem conteúdo disponível'}</p>
                                </div>

                                {article.author && (
                                  <div className="article-author">
                                    <div className="article-author-avatar-placeholder">A</div>
                                    <span>{(article.author as any).username || 'Autor'}</span>
                                  </div>
                                )}

                                <div className="article-meta">
                                  <span className="article-meta-item">
                                    <Clock className="w-4 h-4" /> {new Date(article.created_at).toLocaleDateString('pt-BR')}
                                  </span>
                                  <span className="article-meta-item">
                                    <MessageSquare className="w-4 h-4" /> {article.comments_count && article.comments_count > 0 ?
                                      `${article.comments_count} comentário${article.comments_count > 1 ? 's' : ''}` :
                                      'Sem comentários'}
                                  </span>
                                  {(article as any).views && (
                                    <span className="article-meta-item">
                                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4">
                                        <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" />
                                        <circle cx="12" cy="12" r="3" />
                                      </svg> {(article as any).views} visualizaç{(article as any).views > 1 ? 'ões' : 'ão'}
                                    </span>
                                  )}
                                </div>
                              </div>
                            </figure>
                          </article>
                        </Link>
                        {isAuthenticated && user && (
                          (user as any).is_staff || (user as any).is_superuser || (article.author_id && String(user.id) === String(article.author_id))
                        ) && (
                          <div className="article-actions">
                            <Link href={`/artigos/${article.slug}/editar`} className="edit-button">
                              <Edit className="w-4 h-4" />
                            </Link>
                            <DeleteArticleButton
                              slug={article.slug}
                              className="delete-button"
                              showIcon={true}
                              buttonText=""
                              onDelete={handleArticleDeleted}
                            />
                          </div>
                        )}
                      </div>
                    ))}
                  </section>
                )}

                {searchedArticlesData.destaques.length > 0 && (
                  <section className="article-section">
                    <header>
                      <h1>Artigos em Destaque</h1>
                    </header>
                    {searchedArticlesData.destaques.map(article => (
                      <div key={article.id} className="article-card-wrapper">
                        <Link href={`/artigos/${article.slug}`}>
                          <article className="article-card" style={{"--avarage-color": article.color} as React.CSSProperties}>
                            <figure className="article-figure">
                              <img
                                src={article.cover_image || article.image || `https://source.unsplash.com/random/300x200?sig=${article.id}&${article.title}`}
                                alt={article.title}
                              />
                              <div className="article-info">
                                {article.category && (
                                  <span className="article-category">
                                    <Tag className="w-3 h-3" /> {article.category.name}
                                  </span>
                                )}

                                <div>
                                  <h2 className="article-title">{article.title}</h2>
                                  <p className="article-excerpt">{article.content ? article.content.replace(/<[^>]*>/g, '').substring(0, 150) + '...' : 'Sem conteúdo disponível'}</p>
                                </div>

                                {article.author && (
                                  <div className="article-author">
                                    <div className="article-author-avatar-placeholder">A</div>
                                    <span>{(article.author as any).username || 'Autor'}</span>
                                  </div>
                                )}

                                <div className="article-meta">
                                  <span className="article-meta-item">
                                    <Clock className="w-4 h-4" /> {new Date(article.created_at).toLocaleDateString('pt-BR')}
                                  </span>
                                  <span className="article-meta-item">
                                    <MessageSquare className="w-4 h-4" /> {article.comments_count && article.comments_count > 0 ?
                                      `${article.comments_count} comentário${article.comments_count > 1 ? 's' : ''}` :
                                      'Sem comentários'}
                                  </span>
                                  {(article as any).views && (
                                    <span className="article-meta-item">
                                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4">
                                        <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" />
                                        <circle cx="12" cy="12" r="3" />
                                      </svg> {(article as any).views} visualizaç{(article as any).views > 1 ? 'ões' : 'ão'}
                                    </span>
                                  )}
                                </div>
                              </div>
                            </figure>
                          </article>
                        </Link>
                        {isAuthenticated && user && (
                          (user as any).is_staff || (user as any).is_superuser || (article.author_id && String(user.id) === String(article.author_id))
                        ) && (
                          <div className="article-actions">
                            <Link href={`/artigos/${article.slug}/editar`} className="edit-button">
                              <Edit className="w-4 h-4" />
                            </Link>
                            <DeleteArticleButton
                              slug={article.slug}
                              className="delete-button"
                              showIcon={true}
                              buttonText=""
                              onDelete={handleArticleDeleted}
                            />
                          </div>
                        )}
                      </div>
                    ))}
                  </section>
                )}

                {/* Se não houver artigos em nenhuma categoria após a filtragem */}
                {searchedArticlesData.recentes.length === 0 &&
                 searchedArticlesData.populares.length === 0 &&
                 searchedArticlesData.destaques.length === 0 && (
                  <div className="text-center py-12 bg-gray-50 dark:bg-gray-800 rounded-lg shadow-sm">
                    <p className="text-gray-500 dark:text-gray-400 font-medium">Nenhum artigo encontrado.</p>
                    <p className="text-gray-400 dark:text-gray-500 text-sm mt-2">Tente ajustar os filtros ou a busca.</p>
                  </div>
                )}
              </main>
            </div>

            {/* Informação sobre total de artigos */}
            <div className="text-center mb-4 text-sm text-gray-500 dark:text-gray-400">
              {filter !== 'all' || searchQuery ? (
                <span>
                  Mostrando {filteredArticles.length} artigos filtrados de {totalArticles} no total
                </span>
              ) : (
                <span>
                  Mostrando {articles.length} de {totalArticles} artigos
                </span>
              )}
            </div>

            {/* Paginação */}
            <div className="overflow-x-auto py-2">
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={handlePageChange}
              />
            </div>
          </>
        )}
      </div>
    </>
  );
}
