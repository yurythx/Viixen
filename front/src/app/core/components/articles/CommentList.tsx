'use client';

import React, { useState } from 'react';
import { Comment } from '../../types/models';
import { MessageSquare, Reply, Trash2, Edit } from 'lucide-react';
import CommentForm from './CommentForm';
import { useAuth } from '../../contexts/AuthContext';
import { articlesService } from '../../services/api';
import { useNotification } from '../../contexts/NotificationContext';

interface CommentItemProps {
  comment: Comment;
  articleId: number;
  onCommentAdded: () => void;
}

const CommentItem: React.FC<CommentItemProps> = ({ comment, articleId, onCommentAdded }) => {
  const { isAuthenticated, user } = useAuth();
  const { showNotification } = useNotification();
  const [showReplyForm, setShowReplyForm] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  // Função para formatar a data
  const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('pt-BR', options);
  };

  const handleDeleteComment = async () => {
    try {
      setIsDeleting(true);
      await articlesService.deleteComment(comment.id);

      // Mostrar notificação de sucesso
      showNotification('success', 'Comentário excluído com sucesso!');

      onCommentAdded(); // Atualizar a lista de comentários
      setShowDeleteConfirm(false);
    } catch (err: any) {
      console.error('Erro ao excluir comentário:', err);
      const errorMessage = 'Não foi possível excluir o comentário. Por favor, tente novamente.';
      setError(errorMessage);
      showNotification('error', errorMessage);
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div className="border-l-2 border-gray-200 dark:border-gray-700 pl-4 mb-4">
      <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
        <div className="flex justify-between items-start">
          <div>
            <h4 className="font-medium text-gray-900 dark:text-white">{comment.name}</h4>
            <span className="text-xs text-gray-500 dark:text-gray-400">
              {formatDate(comment.created_at)}
            </span>
          </div>

          {isAuthenticated && (
            <div className="flex space-x-2">
              <button
                onClick={() => setShowReplyForm(!showReplyForm)}
                className="text-indigo-600 hover:text-indigo-800 focus:outline-none"
                title={showReplyForm ? 'Cancelar resposta' : 'Responder'}
              >
                <Reply className="w-4 h-4" />
              </button>

              {/* Apenas o administrador pode excluir comentários */}
              {user && user.is_active && (
                <button
                  onClick={() => setShowDeleteConfirm(true)}
                  className="text-red-600 hover:text-red-800 focus:outline-none"
                  title="Excluir comentário"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              )}
            </div>
          )}
        </div>

        <p className="mt-2 text-gray-600 dark:text-gray-300">{comment.text}</p>

        {!isAuthenticated && (
          <button
            onClick={() => setShowReplyForm(!showReplyForm)}
            className="mt-2 flex items-center text-sm text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300"
          >
            <Reply className="w-4 h-4 mr-1" />
            {showReplyForm ? 'Cancelar resposta' : 'Responder'}
          </button>
        )}
      </div>

      {showReplyForm && (
        <div className="mt-2 ml-4">
          <CommentForm
            articleId={articleId}
            parentId={comment.id}
            onCommentAdded={() => {
              onCommentAdded();
              setShowReplyForm(false);
            }}
            onCancel={() => setShowReplyForm(false)}
            isReply={true}
          />
        </div>
      )}

      {/* Modal de confirmação de exclusão */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
              Confirmar exclusão
            </h3>

            <p className="text-gray-700 dark:text-gray-300 mb-6">
              Tem certeza que deseja excluir este comentário? Esta ação não pode ser desfeita.
            </p>

            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                {error}
              </div>
            )}

            <div className="flex justify-end space-x-4">
              <button
                type="button"
                onClick={() => setShowDeleteConfirm(false)}
                className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 dark:bg-gray-700 dark:text-white dark:border-gray-600 dark:hover:bg-gray-600"
                disabled={isDeleting}
              >
                Cancelar
              </button>
              <button
                type="button"
                onClick={handleDeleteComment}
                className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
                disabled={isDeleting}
              >
                {isDeleting ? 'Excluindo...' : 'Excluir'}
              </button>
            </div>
          </div>
        </div>
      )}

      {comment.replies && comment.replies.length > 0 && (
        <div className="ml-4 mt-2">
          {comment.replies.map((reply) => (
            <CommentItem
              key={reply.id}
              comment={reply}
              articleId={articleId}
              onCommentAdded={onCommentAdded}
            />
          ))}
        </div>
      )}
    </div>
  );
};

interface CommentListProps {
  comments: Comment[];
  articleId: number;
  onCommentAdded: () => void;
}

const CommentList: React.FC<CommentListProps> = ({ comments, articleId, onCommentAdded }) => {
  return (
    <div className="mt-8">
      <h3 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center mb-4">
        <MessageSquare className="w-5 h-5 mr-2" />
        Comentários ({comments.length})
      </h3>

      {comments.length === 0 ? (
        <p className="text-gray-500 dark:text-gray-400">Nenhum comentário ainda. Seja o primeiro a comentar!</p>
      ) : (
        <div className="space-y-4">
          {comments.map((comment) => (
            <CommentItem
              key={comment.id}
              comment={comment}
              articleId={articleId}
              onCommentAdded={onCommentAdded}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default CommentList;
