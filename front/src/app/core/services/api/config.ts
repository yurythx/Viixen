/**
 * Configuração da API
 */

// URL base da API
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Endpoints da API
export const API_ENDPOINTS = {
  // Autenticação
  AUTH: {
    LOGIN: '/auth/jwt/create/',
    REFRESH: '/auth/jwt/refresh/',
    VERIFY: '/auth/jwt/verify/',
    REGISTER: '/auth/users/',
    CURRENT_USER: '/auth/users/me/',
  },

  // Usuários
  USERS: {
    BASE: '/accounts/users/',
    DETAIL: (slug: string) => `/accounts/users/${slug}/`,
    PASSWORD_CHANGE: '/accounts/users/change-password/',
    UPDATE_PROFILE: '/accounts/users/update-profile/',
  },

  // Artigos
  ARTICLES: {
    BASE: '/articles/articles/',
    DETAIL: (slug: string) => `/articles/articles/${slug}/`,
    COMMENTS: '/articles/comments/',
    ARTICLE_COMMENTS: (articleId: number) => `/articles/comments/?article=${articleId}`,
  },

  // Projetos
  PROJECTS: {
    // Quadros
    BOARDS: {
      BASE: '/projects/boards/',
      DETAIL: (id: number) => `/projects/boards/${id}/`,
    },
    // Tarefas
    TASKS: {
      BASE: '/projects/tasks/',
      DETAIL: (id: number) => `/projects/tasks/${id}/`,
      BY_BOARD: (boardId: number) => `/projects/tasks/?board=${boardId}`,
    },
    // Equipes
    TEAMS: {
      BASE: '/projects/teams/',
      DETAIL: (id: number) => `/projects/teams/${id}/`,
      MEMBERS: (teamId: number) => `/projects/teams/${teamId}/members/`,
    },
    // Comentários
    COMMENTS: {
      BASE: '/projects/comments/',
      DETAIL: (id: number) => `/projects/comments/${id}/`,
      BY_TASK: (taskId: number) => `/projects/comments/?task=${taskId}`,
    },
  },

  // Mangás (assumindo que você terá endpoints para mangás)
  MANGAS: {
    BASE: '/mangas/',
    DETAIL: (slug: string) => `/mangas/${slug}/`,
    CATEGORIES: '/mangas/categories/',
  },

  // Categorias de artigos
  CATEGORIES: {
    BASE: '/articles/categories/',
    DETAIL: (slug: string) => `/articles/categories/${slug}/`,
  }
};

// Configuração de headers padrão
export const getDefaultHeaders = (token?: string) => {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  return headers;
};

// Função para lidar com erros da API
export const handleApiError = async (response: Response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw {
      status: response.status,
      statusText: response.statusText,
      data: errorData,
    };
  }
  return response;
};
