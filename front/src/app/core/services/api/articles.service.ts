/**
 * Serviço de artigos
 */
import { API_BASE_URL, API_ENDPOINTS, getDefaultHeaders, handleApiError } from './config';
import {
  Article,
  ArticleCreateData,
  ArticleUpdateData,
  Comment,
  CommentCreateData,
  CommentUpdateData,
  PaginatedResponse
} from '../../types/models';
import { getAccessToken } from './auth.service';

/**
 * Obtém a lista de artigos
 */
export const getArticles = async (): Promise<Article[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.BASE}`, {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    await handleApiError(response);
    const data = await response.json();

    // Verificar se os dados retornados são uma resposta paginada
    if (data && typeof data === 'object' && 'results' in data) {
      console.log('API retornou dados paginados:', data);
      return data.results;
    }

    // Verificar se os dados retornados são um array
    if (Array.isArray(data)) {
      return data;
    }

    console.error('API retornou um formato inválido para artigos:', data);
    return [];
  } catch (error) {
    console.error('Erro ao buscar artigos:', error);
    return [];
  }
};

/**
 * Obtém um artigo pelo slug
 */
export const getArticleBySlug = async (slug: string): Promise<Article | null> => {
  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.DETAIL(slug)}`, {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    await handleApiError(response);
    const data = await response.json();

    // Verificar se os dados retornados são válidos
    if (!data || typeof data !== 'object' || !data.id) {
      console.error('API retornou um formato inválido para o artigo:', data);
      return null;
    }

    return data;
  } catch (error) {
    console.error(`Erro ao buscar artigo com slug "${slug}":`, error);
    return null;
  }
};

/**
 * Cria um novo artigo
 */
export const createArticle = async (data: ArticleCreateData): Promise<Article> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.BASE}`, {
      method: 'POST',
      headers: getDefaultHeaders(token),
      body: JSON.stringify(data),
    });

    await handleApiError(response);
    return response.json();
  } catch (error) {
    console.error('Erro ao criar artigo:', error);
    throw error;
  }
};

/**
 * Atualiza um artigo existente
 */
export const updateArticle = async (slug: string, data: ArticleUpdateData): Promise<Article> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.DETAIL(slug)}`, {
      method: 'PATCH',
      headers: getDefaultHeaders(token),
      body: JSON.stringify(data),
    });

    await handleApiError(response);
    return response.json();
  } catch (error) {
    console.error(`Erro ao atualizar artigo ${slug}:`, error);
    throw error;
  }
};

/**
 * Exclui um artigo
 */
export const deleteArticle = async (slug: string): Promise<void> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.DETAIL(slug)}`, {
      method: 'DELETE',
      headers: getDefaultHeaders(token),
    });

    await handleApiError(response);
    return;
  } catch (error) {
    console.error(`Erro ao excluir artigo ${slug}:`, error);
    throw error;
  }
};

/**
 * Obtém a lista de artigos com paginação
 */
export const getPaginatedArticles = async (page: number = 1): Promise<PaginatedResponse<Article>> => {
  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.BASE}?page=${page}`, {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    await handleApiError(response);
    const data = await response.json();

    // Verificar se os dados retornados são uma resposta paginada
    if (data && typeof data === 'object' && 'results' in data) {
      return data as PaginatedResponse<Article>;
    }

    // Se não for uma resposta paginada, criar uma estrutura paginada com os dados
    if (Array.isArray(data)) {
      return {
        count: data.length,
        next: null,
        previous: null,
        results: data
      };
    }

    console.error('API retornou um formato inválido para artigos paginados:', data);
    return {
      count: 0,
      next: null,
      previous: null,
      results: []
    };
  } catch (error) {
    console.error('Erro ao buscar artigos paginados:', error);
    return {
      count: 0,
      next: null,
      previous: null,
      results: []
    };
  }
};

/**
 * Obtém os comentários de um artigo
 */
export const getArticleComments = async (articleId: number): Promise<Comment[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.ARTICLE_COMMENTS(articleId)}`, {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    await handleApiError(response);
    const data = await response.json();

    // Verificar se os dados retornados são uma resposta paginada
    if (data && typeof data === 'object' && 'results' in data) {
      return data.results;
    }

    // Verificar se os dados retornados são um array
    if (Array.isArray(data)) {
      return data;
    }

    console.error('API retornou um formato inválido para comentários:', data);
    return [];
  } catch (error) {
    console.error(`Erro ao buscar comentários do artigo ${articleId}:`, error);
    return [];
  }
};

/**
 * Cria um novo comentário
 */
export const createComment = async (data: CommentCreateData): Promise<Comment> => {
  const token = getAccessToken();

  const headers = token
    ? getDefaultHeaders(token)
    : getDefaultHeaders();

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.COMMENTS}`, {
      method: 'POST',
      headers,
      body: JSON.stringify(data),
    });

    await handleApiError(response);
    return response.json();
  } catch (error) {
    console.error('Erro ao criar comentário:', error);
    throw error;
  }
};

/**
 * Atualiza um comentário existente
 */
export const updateComment = async (commentId: number, data: CommentUpdateData): Promise<Comment> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.COMMENTS}/${commentId}/`, {
      method: 'PATCH',
      headers: getDefaultHeaders(token),
      body: JSON.stringify(data),
    });

    await handleApiError(response);
    return response.json();
  } catch (error) {
    console.error(`Erro ao atualizar comentário ${commentId}:`, error);
    throw error;
  }
};

/**
 * Exclui um comentário
 */
export const deleteComment = async (commentId: number): Promise<void> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.ARTICLES.COMMENTS}/${commentId}/`, {
      method: 'DELETE',
      headers: getDefaultHeaders(token),
    });

    await handleApiError(response);
    return;
  } catch (error) {
    console.error(`Erro ao excluir comentário ${commentId}:`, error);
    throw error;
  }
};
