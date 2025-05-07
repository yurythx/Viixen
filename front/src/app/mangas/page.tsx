'use client';

import { useState } from 'react';
import { BookOpen, Star, Filter } from 'lucide-react';
import Link from 'next/link';

export default function MangasPage() {
  const [filter, setFilter] = useState('all');

  const mangas = [
    {
      id: 1,
      title: 'One Piece',
      cover: '/images/mangas/one-piece.jpg',
      author: 'Eiichiro Oda',
      genres: ['Ação', 'Aventura', 'Fantasia'],
      status: 'Em andamento',
      rating: 4.8,
      chapters: 1089,
      description: 'A história segue Monkey D. Luffy, um jovem cujo corpo ganhou as propriedades de borracha após ter comido uma fruta do diabo acidentalmente.'
    },
    {
      id: 2,
      title: 'Naruto',
      cover: '/images/mangas/naruto.jpg',
      author: 'Masashi Kishimoto',
      genres: ['Ação', 'Aventura', 'Fantasia'],
      status: 'Completo',
      rating: 4.7,
      chapters: 700,
      description: 'Naruto Uzumaki é um jovem ninja que constantemente procura por reconhecimento e sonha em se tornar Hokage, o ninja líder de sua vila.'
    },
    {
      id: 3,
      title: 'Demon Slayer',
      cover: '/images/mangas/demon-slayer.jpg',
      author: 'Koyoharu Gotouge',
      genres: ['Ação', 'Sobrenatural', 'Histórico'],
      status: 'Completo',
      rating: 4.9,
      chapters: 205,
      description: 'Tanjiro Kamado e sua irmã Nezuko são os únicos sobreviventes de um incidente onde o resto de sua família foi morta por demônios.'
    }
  ];

  const filteredMangas = filter === 'all' 
    ? mangas 
    : mangas.filter(manga => 
        filter === 'ongoing' 
          ? manga.status === 'Em andamento' 
          : manga.status === 'Completo'
      );

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
              <option value="ongoing">Em andamento</option>
              <option value="completed">Completos</option>
            </select>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredMangas.map(manga => (
          <Link href={`/mangas/${manga.id}`} key={manga.id}>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
              <div className="h-48 bg-gray-200 dark:bg-gray-700 relative">
                {/* Placeholder for manga cover */}
                <div className="absolute inset-0 flex items-center justify-center text-gray-500 dark:text-gray-400">
                  <BookOpen className="w-12 h-12" />
                </div>
              </div>
              <div className="p-4">
                <div className="flex justify-between items-start">
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">{manga.title}</h2>
                  <div className="flex items-center gap-1 text-yellow-500">
                    <Star className="w-4 h-4 fill-current" />
                    <span className="text-sm">{manga.rating}</span>
                  </div>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">{manga.author}</p>
                <div className="flex flex-wrap gap-1 mt-2">
                  {manga.genres.map((genre, idx) => (
                    <span 
                      key={idx} 
                      className="text-xs bg-indigo-100 dark:bg-indigo-900 text-indigo-800 dark:text-indigo-200 px-2 py-1 rounded"
                    >
                      {genre}
                    </span>
                  ))}
                </div>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                  {manga.status} • {manga.chapters} capítulos
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-300 mt-2 line-clamp-2">
                  {manga.description}
                </p>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
