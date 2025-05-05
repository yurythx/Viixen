// app/articles/[slug]/page.tsx (detalhe + delete)
'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { use } from 'react';
import { Article, Comment, getArticle, deleteArticle, createComment, deleteComment, getArticleBySlug } from '@/services/articles';
import { motion } from 'framer-motion';
import { PencilIcon, TrashIcon, ChatBubbleLeftIcon } from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import Comments from '@/components/Comments';

export default function ArticlePage() {
  const params = useParams();
  const [article, setArticle] = useState<Article | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newComment, setNewComment] = useState({ name: '', text: '' });
  const [replyingTo, setReplyingTo] = useState<number | null>(null);
  const router = useRouter();

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

  const handleDelete = async () => {
    if (!confirm('Tem certeza que deseja excluir este artigo?')) {
      return;
    }

    try {
      await deleteArticle(params.slug as string);
      toast.success('Artigo excluído com sucesso!');
      router.push('/articles');
    } catch (error) {
      console.error('Erro ao excluir artigo:', error);
      toast.error('Não foi possível excluir o artigo. Por favor, tente novamente.');
    }
  };

  const handleCommentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const comment = await createComment(params.slug as string, {
        ...newComment,
        parent_id: replyingTo || undefined
      });
      
      if (article) {
        setArticle({
          ...article,
          comments: [...article.comments, comment],
          comments_count: article.comments_count + 1
        });
      }
      
      setNewComment({ name: '', text: '' });
      setReplyingTo(null);
      toast.success('Comentário adicionado com sucesso!');
    } catch (error) {
      console.error('Erro ao adicionar comentário:', error);
      toast.error('Não foi possível adicionar o comentário. Por favor, tente novamente.');
    }
  };

  const handleDeleteComment = async (commentId: number) => {
    if (!confirm('Tem certeza que deseja excluir este comentário?')) {
      return;
    }

    try {
      await deleteComment(commentId);
      if (article) {
        setArticle({
          ...article,
          comments: article.comments.filter(c => c.id !== commentId),
          comments_count: article.comments_count - 1
        });
      }
      toast.success('Comentário excluído com sucesso!');
    } catch (error) {
      console.error('Erro ao excluir comentário:', error);
      toast.error('Não foi possível excluir o comentário. Por favor, tente novamente.');
    }
  };

  const renderComment = (comment: Comment, level = 0) => (
    <div key={comment.id} className={`mt-4 ${level > 0 ? 'ml-8' : ''}`}>
      <div className="bg-gray-50 rounded-lg p-4">
        <div className="flex justify-between items-start">
          <div>
            <h4 className="text-sm font-medium text-gray-900">{comment.name}</h4>
            <p className="mt-1 text-sm text-gray-600">{comment.text}</p>
            <p className="mt-1 text-xs text-gray-500">
              {new Date(comment.created_at).toLocaleDateString()}
            </p>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => setReplyingTo(comment.id)}
              className="text-sm text-blue-600 hover:text-blue-800"
            >
              Responder
            </button>
            <button
              onClick={() => handleDeleteComment(comment.id)}
              className="text-sm text-red-600 hover:text-red-800"
            >
              Excluir
            </button>
          </div>
        </div>
        {replyingTo === comment.id && (
          <form onSubmit={handleCommentSubmit} className="mt-4">
            <input
              type="text"
              value={newComment.name}
              onChange={(e) => setNewComment(prev => ({ ...prev, name: e.target.value }))}
              placeholder="Seu nome"
              className="w-full mb-2 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              required
            />
            <textarea
              value={newComment.text}
              onChange={(e) => setNewComment(prev => ({ ...prev, text: e.target.value }))}
              placeholder="Seu comentário"
              className="w-full mb-2 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              rows={3}
              required
            />
            <div className="flex justify-end space-x-2">
              <button
                type="button"
                onClick={() => setReplyingTo(null)}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Cancelar
              </button>
              <button
                type="submit"
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Enviar
              </button>
            </div>
          </form>
        )}
      </div>
      {comment.replies && comment.replies.length > 0 && (
        <div className="mt-4">
          {comment.replies.map(reply => renderComment(reply, level + 1))}
        </div>
      )}
    </div>
  );

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

  const handleCommentAdded = async () => {
    try {
      const updatedArticle = await getArticleBySlug(article.slug);
      setArticle(updatedArticle);
    } catch (err) {
      console.error('Erro ao atualizar comentários:', err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.article
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
              className="text-3xl font-bold text-gray-900 mb-4"
            >
              {article.title}
            </motion.h1>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="text-sm text-gray-500 mb-8"
            >
              Publicado em {new Date(article.created_at).toLocaleDateString()}
            </motion.div>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="prose prose-green max-w-none"
              dangerouslySetInnerHTML={{ __html: article.content }}
            />
          </div>
        </motion.article>

        <Comments
          articleSlug={article.slug}
          comments={article.comments || []}
          onCommentAdded={handleCommentAdded}
          onCommentUpdated={handleCommentAdded}
          onCommentDeleted={handleCommentAdded}
        />
      </div>
    </div>
  );
}
