'use client';

import { useState, useEffect } from 'react';
import { BookOpen, Star, Filter } from 'lucide-react';
import Link from 'next/link';
import './styles/MangaGallery.css';

export default function MangasPage() {
  const [filter, setFilter] = useState('all');

  // Dados de mangás com cores médias para o efeito visual
  const mangasData = {
    reading: [
      {
        id: 1,
        title: 'Frieren: Beyond Journey\'s End',
        image: 'https://i.imgur.com/HWxOtcQ.jpeg',
        color: '#b0b6a9',
        status: 'Em andamento'
      },
      {
        id: 2,
        title: 'Shinozaki-kun no Mente Jijou',
        image: 'https://i.imgur.com/wRoptbT.png',
        color: '#afa294',
        status: 'Em andamento'
      },
      {
        id: 3,
        title: 'Bibliomania',
        image: 'https://i.imgur.com/MwRrRSd.jpeg',
        color: '#3c3c3d',
        status: 'Em andamento'
      },
      {
        id: 4,
        title: 'Dandadan',
        image: 'https://i.imgur.com/7FQ6L5j.jpeg',
        color: '#b47460',
        status: 'Em andamento'
      },
      {
        id: 5,
        title: 'The Summer Hikaru Died',
        image: 'https://i.imgur.com/IQSq88g.jpeg',
        color: '#60a6ce',
        status: 'Em andamento'
      },
      {
        id: 6,
        title: 'The Color of the End: Mission in the Apocalypse',
        image: 'https://i.imgur.com/QfF46xU.jpeg',
        color: '#46666f',
        status: 'Em andamento'
      },
      {
        id: 7,
        title: 'Smoking Behind the Supermarket with You',
        image: 'https://i.imgur.com/jcgbHCO.jpeg',
        color: '#8e898f',
        status: 'Em andamento'
      },
      {
        id: 8,
        title: 'Another',
        image: 'https://i.imgur.com/lIPenqN.jpeg',
        color: '#8d516e',
        status: 'Em andamento'
      }
    ],
    completed: [
      {
        id: 9,
        title: 'My Broken Mariko',
        image: 'https://i.imgur.com/OS0VRhm.png',
        color: '#6e695e',
        status: 'Completo'
      },
      {
        id: 10,
        title: 'Adabana',
        image: 'https://i.imgur.com/uqktm8j.jpeg',
        color: '#b16e79',
        status: 'Completo'
      },
      {
        id: 11,
        title: 'Yiska',
        image: 'https://i.imgur.com/QKXIJlH.jpeg',
        color: '#bdbdbd',
        status: 'Completo'
      }
    ],
    planning: [
      {
        id: 12,
        title: 'BLAME!',
        image: 'https://i.imgur.com/yCBmW1b.png',
        color: '#7b4d35',
        status: 'Planejado'
      },
      {
        id: 13,
        title: 'I Have a Crush at Work',
        image: 'https://i.imgur.com/ZGvNhE7.jpeg',
        color: '#ceb5a8',
        status: 'Planejado'
      },
      {
        id: 14,
        title: 'Carnelian: the Sille Dragon Odyssey',
        image: 'https://i.imgur.com/kTmZvmd.jpeg',
        color: '#6d413f',
        status: 'Planejado'
      },
      {
        id: 15,
        title: 'Ougon no Keikenchi',
        image: 'https://i.imgur.com/jXc2WJf.jpeg',
        color: '#666060',
        status: 'Planejado'
      },
      {
        id: 16,
        title: 'Cigarette & Cherry',
        image: 'https://i.imgur.com/fHFUOYg.jpeg',
        color: '#827d88',
        status: 'Planejado'
      }
    ]
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
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Mangás</h1>
        <div className="flex items-center gap-2">
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

      <div className="manga-gallery">
        <main className="manga-gallery-container">
          {filteredMangas.reading.length > 0 && (
            <section className="manga-section">
              <header>
                <h1>Em Leitura</h1>
              </header>
              {filteredMangas.reading.map(manga => (
                <Link href={`/mangas/${manga.id}`} key={manga.id}>
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
                <Link href={`/mangas/${manga.id}`} key={manga.id}>
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
                <Link href={`/mangas/${manga.id}`} key={manga.id}>
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
        </main>
      </div>
    </div>
  );
}
