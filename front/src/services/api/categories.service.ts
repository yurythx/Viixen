import { API_BASE_URL, API_ENDPOINTS, getDefaultHeaders, handleApiError } from './config';
import { Category, PaginatedResponse } from '../../types/models';
import { getAccessToken } from './auth.service';

// Dados simulados para categorias
const MOCK_CATEGORIES: Category[] = [
  { id: 1, name: 'Tecnologia', slug: 'tecnologia', description: 'Artigos sobre tecnologia', created_at: new Date().toISOString() },
  { id: 2, name: 'Programação', slug: 'programacao', description: 'Artigos sobre programação', created_at: new Date().toISOString() },
  { id: 3, name: 'Design', slug: 'design', description: 'Artigos sobre design', created_at: new Date().toISOString() },
  { id: 4, name: 'Marketing', slug: 'marketing', description: 'Artigos sobre marketing', created_at: new Date().toISOString() },
  { id: 5, name: 'Negócios', slug: 'negocios', description: 'Artigos sobre negócios', created_at: new Date().toISOString() },
];

/**
 * Obtém a lista de categorias
 */
export const getCategories = async (): Promise<Category[]> => {
  try {
    // Tentar buscar da API primeiro
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.CATEGORIES.BASE}`, {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    // Se a API retornar erro, usar dados simulados
    if (!response.ok) {
      console.log('Usando dados simulados para categorias');
      return MOCK_CATEGORIES;
    }

    const data = await response.json();

    // Verificar se os dados retornados são uma resposta paginada
    if (data && typeof data === 'object' && 'results' in data) {
      return data.results;
    }

    // Verificar se os dados retornados são um array
    if (Array.isArray(data)) {
      return data;
    }

    console.error('API retornou um formato inválido para categorias:', data);
    return MOCK_CATEGORIES;
  } catch (error) {
    console.error('Erro ao buscar categorias:', error);
    return MOCK_CATEGORIES;
  }
};

/**
 * Obtém a lista de categorias com paginação
 */
export const getPaginatedCategories = async (page: number = 1): Promise<PaginatedResponse<Category>> => {
  try {
    // Tentar buscar da API primeiro
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.CATEGORIES.BASE}?page=${page}`, {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    // Se a API retornar erro, usar dados simulados
    if (!response.ok) {
      console.log('Usando dados simulados para categorias paginadas');
      return {
        count: MOCK_CATEGORIES.length,
        next: null,
        previous: null,
        results: MOCK_CATEGORIES
      };
    }

    const data = await response.json();

    // Verificar se os dados retornados são uma resposta paginada
    if (data && typeof data === 'object' && 'results' in data) {
      return data as PaginatedResponse<Category>;
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

    console.error('API retornou um formato inválido para categorias paginadas:', data);
    return {
      count: MOCK_CATEGORIES.length,
      next: null,
      previous: null,
      results: MOCK_CATEGORIES
    };
  } catch (error) {
    console.error('Erro ao buscar categorias paginadas:', error);
    return {
      count: MOCK_CATEGORIES.length,
      next: null,
      previous: null,
      results: MOCK_CATEGORIES
    };
  }
};

/**
 * Obtém uma categoria pelo slug
 */
export const getCategoryBySlug = async (slug: string): Promise<Category | null> => {
  try {
    // Tentar buscar da API primeiro
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.CATEGORIES.DETAIL(slug)}`, {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    // Se a API retornar erro, usar dados simulados
    if (!response.ok) {
      console.log(`Usando dados simulados para categoria com slug "${slug}"`);
      const mockCategory = MOCK_CATEGORIES.find(cat => cat.slug === slug);
      return mockCategory || null;
    }

    return response.json();
  } catch (error) {
    console.error(`Erro ao buscar categoria com slug "${slug}":`, error);
    // Tentar encontrar nos dados simulados
    const mockCategory = MOCK_CATEGORIES.find(cat => cat.slug === slug);
    return mockCategory || null;
  }
};

/**
 * Cria uma nova categoria
 */
export const createCategory = async (name: string): Promise<Category> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.CATEGORIES.BASE}`, {
      method: 'POST',
      headers: getDefaultHeaders(token),
      body: JSON.stringify({ name }),
    });

    await handleApiError(response);
    return response.json();
  } catch (error) {
    console.error('Erro ao criar categoria:', error);
    throw error;
  }
};

/**
 * Atualiza uma categoria existente
 */
export const updateCategory = async (slug: string, name: string): Promise<Category> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.CATEGORIES.DETAIL(slug)}`, {
      method: 'PATCH',
      headers: getDefaultHeaders(token),
      body: JSON.stringify({ name }),
    });

    await handleApiError(response);
    return response.json();
  } catch (error) {
    console.error(`Erro ao atualizar categoria ${slug}:`, error);
    throw error;
  }
};

/**
 * Exclui uma categoria
 */
export const deleteCategory = async (slug: string): Promise<void> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.CATEGORIES.DETAIL(slug)}`, {
      method: 'DELETE',
      headers: getDefaultHeaders(token),
    });

    await handleApiError(response);
    return;
  } catch (error) {
    console.error(`Erro ao excluir categoria ${slug}:`, error);
    throw error;
  }
};
