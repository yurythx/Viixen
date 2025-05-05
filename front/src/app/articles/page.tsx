// src/app/articles/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { Article, getArticles, deleteArticle } from '@/services/articles';
import { motion } from 'framer-motion';
import { PencilIcon, TrashIcon, PlusIcon } from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import Modal from '@/components/Modal';
import ArticleForm from '@/components/ArticleForm';
import Button from '@/components/Button';

export default function ArticlesPage() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedArticle, setSelectedArticle] = useState<Article | null>(null);

  const fetchArticles = async () => {
    try {
      const data = await getArticles();
      setArticles(data);
    } catch (err) {
      console.error('Erro ao carregar artigos:', err);
      setError('Não foi possível carregar os artigos. Por favor, tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchArticles();
  }, []);

  const handleDelete = async (article: Article) => {
    if (!confirm('Tem certeza que deseja excluir este artigo?')) return;

    try {
      await deleteArticle(article.id);
      toast.success('Artigo excluído com sucesso!');
      fetchArticles();
    } catch (error) {
      console.error('Erro ao excluir artigo:', error);
      toast.error('Não foi possível excluir o artigo. Por favor, tente novamente.');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse space-y-8">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="bg-white shadow-sm rounded-lg p-6">
                <div className="h-6 bg-gray-200 rounded w-3/4 mb-4"></div>
                <div className="space-y-3">
                  <div className="h-4 bg-gray-200 rounded"></div>
                  <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-red-50 border border-red-200 rounded-md p-4">
            <p className="text-red-700">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Artigos</h1>
          <Button
            onClick={() => setShowCreateModal(true)}
            leftIcon={<PlusIcon className="h-5 w-5" />}
          >
            Novo Artigo
          </Button>
        </div>

        {articles.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <p className="text-gray-500 mb-4">Nenhum artigo encontrado.</p>
            <Button
              onClick={() => setShowCreateModal(true)}
              variant="secondary"
              leftIcon={<PlusIcon className="h-5 w-5" />}
            >
              Criar Artigo
            </Button>
          </motion.div>
        ) : (
          <div className="space-y-6">
            {articles.map((article) => (
              <motion.div
                key={article.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className="bg-white shadow-sm rounded-lg overflow-hidden"
              >
                <div className="p-6">
                  <div className="flex justify-between items-start">
                    <div>
                      <h2 className="text-xl font-semibold text-gray-900 mb-2">
                        {article.title}
                      </h2>
                      <p className="text-gray-600 line-clamp-2">{article.content}</p>
                      <p className="mt-2 text-sm text-gray-500">
                        Publicado em {new Date(article.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="flex space-x-2">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => {
                          setSelectedArticle(article);
                          setShowEditModal(true);
                        }}
                        leftIcon={<PencilIcon className="h-5 w-5" />}
                      >
                        Editar
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleDelete(article)}
                        leftIcon={<TrashIcon className="h-5 w-5" />}
                      >
                        Excluir
                      </Button>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}

        <Modal
          isOpen={showCreateModal}
          onClose={() => setShowCreateModal(false)}
          title="Criar Novo Artigo"
        >
          <ArticleForm
            onSuccess={() => {
              setShowCreateModal(false);
              fetchArticles();
            }}
            onCancel={() => setShowCreateModal(false)}
          />
        </Modal>

        <Modal
          isOpen={showEditModal}
          onClose={() => {
            setShowEditModal(false);
            setSelectedArticle(null);
          }}
          title="Editar Artigo"
        >
          {selectedArticle && (
            <ArticleForm
              article={selectedArticle}
              onSuccess={() => {
                setShowEditModal(false);
                setSelectedArticle(null);
                fetchArticles();
              }}
              onCancel={() => {
                setShowEditModal(false);
                setSelectedArticle(null);
              }}
            />
          )}
        </Modal>
      </div>
    </div>
  );
}