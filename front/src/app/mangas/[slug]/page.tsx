'use client';

import { useState } from 'react';
import { ArrowLeft, BookOpen, Star, Clock, Calendar, User, Tag, ChevronDown, ChevronUp, Heart } from 'lucide-react';
import Link from 'next/link';

export default function MangaDetailPage({ params }: { params: { slug: string } }) {
  const [showFullDescription, setShowFullDescription] = useState(false);
  const [isFavorite, setIsFavorite] = useState(false);

  // Mock data - in a real app, this would come from an API
  const manga = {
    id: parseInt(params.slug),
    title: params.slug === '1' ? 'One Piece' : params.slug === '2' ? 'Naruto' : 'Demon Slayer',
    cover: `/images/mangas/${params.slug === '1' ? 'one-piece' : params.slug === '2' ? 'naruto' : 'demon-slayer'}.jpg`,
    author: params.slug === '1' ? 'Eiichiro Oda' : params.slug === '2' ? 'Masashi Kishimoto' : 'Koyoharu Gotouge',
    genres: ['Ação', 'Aventura', 'Fantasia'],
    status: params.slug === '1' ? 'Em andamento' : 'Completo',
    rating: params.slug === '1' ? 4.8 : params.slug === '2' ? 4.7 : 4.9,
    chapters: params.slug === '1' ? 1089 : params.slug === '2' ? 700 : 205,
    description: params.slug === '1'
      ? 'A história segue Monkey D. Luffy, um jovem cujo corpo ganhou as propriedades de borracha após ter comido uma fruta do diabo acidentalmente. Com sua tripulação, os Piratas do Chapéu de Palha, Luffy explora a Grand Line em busca do tesouro mais procurado do mundo, o "One Piece", a fim de se tornar o próximo Rei dos Piratas. A série é conhecida por seu mundo vasto e detalhado, personagens carismáticos, humor, drama e combates emocionantes.'
      : params.slug === '2'
      ? 'Naruto Uzumaki é um jovem ninja que constantemente procura por reconhecimento e sonha em se tornar Hokage, o ninja líder de sua vila. A história é dividida em duas partes, a primeira parte segue as aventuras de Naruto pré-adolescente, e a segunda parte segue Naruto em sua adolescência. A série é centrada em temas de amizade, traição, redenção e o conceito de destino e livre arbítrio.'
      : 'Tanjiro Kamado e sua irmã Nezuko são os únicos sobreviventes de um incidente onde o resto de sua família foi morta por demônios. Nezuko foi transformada em um demônio, mas surpreendentemente ainda mostra sinais de emoções e pensamentos humanos. Tanjiro se torna um caçador de demônios para ajudar sua irmã a se tornar humana novamente e para impedir que a mesma tragédia aconteça com outras pessoas.',
    publishedDate: '1997-07-22',
    lastUpdated: '2023-08-06',
    chapters: [
      { number: 1, title: 'Capítulo 1', date: '1997-07-22' },
      { number: 2, title: 'Capítulo 2', date: '1997-07-29' },
      { number: 3, title: 'Capítulo 3', date: '1997-08-05' },
      // More chapters would be here
    ]
  };

  return (
    <div className="space-y-8">
      <div className="flex items-center gap-4">
        <Link href="/mangas" className="text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 dark:hover:text-indigo-300 flex items-center gap-1">
          <ArrowLeft className="w-5 h-5" />
          <span>Voltar</span>
        </Link>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
        <div className="md:flex">
          <div className="md:w-1/3 lg:w-1/4 bg-gray-200 dark:bg-gray-700 h-64 md:h-auto relative">
            {/* Placeholder for manga cover */}
            <div className="absolute inset-0 flex items-center justify-center text-gray-500 dark:text-gray-400">
              <BookOpen className="w-16 h-16" />
            </div>
          </div>
          <div className="p-6 md:w-2/3 lg:w-3/4">
            <div className="flex justify-between items-start">
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">{manga.title}</h1>
              <button
                onClick={() => setIsFavorite(!isFavorite)}
                className={`p-2 rounded-full ${isFavorite ? 'bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-300' : 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400'}`}
              >
                <Heart className={`w-5 h-5 ${isFavorite ? 'fill-current' : ''}`} />
              </button>
            </div>

            <div className="flex items-center gap-2 mt-2">
              <div className="flex items-center gap-1 text-yellow-500">
                <Star className="w-5 h-5 fill-current" />
                <span className="font-medium">{manga.rating}</span>
              </div>
              <span className="text-gray-500 dark:text-gray-400">•</span>
              <span className="text-gray-600 dark:text-gray-300">{manga.status}</span>
              <span className="text-gray-500 dark:text-gray-400">•</span>
              <span className="text-gray-600 dark:text-gray-300">{manga.chapters} capítulos</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
              <div className="flex items-center gap-2 text-gray-600 dark:text-gray-300">
                <User className="w-5 h-5 text-gray-500 dark:text-gray-400" />
                <span>Autor: <span className="font-medium">{manga.author}</span></span>
              </div>
              <div className="flex items-center gap-2 text-gray-600 dark:text-gray-300">
                <Calendar className="w-5 h-5 text-gray-500 dark:text-gray-400" />
                <span>Publicado: <span className="font-medium">{manga.publishedDate}</span></span>
              </div>
              <div className="flex items-center gap-2 text-gray-600 dark:text-gray-300">
                <Clock className="w-5 h-5 text-gray-500 dark:text-gray-400" />
                <span>Última atualização: <span className="font-medium">{manga.lastUpdated}</span></span>
              </div>
              <div className="flex items-center gap-2 text-gray-600 dark:text-gray-300">
                <Tag className="w-5 h-5 text-gray-500 dark:text-gray-400" />
                <span>Gêneros: <span className="font-medium">{manga.genres.join(', ')}</span></span>
              </div>
            </div>

            <div className="mt-6">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Sinopse</h2>
              <div className="relative">
                <p className={`text-gray-600 dark:text-gray-300 ${!showFullDescription && 'line-clamp-3'}`}>
                  {manga.description}
                </p>
                {manga.description.length > 200 && (
                  <button
                    onClick={() => setShowFullDescription(!showFullDescription)}
                    className="mt-2 text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 dark:hover:text-indigo-300 flex items-center gap-1"
                  >
                    {showFullDescription ? (
                      <>
                        <ChevronUp className="w-4 h-4" />
                        <span>Mostrar menos</span>
                      </>
                    ) : (
                      <>
                        <ChevronDown className="w-4 h-4" />
                        <span>Mostrar mais</span>
                      </>
                    )}
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Capítulos</h2>
        <div className="space-y-2">
          {manga.chapters.map((chapter) => (
            <Link
              href={`/mangas/${params.slug}/chapters/${chapter.number}`}
              key={chapter.number}
              className="block p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            >
              <div className="flex justify-between items-center">
                <div>
                  <span className="font-medium text-gray-900 dark:text-white">Capítulo {chapter.number}</span>
                  <span className="ml-2 text-gray-600 dark:text-gray-300">{chapter.title}</span>
                </div>
                <span className="text-sm text-gray-500 dark:text-gray-400">{chapter.date}</span>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
