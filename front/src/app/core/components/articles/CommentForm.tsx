'use client';

import React, { useState, useEffect } from 'react';
import { CommentCreateData } from '../../types/models';
import { articlesService } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';
import { useNotification } from '../../contexts/NotificationContext';

interface CommentFormProps {
  articleId: number;
  parentId?: number | null;
  onCommentAdded: () => void;
  onCancel?: () => void;
  isReply?: boolean;
}

const CommentForm: React.FC<CommentFormProps> = ({
  articleId,
  parentId = null,
  onCommentAdded,
  onCancel,
  isReply = false
}) => {
  const { user } = useAuth();
  const { showNotification } = useNotification();
  const [formData, setFormData] = useState<CommentCreateData>({
    name: '',
    text: '',
    article: articleId,
    parent: parentId,
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Preencher o nome com o nome do usuário logado, se disponível
  useEffect(() => {
    if (user) {
      const userName = `${user.first_name} ${user.last_name}`.trim() || user.username;
      setFormData(prev => ({ ...prev, name: userName }));
    }
  }, [user]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.name.trim() || !formData.text.trim()) {
      setError('Por favor, preencha todos os campos.');
      return;
    }

    setError(null);
    setIsSubmitting(true);

    try {
      const comment = await articlesService.createComment(formData);

      // Limpar apenas o texto, mantendo o nome
      setFormData(prev => ({
        ...prev,
        text: '',
      }));

      // Mostrar notificação de sucesso
      showNotification(
        'success',
        isReply ? 'Resposta adicionada com sucesso!' : 'Comentário adicionado com sucesso!'
      );

      // Notificar que o comentário foi adicionado
      onCommentAdded();

      // Fechar o formulário de resposta se for uma resposta
      if (isReply && onCancel) {
        onCancel();
      }
    } catch (err: any) {
      console.error('Erro ao adicionar comentário:', err);
      let errorMessage = 'Ocorreu um erro ao adicionar o comentário. Por favor, tente novamente.';

      if (err.data) {
        // Formatar mensagens de erro
        errorMessage = Object.entries(err.data)
          .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
          .join('; ');
      }

      setError(errorMessage);
      showNotification('error', errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={`space-y-4 ${isReply ? 'bg-gray-100 dark:bg-gray-750' : 'bg-gray-50 dark:bg-gray-700'} p-4 rounded-lg`}>
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div>
        <label htmlFor={`name-${parentId || 'main'}`} className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Nome
        </label>
        <input
          type="text"
          id={`name-${parentId || 'main'}`}
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
          className="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-800 dark:text-white"
        />
      </div>

      <div>
        <label htmlFor={`text-${parentId || 'main'}`} className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Comentário
        </label>
        <textarea
          id={`text-${parentId || 'main'}`}
          name="text"
          value={formData.text}
          onChange={handleChange}
          required
          rows={isReply ? 3 : 4}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-800 dark:text-white"
          placeholder="Digite seu comentário"
        />
      </div>

      <div className="flex justify-end space-x-2">
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="py-2 px-4 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Cancelar
          </button>
        )}
        <button
          type="submit"
          disabled={isSubmitting}
          className="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {isSubmitting ? 'Enviando...' : isReply ? 'Responder' : 'Enviar Comentário'}
        </button>
      </div>
    </form>
  );
};

export default CommentForm;
