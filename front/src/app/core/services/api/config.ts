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
    SETTINGS: '/accounts/users/settings/',
  },

  // Configurações
  SETTINGS: {
    BASE: '/accounts/settings/',
    MY_SETTINGS: '/accounts/settings/my_settings/',
  },

  // Artigos
  ARTICLES: {
    BASE: '/articles/articles/',
    DETAIL: (slug: string) => `/articles/articles/${slug}/`,
    COMMENTS: '/articles/comments/',
    ARTICLE_COMMENTS: (articleId: number) => `/articles/comments/?article=${articleId}`,
    // Endpoints do back-end
    INCREMENT_VIEWS: (slug: string) => `/articles/articles/${slug}/increment_views/`,
    FEATURED: '/articles/articles/?featured=true',
    POPULAR: '/articles/articles/?ordering=-views_count',
    RECENT: '/articles/articles/?ordering=-created_at',
    FAVORITE: (slug: string) => `/articles/articles/${slug}/favorite/`,
    MY_FAVORITES: '/articles/articles/favorites/',
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
    CHUNKED_UPLOAD: '/mangas/chunked-upload/',
  },

  // Categorias
  CATEGORIES: {
    BASE: '/categories/',
    DETAIL: (slug: string) => `/categories/${slug}/`,
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

// Tipos de erro da API
export interface ApiError {
  status: number;
  statusText: string;
  message: string;
  data: any;
  isApiError: boolean;
}

// Função para obter mensagem de erro amigável com base no status HTTP
export const getErrorMessage = (status: number, data: any): string => {
  switch (status) {
    case 400:
      // Tentar extrair mensagens de erro específicas dos campos
      if (data && typeof data === 'object') {
        const fieldErrors = Object.entries(data)
          .filter(([key, value]) => key !== 'detail' && Array.isArray(value))
          .map(([key, value]) => `${key}: ${(value as string[]).join(', ')}`)
          .join('; ');

        if (fieldErrors) {
          return `Dados inválidos: ${fieldErrors}`;
        }

        // Verificar se há uma mensagem de erro geral
        if (data.detail) {
          return data.detail;
        }
      }
      return 'Requisição inválida. Verifique os dados enviados.';

    case 401:
      return 'Autenticação necessária. Faça login para continuar.';

    case 403:
      return 'Você não tem permissão para realizar esta ação.';

    case 404:
      return 'O recurso solicitado não foi encontrado.';

    case 409:
      return 'Conflito ao processar a requisição. O recurso pode já existir.';

    case 422:
      return 'Não foi possível processar a requisição. Verifique os dados enviados.';

    case 429:
      return 'Muitas requisições. Tente novamente mais tarde.';

    case 500:
      return 'Erro interno do servidor. Tente novamente mais tarde.';

    case 503:
      return 'Serviço indisponível. Tente novamente mais tarde.';

    default:
      return 'Ocorreu um erro inesperado. Tente novamente mais tarde.';
  }
};

// Função para lidar com erros da API
export const handleApiError = async (response: Response) => {
  if (!response.ok) {
    let errorData = {};

    // Tentar obter dados de erro do corpo da resposta
    try {
      errorData = await response.json();
    } catch (e) {
      // Se não for possível obter JSON, usar um objeto vazio
      console.warn('Não foi possível obter detalhes do erro da API:', e);
    }

    // Criar objeto de erro padronizado
    const apiError: ApiError = {
      status: response.status,
      statusText: response.statusText,
      message: getErrorMessage(response.status, errorData),
      data: errorData,
      isApiError: true
    };

    // Registrar erro no console para depuração
    console.error('Erro na API:', apiError);

    throw apiError;
  }

  return response;
};
