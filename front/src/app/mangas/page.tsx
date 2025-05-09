'use client';

import { useState, useEffect } from 'react';
import { BookOpen, Star, Filter, Plus } from 'lucide-react';
import Link from 'next/link';
import './styles/MangaGallery.css';
import mangasService, { Manga } from '../core/services/api/mangas.service';
import { useAuth } from '../core/contexts/AuthContext';
import { useNotification } from '../core/contexts/NotificationContext';

// Interface para os mangás com informações de exibição
interface DisplayManga {
  id: number;
  title: string;
  image: string;
  color: string;
  status: string;
  slug: string;
}

export default function MangasPage() {
  const [filter, setFilter] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated } = useAuth();
  const { showNotification } = useNotification();
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalMangas, setTotalMangas] = useState(0);

  // Estado para armazenar os mangás
  const [mangasData, setMangasData] = useState<{
    reading: DisplayManga[];
    completed: DisplayManga[];
    planning: DisplayManga[];
  }>({
    reading: [],
    completed: [],
    planning: []
  });

  // Buscar mangás da API
  useEffect(() => {
    const fetchMangas = async () => {
      try {
        setIsLoading(true);

        // Buscar mangás com paginação e pesquisa
        const paginatedData = await mangasService.getPaginatedMangas(currentPage, searchTerm);

        // Atualizar informações de paginação
        setTotalMangas(paginatedData.count);
        const pages = Math.ceil(paginatedData.count / 10); // Assumindo 10 itens por página
        setTotalPages(pages > 0 ? pages : 1);

        // Converter os mangás da API para o formato de exibição
        const reading: DisplayManga[] = [];
        const completed: DisplayManga[] = [];
        const planning: DisplayManga[] = [];

        paginatedData.results.forEach(manga => {
          // Gerar uma cor aleatória para cada mangá
          const color = `#${Math.floor(Math.random()*16777215).toString(16)}`;

          const displayManga: DisplayManga = {
            id: manga.id,
            title: manga.title,
            image: manga.cover || 'https://placehold.co/300x450?text=Sem+Capa',
            color: color,
            status: 'Em andamento', // Você pode adicionar um campo status ao modelo Manga
            slug: manga.slug
          };

          // Categorização baseada nos capítulos
          if (manga.chapters && manga.chapters.length > 0) {
            // Se tiver mais de 80% dos capítulos, consideramos completo
            // Esta é uma lógica de exemplo, você pode ajustar conforme necessário
            const totalChapters = manga.chapters.length;
            const lastChapterNumber = Math.max(...manga.chapters.map(c => c.number));

            if (lastChapterNumber > 0 && totalChapters / lastChapterNumber > 0.8) {
              completed.push(displayManga);
            } else {
              reading.push(displayManga);
            }
          } else {
            planning.push(displayManga);
          }
        });

        setMangasData({
          reading,
          completed,
          planning
        });

        setError(null);
      } catch (error) {
        console.error('Erro ao buscar mangás:', error);
        setError('Não foi possível carregar os mangás. Tente novamente mais tarde.');

        // Usar dados de fallback em caso de erro
        setMangasData({
          reading: [
            {
              id: 1,
              title: 'Frieren: Beyond Journey\'s End',
              image: 'https://i.imgur.com/HWxOtcQ.jpeg',
              color: '#b0b6a9',
              status: 'Em andamento',
              slug: 'frieren'
            },
            {
              id: 2,
              title: 'Dandadan',
              image: 'https://i.imgur.com/7FQ6L5j.jpeg',
              color: '#b47460',
              status: 'Em andamento',
              slug: 'dandadan'
            }
          ],
          completed: [
            {
              id: 9,
              title: 'My Broken Mariko',
              image: 'https://i.imgur.com/OS0VRhm.png',
              color: '#6e695e',
              status: 'Completo',
              slug: 'my-broken-mariko'
            }
          ],
          planning: [
            {
              id: 12,
              title: 'BLAME!',
              image: 'https://i.imgur.com/yCBmW1b.png',
              color: '#7b4d35',
              status: 'Planejado',
              slug: 'blame'
            }
          ]
        });

        setTotalPages(1);
        setTotalMangas(0);
      } finally {
        setIsLoading(false);
      }
    };

    fetchMangas();
  }, [currentPage, searchTerm]);

  // Função para lidar com a pesquisa
  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setCurrentPage(1); // Resetar para a primeira página ao pesquisar
  };

  // Função para limpar a pesquisa
  const clearSearch = () => {
    setSearchTerm('');
    setCurrentPage(1);
  };

  // Filtrar mangás com base na seleção
  const getFilteredMangas = () => {
    if (filter === 'all') {
      return {
        reading: mangasData.reading,
        completed: mangasData.completed,
        planning: mangasData.planning
      };
    } else if (filter === 'ongoing') {
      return {
        reading: mangasData.reading,
        completed: [],
        planning: []
      };
    } else if (filter === 'completed') {
      return {
        reading: [],
        completed: mangasData.completed,
        planning: []
      };
    } else if (filter === 'planning') {
      return {
        reading: [],
        completed: [],
        planning: mangasData.planning
      };
    }
    return mangasData;
  };

  const filteredMangas = getFilteredMangas();

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Mangás</h1>
        <div className="flex flex-col sm:flex-row items-center gap-4 w-full md:w-auto">
          {/* Barra de pesquisa */}
          <form onSubmit={handleSearch} className="relative w-full sm:w-64 md:w-72">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Pesquisar mangás..."
              className="w-full px-4 py-2 pr-10 border rounded-lg focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            />
            {searchTerm && (
              <button
                type="button"
                onClick={clearSearch}
                className="absolute right-10 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
              >
                ×
              </button>
            )}
            <button
              type="submit"
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
            >
              🔍
            </button>
          </form>

          <div className="flex items-center gap-2">
            {isAuthenticated && (
              <Link
                href="/mangas/novo"
                className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors whitespace-nowrap"
              >
                <Plus className="w-5 h-5" />
                Novo Mangá
              </Link>
            )}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-2 flex items-center gap-2">
              <Filter className="w-5 h-5 text-gray-500 dark:text-gray-400" />
              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="bg-transparent border-none text-gray-700 dark:text-gray-300 focus:ring-0"
              >
                <option value="all">Todos</option>
                <option value="ongoing">Em leitura</option>
                <option value="completed">Completos</option>
                <option value="planning">Planejados</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      )}

      {searchTerm && (
        <div className="bg-indigo-50 dark:bg-indigo-900/20 p-4 rounded-lg">
          <p className="text-indigo-700 dark:text-indigo-300">
            Resultados da pesquisa para: <strong>"{searchTerm}"</strong>
            <button
              onClick={clearSearch}
              className="ml-2 text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 dark:hover:text-indigo-300"
            >
              Limpar pesquisa
            </button>
          </p>
        </div>
      )}

      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
      ) : (
        <>
          <div className="manga-gallery">
            <main className="manga-gallery-container">
              {filteredMangas.reading.length > 0 && (
                <section className="manga-section">
                  <header>
                    <h1>Em Leitura</h1>
                  </header>
                  {filteredMangas.reading.map(manga => (
                    <Link href={`/mangas/${manga.slug}`} key={manga.id}>
                      <article className="manga-card" style={{"--avarage-color": manga.color} as React.CSSProperties}>
                        <figure className="manga-figure">
                          <img src={manga.image} alt={manga.title} />
                          <figcaption>{manga.title}</figcaption>
                        </figure>
                      </article>
                    </Link>
                  ))}
                </section>
              )}

              {filteredMangas.completed.length > 0 && (
                <section className="manga-section">
                  <header>
                    <h1>Completos</h1>
                  </header>
                  {filteredMangas.completed.map(manga => (
                    <Link href={`/mangas/${manga.slug}`} key={manga.id}>
                      <article className="manga-card" style={{"--avarage-color": manga.color} as React.CSSProperties}>
                        <figure className="manga-figure">
                          <img src={manga.image} alt={manga.title} />
                          <figcaption>{manga.title}</figcaption>
                        </figure>
                      </article>
                    </Link>
                  ))}
                </section>
              )}

              {filteredMangas.planning.length > 0 && (
                <section className="manga-section">
                  <header>
                    <h1>Planejados</h1>
                  </header>
                  {filteredMangas.planning.map(manga => (
                    <Link href={`/mangas/${manga.slug}`} key={manga.id}>
                      <article className="manga-card" style={{"--avarage-color": manga.color} as React.CSSProperties}>
                        <figure className="manga-figure">
                          <img src={manga.image} alt={manga.title} />
                          <figcaption>{manga.title}</figcaption>
                        </figure>
                      </article>
                    </Link>
                  ))}
                </section>
              )}

              {filteredMangas.reading.length === 0 &&
               filteredMangas.completed.length === 0 &&
               filteredMangas.planning.length === 0 && (
                <div className="text-center py-12">
                  <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Nenhum mangá encontrado</h2>
                  <p className="text-gray-600 dark:text-gray-300 mb-6">
                    {searchTerm
                      ? `Não encontramos nenhum mangá correspondente a "${searchTerm}".`
                      : 'Não há mangás disponíveis no momento.'}
                  </p>
                  {searchTerm && (
                    <button
                      onClick={clearSearch}
                      className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors"
                    >
                      Limpar pesquisa
                    </button>
                  )}
                </div>
              )}
            </main>
          </div>

          {/* Paginação */}
          {totalPages > 1 && (
            <div className="flex justify-center mt-8">
              <nav className="flex items-center gap-1">
                <button
                  onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                  disabled={currentPage === 1}
                  className={`px-3 py-1 rounded-md ${
                    currentPage === 1
                      ? 'text-gray-400 cursor-not-allowed'
                      : 'text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
                  }`}
                >
                  Anterior
                </button>

                {Array.from({ length: totalPages }, (_, i) => i + 1).map(page => (
                  <button
                    key={page}
                    onClick={() => setCurrentPage(page)}
                    className={`px-3 py-1 rounded-md ${
                      currentPage === page
                        ? 'bg-indigo-600 text-white'
                        : 'text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
                    }`}
                  >
                    {page}
                  </button>
                ))}

                <button
                  onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                  disabled={currentPage === totalPages}
                  className={`px-3 py-1 rounded-md ${
                    currentPage === totalPages
                      ? 'text-gray-400 cursor-not-allowed'
                      : 'text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
                  }`}
                >
                  Próxima
                </button>
              </nav>
            </div>
          )}

          {/* Informações de paginação */}
          {totalMangas > 0 && (
            <div className="text-center text-sm text-gray-500 dark:text-gray-400 mt-2">
              Mostrando página {currentPage} de {totalPages} ({totalMangas} mangás no total)
            </div>
          )}
        </>
      )}
    </div>
  );
}
