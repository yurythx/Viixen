'use client';

import Header from './components/Header';
import Hero from './components/Hero';
import FeaturedArticles from './components/FeaturedArticles';
import { useState } from 'react';
import { FileText, Filter, Clock, Tag } from 'lucide-react';
import Link from 'next/link';

export default function ArtigosPage() {
  const [filter, setFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  const artigos = [
    {
      id: 1,
      title: 'Como Criar um Blog com Next.js',
      excerpt: 'Um guia completo para criar um blog moderno usando Next.js, Tailwind CSS e TypeScript.',
      author: 'João Silva',
      date: '2023-08-15',
      readTime: '5 min',
      category: 'Tecnologia',
      tags: ['Next.js', 'React', 'Web Development'],
      featured: true
    },
    {
      id: 2,
      title: 'Introdução ao TypeScript',
      excerpt: 'Aprenda os conceitos básicos do TypeScript e como ele pode melhorar seu desenvolvimento.',
      author: 'Maria Souza',
      date: '2023-07-22',
      readTime: '8 min',
      category: 'Programação',
      tags: ['TypeScript', 'JavaScript', 'Programação'],
      featured: false
    },
    {
      id: 3,
      title: 'Tailwind CSS: Guia Definitivo',
      excerpt: 'Domine o Tailwind CSS e crie interfaces modernas com facilidade.',
      author: 'Pedro Oliveira',
      date: '2023-06-10',
      readTime: '6 min',
      category: 'Design',
      tags: ['CSS', 'Tailwind', 'UI/UX'],
      featured: true
    },
    {
      id: 4,
      title: 'Os Melhores Mangás de 2023',
      excerpt: 'Uma lista completa dos mangás mais populares e bem avaliados deste ano.',
      author: 'Ana Costa',
      date: '2023-09-05',
      readTime: '10 min',
      category: 'Mangá',
      tags: ['Mangá', 'Anime', 'Cultura Japonesa'],
      featured: true
    },
    {
      id: 5,
      title: 'História dos Mangás no Ocidente',
      excerpt: 'Como os mangás conquistaram o público ocidental e transformaram a indústria de quadrinhos.',
      author: 'Carlos Mendes',
      date: '2023-05-18',
      readTime: '12 min',
      category: 'Cultura',
      tags: ['Mangá', 'História', 'Cultura'],
      featured: false
    }
  ];

  const filteredArtigos = filter === 'all'
    ? artigos
    : filter === 'featured'
      ? artigos.filter(artigo => artigo.featured)
      : artigos.filter(artigo => artigo.category.toLowerCase() === filter);

  const searchedArtigos = searchQuery
    ? filteredArtigos.filter(artigo =>
        artigo.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        artigo.excerpt.toLowerCase().includes(searchQuery.toLowerCase()) ||
        artigo.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
      )
    : filteredArtigos;

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
                  <option value="featured">Destaques</option>
                  <option value="tecnologia">Tecnologia</option>
                  <option value="programação">Programação</option>
                  <option value="design">Design</option>
                  <option value="mangá">Mangá</option>
                  <option value="cultura">Cultura</option>
                </select>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {searchedArtigos.map(artigo => (
              <Link href={`/artigos/${artigo.id}`} key={artigo.id}>
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow h-full flex flex-col">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 text-sm text-indigo-600 dark:text-indigo-400 mb-2">
                      <Tag className="w-4 h-4" />
                      <span>{artigo.category}</span>
                      {artigo.featured && (
                        <span className="bg-indigo-100 dark:bg-indigo-900 text-indigo-800 dark:text-indigo-200 px-2 py-0.5 rounded text-xs ml-2">
                          Destaque
                        </span>
                      )}
                    </div>
                    <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                      {artigo.title}
                    </h2>
                    <p className="text-gray-600 dark:text-gray-300 mb-4">
                      {artigo.excerpt}
                    </p>
                    <div className="flex flex-wrap gap-1 mt-2">
                      {artigo.tags.map((tag, idx) => (
                        <span
                          key={idx}
                          className="text-xs bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-2 py-1 rounded"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      {artigo.author}
                    </span>
                    <div className="flex items-center gap-1 text-sm text-gray-500 dark:text-gray-400">
                      <Clock className="w-4 h-4" />
                      <span>{artigo.readTime}</span>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
