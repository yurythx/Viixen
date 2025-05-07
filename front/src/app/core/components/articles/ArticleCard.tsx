'use client';

import React from 'react';
import Link from 'next/link';
import { Article } from '../../types/models';
import { Clock, MessageSquare, Tag } from 'lucide-react';

interface ArticleCardProps {
  article: Article;
}

const ArticleCard: React.FC<ArticleCardProps> = ({ article }) => {
  // Função para formatar a data
  const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('pt-BR', options);
  };

  // Extrair um resumo do conteúdo (primeiros 150 caracteres)
  const getExcerpt = (content: string) => {
    // Remover tags HTML
    const plainText = content.replace(/<[^>]+>/g, '');
    return plainText.length > 150 ? `${plainText.substring(0, 150)}...` : plainText;
  };

  return (
    <Link href={`/artigos/${article.slug}`}>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow h-full flex flex-col">
        <div className="flex-1">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            {article.title}
          </h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            {getExcerpt(article.content)}
          </p>
        </div>
        <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
          {article.category && (
            <div className="flex items-center mb-2 text-sm text-indigo-600 dark:text-indigo-400">
              <Tag className="w-4 h-4 mr-1" />
              <span>{article.category.name}</span>
            </div>
          )}
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-500 dark:text-gray-400">
              {formatDate(article.created_at)}
            </div>
            <div className="flex items-center gap-1 text-sm text-gray-500 dark:text-gray-400">
              <MessageSquare className="w-4 h-4" />
              <span>{article.comments_count || 0}</span>
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default ArticleCard;
