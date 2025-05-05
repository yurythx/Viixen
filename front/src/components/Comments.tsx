'use client';

import { useState } from 'react';
import { Comment, CreateCommentData, UpdateCommentData, createComment, updateComment, deleteComment } from '@/services/articles';
import toast from 'react-hot-toast';
import { motion } from 'framer-motion';
import { PencilIcon, TrashIcon, ArrowUturnLeftIcon } from '@heroicons/react/24/outline';

interface CommentsProps {
  articleSlug: string;
  comments: Comment[];
  onCommentAdded: () => void;
  onCommentUpdated: () => void;
  onCommentDeleted: () => void;
}

export default function Comments({ articleSlug, comments, onCommentAdded, onCommentUpdated, onCommentDeleted }: CommentsProps) {
  const [newComment, setNewComment] = useState('');
  const [newName, setNewName] = useState('');
  const [replyingTo, setReplyingTo] = useState<number | null>(null);
  const [editingComment, setEditingComment] = useState<number | null>(null);
  const [editText, setEditText] = useState('');
  const [editName, setEditName] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmitComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newComment.trim() || !newName.trim()) return;

    setLoading(true);
    try {
      const data: CreateCommentData = {
        name: newName,
        text: newComment,
        article_slug: articleSlug,
        parent_id: replyingTo || undefined
      };
      await createComment(data);
      toast.success('Comentário adicionado com sucesso!');
      setNewComment('');
      setNewName('');
      setReplyingTo(null);
      onCommentAdded();
    } catch (error) {
      console.error('Erro ao adicionar comentário:', error);
      toast.error('Não foi possível adicionar o comentário. Por favor, tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateComment = async (commentId: number) => {
    if (!editText.trim() || !editName.trim()) return;

    setLoading(true);
    try {
      const data: UpdateCommentData = {
        name: editName,
        text: editText
      };
      await updateComment(commentId, data);
      toast.success('Comentário atualizado com sucesso!');
      setEditingComment(null);
      onCommentUpdated();
    } catch (error) {
      console.error('Erro ao atualizar comentário:', error);
      toast.error('Não foi possível atualizar o comentário. Por favor, tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteComment = async (commentId: number) => {
    if (!confirm('Tem certeza que deseja excluir este comentário?')) return;

    setLoading(true);
    try {
      await deleteComment(commentId);
      toast.success('Comentário excluído com sucesso!');
      onCommentDeleted();
    } catch (error) {
      console.error('Erro ao excluir comentário:', error);
      toast.error('Não foi possível excluir o comentário. Por favor, tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const renderComment = (comment: Comment, level = 0) => (
    <motion.div
      key={comment.id}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`mt-4 ${level > 0 ? 'ml-8' : ''}`}
    >
      <div className="bg-white rounded-lg shadow-sm p-4">
        <div className="flex justify-between items-start">
          <div>
            <h4 className="font-medium text-gray-900">{comment.name}</h4>
            <p className="mt-1 text-gray-600">{comment.text}</p>
            <p className="mt-2 text-sm text-gray-500">
              {new Date(comment.created_at).toLocaleDateString()}
            </p>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => {
                setReplyingTo(comment.id);
                setNewName('');
                setNewComment('');
              }}
              className="text-gray-500 hover:text-green-600"
            >
              <ArrowUturnLeftIcon className="h-5 w-5" />
            </button>
            <button
              onClick={() => {
                setEditingComment(comment.id);
                setEditText(comment.text);
                setEditName(comment.name);
              }}
              className="text-gray-500 hover:text-green-600"
            >
              <PencilIcon className="h-5 w-5" />
            </button>
            <button
              onClick={() => handleDeleteComment(comment.id)}
              className="text-gray-500 hover:text-red-600"
            >
              <TrashIcon className="h-5 w-5" />
            </button>
          </div>
        </div>

        {editingComment === comment.id && (
          <div className="mt-4">
            <input
              type="text"
              value={editName}
              onChange={(e) => setEditName(e.target.value)}
              placeholder="Seu nome"
              className="w-full mb-2 rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm"
            />
            <textarea
              value={editText}
              onChange={(e) => setEditText(e.target.value)}
              placeholder="Seu comentário"
              rows={3}
              className="w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm"
            />
            <div className="mt-2 flex justify-end space-x-2">
              <button
                onClick={() => setEditingComment(null)}
                className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
              >
                Cancelar
              </button>
              <button
                onClick={() => handleUpdateComment(comment.id)}
                disabled={loading}
                className="px-3 py-1 text-sm text-white bg-green-600 rounded hover:bg-green-700 disabled:opacity-50"
              >
                {loading ? 'Salvando...' : 'Salvar'}
              </button>
            </div>
          </div>
        )}

        {replyingTo === comment.id && (
          <div className="mt-4">
            <form onSubmit={handleSubmitComment} className="space-y-2">
              <input
                type="text"
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                placeholder="Seu nome"
                required
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm"
              />
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Seu comentário"
                required
                rows={3}
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm"
              />
              <div className="flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => setReplyingTo(null)}
                  className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="px-3 py-1 text-sm text-white bg-green-600 rounded hover:bg-green-700 disabled:opacity-50"
                >
                  {loading ? 'Enviando...' : 'Responder'}
                </button>
              </div>
            </form>
          </div>
        )}

        {comment.replies && comment.replies.length > 0 && (
          <div className="mt-4">
            {comment.replies.map((reply) => renderComment(reply, level + 1))}
          </div>
        )}
      </div>
    </motion.div>
  );

  return (
    <div className="mt-8">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Comentários</h3>
      
      <form onSubmit={handleSubmitComment} className="mb-8">
        <div className="space-y-4">
          <input
            type="text"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            placeholder="Seu nome"
            required
            className="w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm"
          />
          <textarea
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Adicione um comentário..."
            required
            rows={4}
            className="w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm"
          />
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={loading}
              className="inline-flex justify-center rounded-md border border-transparent bg-green-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Enviando...' : 'Comentar'}
            </button>
          </div>
        </div>
      </form>

      <div className="space-y-4">
        {comments.map((comment) => renderComment(comment))}
      </div>
    </div>
  );
} 