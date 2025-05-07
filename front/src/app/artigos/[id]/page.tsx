'use client';

import { useState } from 'react';
import { ArrowLeft, Calendar, Clock, User, Tag, Share2, Bookmark, BookmarkCheck, MessageSquare } from 'lucide-react';
import Link from 'next/link';

export default function ArtigoDetailPage({ params }: { params: { id: string } }) {
  const [isSaved, setIsSaved] = useState(false);
  
  // Mock data - em uma aplicação real, isso viria de uma API
  const artigo = {
    id: parseInt(params.id),
    title: params.id === '1' 
      ? 'Como Criar um Blog com Next.js' 
      : params.id === '2' 
        ? 'Introdução ao TypeScript' 
        : params.id === '3' 
          ? 'Tailwind CSS: Guia Definitivo' 
          : params.id === '4' 
            ? 'Os Melhores Mangás de 2023' 
            : 'História dos Mangás no Ocidente',
    content: `
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl. Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl.</p>
      
      <h2>Introdução</h2>
      <p>Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl. Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl.</p>
      
      <p>Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl. Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl.</p>
      
      <h2>Desenvolvimento</h2>
      <p>Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl. Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl.</p>
      
      <ul>
        <li>Item 1</li>
        <li>Item 2</li>
        <li>Item 3</li>
      </ul>
      
      <p>Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl. Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl.</p>
      
      <h2>Conclusão</h2>
      <p>Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl. Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl.</p>
    `,
    author: params.id === '1' 
      ? 'João Silva' 
      : params.id === '2' 
        ? 'Maria Souza' 
        : params.id === '3' 
          ? 'Pedro Oliveira' 
          : params.id === '4' 
            ? 'Ana Costa' 
            : 'Carlos Mendes',
    authorAvatar: '/images/avatars/default.jpg',
    date: params.id === '1' 
      ? '2023-08-15' 
      : params.id === '2' 
        ? '2023-07-22' 
        : params.id === '3' 
          ? '2023-06-10' 
          : params.id === '4' 
            ? '2023-09-05' 
            : '2023-05-18',
    readTime: params.id === '1' 
      ? '5 min' 
      : params.id === '2' 
        ? '8 min' 
        : params.id === '3' 
          ? '6 min' 
          : params.id === '4' 
            ? '10 min' 
            : '12 min',
    category: params.id === '1' 
      ? 'Tecnologia' 
      : params.id === '2' 
        ? 'Programação' 
        : params.id === '3' 
          ? 'Design' 
          : params.id === '4' 
            ? 'Mangá' 
            : 'Cultura',
    tags: params.id === '1' 
      ? ['Next.js', 'React', 'Web Development'] 
      : params.id === '2' 
        ? ['TypeScript', 'JavaScript', 'Programação'] 
        : params.id === '3' 
          ? ['CSS', 'Tailwind', 'UI/UX'] 
          : params.id === '4' 
            ? ['Mangá', 'Anime', 'Cultura Japonesa'] 
            : ['Mangá', 'História', 'Cultura'],
    comments: 5,
    relatedArticles: [
      { id: 1, title: 'Como Criar um Blog com Next.js' },
      { id: 2, title: 'Introdução ao TypeScript' },
      { id: 3, title: 'Tailwind CSS: Guia Definitivo' }
    ].filter(article => article.id !== parseInt(params.id)).slice(0, 2)
  };

  // Formatar a data
  const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('pt-BR', options);
  };

  return (
    <div className="space-y-8">
      <div className="flex items-center gap-4">
        <Link href="/artigos" className="text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 dark:hover:text-indigo-300 flex items-center gap-1">
          <ArrowLeft className="w-5 h-5" />
          <span>Voltar para Artigos</span>
        </Link>
      </div>

      <article className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
        <div className="p-6 md:p-8">
          <div className="flex items-center gap-2 text-sm text-indigo-600 dark:text-indigo-400 mb-4">
            <Tag className="w-4 h-4" />
            <span>{artigo.category}</span>
          </div>
          
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-6">
            {artigo.title}
          </h1>
          
          <div className="flex flex-wrap items-center gap-4 mb-8 text-sm text-gray-600 dark:text-gray-300">
            <div className="flex items-center gap-2">
              <User className="w-4 h-4 text-gray-500 dark:text-gray-400" />
              <span>{artigo.author}</span>
            </div>
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-gray-500 dark:text-gray-400" />
              <span>{formatDate(artigo.date)}</span>
            </div>
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-gray-500 dark:text-gray-400" />
              <span>{artigo.readTime} de leitura</span>
            </div>
            <div className="flex items-center gap-2">
              <MessageSquare className="w-4 h-4 text-gray-500 dark:text-gray-400" />
              <span>{artigo.comments} comentários</span>
            </div>
          </div>
          
          <div className="flex flex-wrap gap-2 mb-8">
            {artigo.tags.map((tag, idx) => (
              <span 
                key={idx} 
                className="text-xs bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-2 py-1 rounded"
              >
                #{tag}
              </span>
            ))}
          </div>
          
          <div 
            className="prose prose-indigo dark:prose-invert max-w-none mb-8"
            dangerouslySetInnerHTML={{ __html: artigo.content }}
          />
          
          <div className="flex justify-between items-center pt-6 border-t border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-4">
              <button className="flex items-center gap-2 text-gray-600 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400">
                <Share2 className="w-5 h-5" />
                <span>Compartilhar</span>
              </button>
              <button 
                className="flex items-center gap-2 text-gray-600 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400"
                onClick={() => setIsSaved(!isSaved)}
              >
                {isSaved ? (
                  <>
                    <BookmarkCheck className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                    <span className="text-indigo-600 dark:text-indigo-400">Salvo</span>
                  </>
                ) : (
                  <>
                    <Bookmark className="w-5 h-5" />
                    <span>Salvar</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </article>

      {artigo.relatedArticles.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Artigos Relacionados</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {artigo.relatedArticles.map((related) => (
              <Link href={`/artigos/${related.id}`} key={related.id}>
                <div className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                  <h3 className="font-medium text-gray-900 dark:text-white">{related.title}</h3>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
