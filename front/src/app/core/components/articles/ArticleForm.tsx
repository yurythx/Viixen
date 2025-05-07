'use client';

import { useState, useEffect } from 'react';
import { Article, ArticleCreateData, ArticleUpdateData, Category } from '../../types/models';
import { useRouter } from 'next/navigation';
import { articlesService, categoriesService } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';
import { useNotification } from '../../contexts/NotificationContext';
import RichTextEditor from '../ui/RichTextEditor';

interface ArticleFormProps {
  article?: Article;
  onSuccess?: () => void;
}

export default function ArticleForm({ article, onSuccess }: ArticleFormProps) {
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const { showNotification } = useNotification();
  const [title, setTitle] = useState(article?.title || '');
  const [content, setContent] = useState(article?.content || '');
  const [categoryId, setCategoryId] = useState<number | undefined>(article?.category_id);
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoadingCategories, setIsLoadingCategories] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const isEditing = !!article;

  useEffect(() => {
    // Redirecionar se não estiver autenticado
    if (!isAuthenticated) {
      router.push('/login?redirect=/artigos/novo');
    }
  }, [isAuthenticated, router]);

  useEffect(() => {
    // Atualizar campos quando o artigo mudar
    if (article) {
      setTitle(article.title);
      setContent(article.content);
      setCategoryId(article.category_id);
    }
  }, [article]);

  // Carregar categorias
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setIsLoadingCategories(true);
        const data = await categoriesService.getCategories();
        setCategories(data);
      } catch (err) {
        console.error('Erro ao carregar categorias:', err);
        showNotification('error', 'Não foi possível carregar as categorias.');
      } finally {
        setIsLoadingCategories(false);
      }
    };

    fetchCategories();
  }, [showNotification]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim() || !content.trim()) {
      setError('Por favor, preencha todos os campos.');
      return;
    }

    try {
      setIsSubmitting(true);
      setError(null);

      if (isEditing && article) {
        // Atualizar artigo existente
        const data: ArticleUpdateData = {
          title: title.trim(),
          content: content.trim(),
          category_id: categoryId
        };

        const updatedArticle = await articlesService.updateArticle(article.slug, data);

        showNotification('success', 'Artigo atualizado com sucesso!');

        if (onSuccess) {
          onSuccess();
        } else {
          router.push(`/artigos/${updatedArticle.slug}`);
        }
      } else {
        // Criar novo artigo
        const data: ArticleCreateData = {
          title: title.trim(),
          content: content.trim(),
          category_id: categoryId
        };

        const newArticle = await articlesService.createArticle(data);

        showNotification('success', 'Artigo criado com sucesso!');

        if (onSuccess) {
          onSuccess();
        } else {
          router.push(`/artigos/${newArticle.slug}`);
        }
      }
    } catch (err: any) {
      console.error('Erro ao salvar artigo:', err);
      const errorMessage = err.message || 'Ocorreu um erro ao salvar o artigo. Por favor, tente novamente.';
      setError(errorMessage);
      showNotification('error', errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Título
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
          placeholder="Digite o título do artigo"
          required
        />
      </div>

      <div>
        <label htmlFor="content" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Conteúdo
        </label>
        <RichTextEditor
          value={content}
          onChange={setContent}
          height={400}
          placeholder="Digite o conteúdo do artigo..."
        />
      </div>

      <div>
        <label htmlFor="category" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Categoria
        </label>
        <select
          id="category"
          value={categoryId || ''}
          onChange={(e) => setCategoryId(e.target.value ? Number(e.target.value) : undefined)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
        >
          <option value="">Selecione uma categoria</option>
          {isLoadingCategories ? (
            <option disabled>Carregando categorias...</option>
          ) : (
            categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))
          )}
        </select>
      </div>

      <div className="flex justify-end">
        <button
          type="button"
          onClick={() => router.back()}
          className="mr-4 px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 dark:bg-gray-700 dark:text-white dark:border-gray-600 dark:hover:bg-gray-600"
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={isSubmitting}
          className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {isSubmitting ? 'Salvando...' : isEditing ? 'Atualizar' : 'Publicar'}
        </button>
      </div>
    </form>
  );
}
