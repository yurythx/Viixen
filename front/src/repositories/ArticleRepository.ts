/**
 * Repositório para artigos
 * Implementa o padrão de repositório para encapsular a lógica de acesso a dados de artigos
 */

import { API_BASE_URL, API_ENDPOINTS, getDefaultHeaders, handleApiError } from '../app/core/services/api/config';
import { getAccessToken } from '../app/core/services/api/auth.service';
import { Article, ArticleComment } from '../types/article.types';

/**
 * Repositório para artigos
 */
export class ArticleRepository {
  /**
   * Obtém todos os artigos
   */
  async getAll(): Promise<Article[]> {
    try {
      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.BASE}`, {
        method: 'GET',
        headers: getDefaultHeaders()
      });

      await handleApiError(response);
      const data = await response.json();
      return data.results || [];
    } catch (error) {
      console.error('Erro ao obter artigos:', error);
      throw error;
    }
  }

  /**
   * Obtém um artigo pelo slug
   */
  async getBySlug(slug: string): Promise<Article> {
    try {
      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.DETAIL(slug)}`, {
        method: 'GET',
        headers: getDefaultHeaders()
      });

      await handleApiError(response);
      return await response.json();
    } catch (error) {
      console.error(`Erro ao obter artigo com slug ${slug}:`, error);
      throw error;
    }
  }

  /**
   * Obtém artigos em destaque
   */
  async getFeatured(): Promise<Article[]> {
    try {
      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.FEATURED}`, {
        method: 'GET',
        headers: getDefaultHeaders()
      });

      await handleApiError(response);
      const data = await response.json();
      return data.results || [];
    } catch (error) {
      console.error('Erro ao obter artigos em destaque:', error);
      throw error;
    }
  }

  /**
   * Obtém artigos populares
   */
  async getPopular(): Promise<Article[]> {
    try {
      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.POPULAR}`, {
        method: 'GET',
        headers: getDefaultHeaders()
      });

      await handleApiError(response);
      const data = await response.json();
      return data.results || [];
    } catch (error) {
      console.error('Erro ao obter artigos populares:', error);
      throw error;
    }
  }

  /**
   * Obtém artigos recentes
   */
  async getRecent(): Promise<Article[]> {
    try {
      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.RECENT}`, {
        method: 'GET',
        headers: getDefaultHeaders()
      });

      await handleApiError(response);
      const data = await response.json();
      return data.results || [];
    } catch (error) {
      console.error('Erro ao obter artigos recentes:', error);
      throw error;
    }
  }

  /**
   * Incrementa o contador de visualizações de um artigo
   */
  async incrementViews(slug: string): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.INCREMENT_VIEWS(slug)}`, {
        method: 'POST',
        headers: getDefaultHeaders()
      });

      await handleApiError(response);
    } catch (error) {
      console.error(`Erro ao incrementar visualizações do artigo ${slug}:`, error);
      // Não lançar o erro para não interromper o fluxo
    }
  }

  /**
   * Obtém comentários de um artigo
   */
  async getComments(articleId: number): Promise<ArticleComment[]> {
    try {
      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.ARTICLE_COMMENTS(articleId)}`, {
        method: 'GET',
        headers: getDefaultHeaders()
      });

      await handleApiError(response);
      const data = await response.json();
      return data.results || [];
    } catch (error) {
      console.error(`Erro ao obter comentários do artigo ${articleId}:`, error);
      throw error;
    }
  }

  /**
   * Adiciona um comentário a um artigo
   */
  async addComment(articleId: number, comment: Partial<ArticleComment>): Promise<ArticleComment> {
    const token = getAccessToken();
    
    try {
      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.COMMENTS}`, {
        method: 'POST',
        headers: getDefaultHeaders(token),
        body: JSON.stringify({
          ...comment,
          article: articleId
        })
      });

      await handleApiError(response);
      return await response.json();
    } catch (error) {
      console.error(`Erro ao adicionar comentário ao artigo ${articleId}:`, error);
      throw error;
    }
  }

  /**
   * Favorita ou desfavorita um artigo
   */
  async toggleFavorite(slug: string): Promise<{ is_favorite: boolean }> {
    const token = getAccessToken();
    
    if (!token) {
      throw new Error('Usuário não autenticado');
    }
    
    try {
      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.FAVORITE(slug)}`, {
        method: 'POST',
        headers: getDefaultHeaders(token)
      });

      await handleApiError(response);
      return await response.json();
    } catch (error) {
      console.error(`Erro ao favoritar/desfavoritar artigo ${slug}:`, error);
      throw error;
    }
  }

  /**
   * Obtém artigos favoritados pelo usuário atual
   */
  async getFavorites(): Promise<Article[]> {
    const token = getAccessToken();
    
    if (!token) {
      throw new Error('Usuário não autenticado');
    }
    
    try {
      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.MY_FAVORITES}`, {
        method: 'GET',
        headers: getDefaultHeaders(token)
      });

      await handleApiError(response);
      const data = await response.json();
      return data.results || [];
    } catch (error) {
      console.error('Erro ao obter artigos favoritos:', error);
      throw error;
    }
  }
}

// Exportar uma instância única do repositório (Singleton)
export const articleRepository = new ArticleRepository();
