// components/ArticleForm.tsx
'use client';
import { useState } from 'react';
import { Article, CreateArticleData, UpdateArticleData, createArticle, updateArticle } from '@/services/articles';
import toast from 'react-hot-toast';
import { motion } from 'framer-motion';
import Button from './Button';

interface ArticleFormProps {
  article?: Article;
  onSuccess: () => void;
  onCancel: () => void;
}

export default function ArticleForm({ article, onSuccess, onCancel }: ArticleFormProps) {
  const [title, setTitle] = useState(article?.title || '');
  const [content, setContent] = useState(article?.content || '');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) return;

    setLoading(true);
    try {
      if (article) {
        await updateArticle(article.id, { title, content });
        toast.success('Artigo atualizado com sucesso!');
      } else {
        await createArticle({ title, content });
        toast.success('Artigo criado com sucesso!');
      }
      onSuccess();
    } catch (error) {
      console.error('Erro ao salvar artigo:', error);
      toast.error('Não foi possível salvar o artigo. Por favor, tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.form
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      onSubmit={handleSubmit}
      className="space-y-6"
    >
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700">
          Título
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Digite o título do artigo"
          required
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm"
        />
      </div>

      <div>
        <label htmlFor="content" className="block text-sm font-medium text-gray-700">
          Conteúdo
        </label>
        <textarea
          id="content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Digite o conteúdo do artigo"
          required
          rows={12}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm"
        />
      </div>

      <div className="flex justify-end space-x-4">
        <Button
          type="button"
          variant="secondary"
          onClick={onCancel}
        >
          Cancelar
        </Button>
        <Button
          type="submit"
          variant="primary"
          isLoading={loading}
        >
          {article ? 'Atualizar' : 'Criar'}
        </Button>
      </div>
    </motion.form>
  );
}
