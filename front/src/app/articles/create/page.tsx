// app/articles/create/page.tsx
'use client';

import { useRouter } from 'next/navigation';
import ArticleForm from '@/components/ArticleForm';
import { motion } from 'framer-motion';

export default function CreateArticlePage() {
  const router = useRouter();

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
              Criar Novo Artigo
            </motion.h1>

            <ArticleForm
              onSuccess={() => router.push('/articles')}
              onCancel={() => router.push('/articles')}
            />
          </div>
        </motion.div>
      </div>
    </div>
  );
}