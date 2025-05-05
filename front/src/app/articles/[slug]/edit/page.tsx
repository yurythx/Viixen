// app/articles/[slug]/edit/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Article, getArticleBySlug } from '@/services/articles';
import ArticleForm from '@/components/ArticleForm';
import { motion } from 'framer-motion';

export default function EditArticlePage() {
  const params = useParams();
  const router = useRouter();
  const [article, setArticle] = useState<Article | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchArticle = async () => {
      if (!params?.slug) {
        setError('Slug do artigo não encontrado');
        setLoading(false);
        return;
      }

      try {
        const slug = params.slug as string;
        const data = await getArticleBySlug(slug);
        setArticle(data);
      } catch (err) {
        setError('Não foi possível carregar o artigo. Por favor, tente novamente.');
        console.error('Erro ao carregar artigo:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchArticle();
  }, [params?.slug]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/4 mb-8"></div>
            <div className="space-y-4">
              <div className="h-4 bg-gray-200 rounded"></div>
              <div className="h-4 bg-gray-200 rounded"></div>
              <div className="h-4 bg-gray-200 rounded w-5/6"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !article) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-red-50 border border-red-200 rounded-md p-4">
            <p className="text-red-700">{error || 'Artigo não encontrado.'}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-white shadow-sm rounded-lg overflow-hidden"
        >
          <div className="p-6 sm:p-8">
            <motion.h1
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="text-3xl font-bold text-gray-900 mb-8"
            >
              Editar Artigo
            </motion.h1>

            <ArticleForm
              article={article}
              onSuccess={() => router.push('/articles')}
              onCancel={() => router.push('/articles')}
            />
          </div>
        </motion.div>
      </div>
    </div>
  );
}
