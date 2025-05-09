/**
 * Serviço de mangás
 */
import { API_BASE_URL, API_ENDPOINTS, getDefaultHeaders, handleApiError } from './config';
import { getAccessToken } from './auth.service';

// Interfaces para os modelos de mangá
export interface Manga {
  id: number;
  title: string;
  slug: string;
  description: string;
  cover: string | null;
  chapters: Chapter[];
  created_at: string;
}

export interface Chapter {
  id: number;
  title: string;
  number: number;
  chapter_type: 'images' | 'pdf';
  chapter_type_display: string;
  pdf_file?: string;
  pages: Page[];
  created_at: string;
}

export interface Page {
  id: number;
  image: string;
  page_number: number;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface MangaCreateData {
  title: string;
  description: string;
  cover?: File | null;
}

export interface ChapterCreateData {
  title: string;
  number: number;
  manga: number; // ID do mangá
  chapter_type: 'images' | 'pdf';
  pdf_file?: File;
  pdf_file_path?: string; // Caminho para o arquivo PDF quando enviado em partes
}

export interface PageCreateData {
  image: File;
  page_number: number;
  chapter: number; // ID do capítulo
}

/**
 * Obtém a lista de mangás
 */
export const getMangas = async (): Promise<Manga[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}mangas/`, {
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

    console.error('API retornou um formato inválido para mangás:', data);
    return [];
  } catch (error) {
    console.error('Erro ao buscar mangás:', error);
    return [];
  }
};

/**
 * Obtém um mangá pelo slug
 */
export const getMangaBySlug = async (slug: string): Promise<Manga | null> => {
  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}mangas/${slug}/`, {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    await handleApiError(response);
    const data = await response.json();

    // Verificar se os dados retornados são válidos
    if (!data || typeof data !== 'object' || !data.id) {
      console.error('API retornou um formato inválido para o mangá:', data);
      return null;
    }

    return data;
  } catch (error) {
    console.error(`Erro ao buscar mangá com slug "${slug}":`, error);
    return null;
  }
};

/**
 * Obtém a lista de mangás com paginação e pesquisa
 */
export const getPaginatedMangas = async (page: number = 1, searchTerm: string = ''): Promise<PaginatedResponse<Manga>> => {
  try {
    // Construir a URL com parâmetros de consulta
    let url = `${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}mangas/?page=${page}`;

    // Adicionar termo de pesquisa se fornecido
    if (searchTerm) {
      url += `&search=${encodeURIComponent(searchTerm)}`;
    }

    const response = await fetch(url, {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    await handleApiError(response);
    const data = await response.json();

    // Verificar se os dados retornados são uma resposta paginada
    if (data && typeof data === 'object' && 'results' in data) {
      return data as PaginatedResponse<Manga>;
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

    console.error('API retornou um formato inválido para mangás paginados:', data);
    return {
      count: 0,
      next: null,
      previous: null,
      results: []
    };
  } catch (error) {
    console.error('Erro ao buscar mangás paginados:', error);
    return {
      count: 0,
      next: null,
      previous: null,
      results: []
    };
  }
};

/**
 * Cria um novo mangá
 */
export const createManga = async (data: MangaCreateData): Promise<Manga> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  // Criar FormData para envio de arquivos
  const formData = new FormData();
  formData.append('title', data.title);
  formData.append('description', data.description);

  if (data.cover) {
    formData.append('cover', data.cover);
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}mangas/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData,
    });

    await handleApiError(response);
    return response.json();
  } catch (error) {
    console.error('Erro ao criar mangá:', error);
    throw error;
  }
};

/**
 * Atualiza um mangá existente
 */
export const updateManga = async (slug: string, data: Partial<MangaCreateData>): Promise<Manga> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  // Criar FormData para envio de arquivos
  const formData = new FormData();

  if (data.title) {
    formData.append('title', data.title);
  }

  if (data.description) {
    formData.append('description', data.description);
  }

  if (data.cover) {
    formData.append('cover', data.cover);
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}mangas/${slug}/`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData,
    });

    await handleApiError(response);
    return response.json();
  } catch (error) {
    console.error(`Erro ao atualizar mangá ${slug}:`, error);
    throw error;
  }
};

/**
 * Exclui um mangá
 */
export const deleteManga = async (slug: string): Promise<void> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}mangas/${slug}/`, {
      method: 'DELETE',
      headers: getDefaultHeaders(token),
    });

    await handleApiError(response);
    return;
  } catch (error) {
    console.error(`Erro ao excluir mangá ${slug}:`, error);
    throw error;
  }
};

/**
 * Obtém os capítulos de um mangá
 */
export const getChaptersByManga = async (mangaSlug: string): Promise<Chapter[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}chapters/?manga_slug=${mangaSlug}`, {
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

    console.error('API retornou um formato inválido para capítulos:', data);
    return [];
  } catch (error) {
    console.error(`Erro ao buscar capítulos do mangá ${mangaSlug}:`, error);
    return [];
  }
};

/**
 * Obtém um capítulo pelo ID
 */
export const getChapterById = async (chapterId: number): Promise<Chapter | null> => {
  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}chapters/${chapterId}/`, {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    await handleApiError(response);
    return response.json();
  } catch (error) {
    console.error(`Erro ao buscar capítulo ${chapterId}:`, error);
    return null;
  }
};

/**
 * Cria um novo capítulo
 */
export const createChapter = async (data: ChapterCreateData): Promise<Chapter> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  try {
    // Usar FormData em vez de JSON para manter consistência com outras chamadas
    const formData = new FormData();
    formData.append('title', data.title);
    formData.append('number', data.number.toString());
    formData.append('manga', data.manga.toString());
    formData.append('chapter_type', data.chapter_type);

    // Adicionar arquivo PDF ou caminho do arquivo se for um capítulo do tipo PDF
    if (data.chapter_type === 'pdf') {
      if (data.pdf_file) {
        console.log('Adicionando PDF ao FormData:', data.pdf_file.name, data.pdf_file.size);

        // Verificar o tamanho do arquivo PDF antes de enviar
        const maxSizeMB = 100;
        const maxSizeBytes = maxSizeMB * 1024 * 1024;

        if (data.pdf_file.size > maxSizeBytes) {
          throw {
            status: 413,
            statusText: 'Arquivo muito grande',
            message: `O arquivo PDF excede o tamanho máximo de ${maxSizeMB}MB.`,
            isApiError: true
          };
        }

        formData.append('pdf_file', data.pdf_file);
      } else if (data.pdf_file_path) {
        console.log('Adicionando caminho do PDF ao FormData:', data.pdf_file_path);
        // Garantir que o caminho use barras normais (/) em vez de barras invertidas (\)
        const normalizedPath = data.pdf_file_path.replace(/\\/g, '/');
        console.log('Caminho normalizado:', normalizedPath);
        formData.append('pdf_file_path', normalizedPath);
      }
      // Temporariamente desativando a validação para permitir capítulos PDF sem arquivo
      // Isso permite criar o capítulo primeiro e adicionar o arquivo depois
      /*
      else {
        console.error('Erro: Tipo de capítulo é PDF, mas nenhum arquivo ou caminho foi fornecido');
        throw {
          status: 400,
          statusText: 'Arquivo não fornecido',
          message: 'É necessário fornecer um arquivo PDF ou um caminho para o arquivo PDF.',
          isApiError: true
        };
      }
      */
    }

    try {
      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}chapters/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData,
      });

      await handleApiError(response);
      return response.json();
    } catch (error) {
      // Verificar se é um erro de tamanho de arquivo
      if (error && typeof error === 'object' && 'status' in error && error.status === 413) {
        throw {
          status: 413,
          statusText: 'Arquivo muito grande',
          message: 'O arquivo PDF excede o tamanho máximo permitido pelo servidor.',
          isApiError: true
        };
      }
      throw error;
    }
  } catch (error) {
    console.error('Erro ao criar capítulo:', error);
    // Mostrar mensagem de erro mais amigável
    if (error && typeof error === 'object' && 'isApiError' in error) {
      throw error;
    } else {
      throw {
        status: 500,
        statusText: 'Erro Interno',
        message: 'Não foi possível criar o capítulo. Tente novamente mais tarde.',
        data: error,
        isApiError: true
      };
    }
  }
};

/**
 * Obtém as páginas de um capítulo
 */
export const getPagesByChapter = async (chapterId: number): Promise<Page[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}pages/?chapter=${chapterId}`, {
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

    console.error('API retornou um formato inválido para páginas:', data);
    return [];
  } catch (error) {
    console.error(`Erro ao buscar páginas do capítulo ${chapterId}:`, error);
    return [];
  }
};

/**
 * Faz upload de um arquivo PDF em partes
 */
export const uploadPdfInChunks = async (
  file: File,
  onProgress?: (progress: number) => void
): Promise<{ filePath: string; fileUrl: string; fileName: string }> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  try {
    // Tamanho de cada parte (5MB)
    const chunkSize = 5 * 1024 * 1024;
    const totalChunks = Math.ceil(file.size / chunkSize);
    let uploadedChunks = 0;

    // Criar um identificador único para este upload
    const uploadId = Date.now().toString();

    for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
      const start = chunkIndex * chunkSize;
      const end = Math.min(start + chunkSize, file.size);
      const chunk = file.slice(start, end);

      const formData = new FormData();
      formData.append('file', chunk);
      formData.append('fileName', file.name);
      formData.append('uploadId', uploadId);
      formData.append('chunkIndex', chunkIndex.toString());
      formData.append('totalChunks', totalChunks.toString());

      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.CHUNKED_UPLOAD}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      await handleApiError(response);
      const result = await response.json();

      uploadedChunks++;
      const progress = Math.round((uploadedChunks / totalChunks) * 100);

      if (onProgress) {
        onProgress(progress);
      }

      // Se for a última parte, retornar as informações do arquivo
      if (chunkIndex === totalChunks - 1 && result.fileUrl) {
        // Normalizar o caminho do arquivo (substituir barras invertidas por barras normais)
        const normalizedPath = result.filePath.replace(/\\/g, '/');
        return {
          filePath: normalizedPath,
          fileUrl: result.fileUrl,
          fileName: result.fileName
        };
      }
    }

    throw new Error('Não foi possível obter as informações do arquivo após o upload');
  } catch (error) {
    console.error('Erro ao fazer upload do PDF em partes:', error);

    if (error && typeof error === 'object' && 'isApiError' in error) {
      throw error;
    } else {
      throw {
        status: 500,
        statusText: 'Erro Interno',
        message: 'Não foi possível fazer upload do arquivo PDF. Tente novamente mais tarde.',
        data: error,
        isApiError: true
      };
    }
  }
};

/**
 * Cria uma nova página
 */
export const createPage = async (data: PageCreateData): Promise<Page> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  // Criar FormData para envio de arquivos
  const formData = new FormData();
  formData.append('image', data.image);
  formData.append('page_number', data.page_number.toString());
  formData.append('chapter', data.chapter.toString());

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}pages/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData,
    });

    await handleApiError(response);
    return response.json();
  } catch (error) {
    console.error('Erro ao criar página:', error);
    // Mostrar mensagem de erro mais amigável
    if (error && typeof error === 'object' && 'isApiError' in error) {
      throw error;
    } else {
      throw {
        status: 500,
        statusText: 'Erro Interno',
        message: 'Não foi possível criar a página. Tente novamente mais tarde.',
        data: error,
        isApiError: true
      };
    }
  }
};

/**
 * Adiciona ou remove um mangá dos favoritos
 */
export const toggleFavorite = async (slug: string): Promise<{ status: string }> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}mangas/${slug}/favorite/`, {
      method: 'POST',
      headers: getDefaultHeaders(token),
    });

    await handleApiError(response);
    return response.json();
  } catch (error) {
    console.error(`Erro ao favoritar/desfavoritar mangá ${slug}:`, error);
    throw error;
  }
};

/**
 * Obtém a lista de mangás favoritos do usuário
 */
export const getMyFavorites = async (): Promise<Manga[]> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}mangas/my_favorites/`, {
      method: 'GET',
      headers: getDefaultHeaders(token),
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

    console.error('API retornou um formato inválido para mangás favoritos:', data);
    return [];
  } catch (error) {
    console.error('Erro ao buscar mangás favoritos:', error);
    return [];
  }
};

/**
 * Atualiza o progresso de leitura de um mangá
 */
export const updateReadingProgress = async (
  slug: string,
  chapterId: number,
  pageId?: number
): Promise<any> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  const data: { chapter: number; page?: number } = {
    chapter: chapterId
  };

  if (pageId) {
    data.page = pageId;
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}mangas/${slug}/update_progress/`, {
      method: 'POST',
      headers: getDefaultHeaders(token),
      body: JSON.stringify(data),
    });

    await handleApiError(response);
    return response.json();
  } catch (error) {
    console.error(`Erro ao atualizar progresso de leitura do mangá ${slug}:`, error);
    throw error;
  }
};

/**
 * Adiciona um comentário a um capítulo
 */
export const addComment = async (chapterId: number, content: string): Promise<any> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}chapters/${chapterId}/comment/`, {
      method: 'POST',
      headers: getDefaultHeaders(token),
      body: JSON.stringify({ content }),
    });

    await handleApiError(response);
    return response.json();
  } catch (error) {
    console.error(`Erro ao adicionar comentário ao capítulo ${chapterId}:`, error);
    throw error;
  }
};

/**
 * Obtém os comentários de um capítulo
 */
export const getComments = async (chapterId: number): Promise<any[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}chapters/${chapterId}/comments/`, {
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
    console.error(`Erro ao buscar comentários do capítulo ${chapterId}:`, error);
    return [];
  }
};

/**
 * Registra uma visualização de mangá
 */
export const recordMangaView = async (mangaId: number): Promise<any> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}history/record_view/`, {
      method: 'POST',
      headers: getDefaultHeaders(token),
      body: JSON.stringify({ manga: mangaId }),
    });

    await handleApiError(response);
    return response.json();
  } catch (error) {
    console.error(`Erro ao registrar visualização do mangá ${mangaId}:`, error);
    throw error;
  }
};

/**
 * Obtém o histórico de visualizações do usuário
 */
export const getViewHistory = async (): Promise<any[]> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}history/my_history/`, {
      method: 'GET',
      headers: getDefaultHeaders(token),
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

    console.error('API retornou um formato inválido para histórico de visualizações:', data);
    return [];
  } catch (error) {
    console.error('Erro ao buscar histórico de visualizações:', error);
    return [];
  }
};

/**
 * Obtém recomendações de mangás para o usuário
 */
export const getRecommendations = async (): Promise<Manga[]> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}history/recommendations/`, {
      method: 'GET',
      headers: getDefaultHeaders(token),
    });

    await handleApiError(response);
    return response.json();
  } catch (error) {
    console.error('Erro ao buscar recomendações:', error);
    return [];
  }
};

/**
 * Obtém estatísticas do usuário
 */
export const getUserStatistics = async (): Promise<any> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}statistics/my_statistics/`, {
      method: 'GET',
      headers: getDefaultHeaders(token),
    });

    await handleApiError(response);
    return response.json();
  } catch (error) {
    console.error('Erro ao buscar estatísticas do usuário:', error);
    throw error;
  }
};

/**
 * Obtém o ranking de leitores
 */
export const getLeaderboard = async (): Promise<any[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.MANGAS.BASE}statistics/leaderboard/`, {
      method: 'GET',
      headers: getDefaultHeaders(),
    });

    await handleApiError(response);
    return response.json();
  } catch (error) {
    console.error('Erro ao buscar ranking de leitores:', error);
    return [];
  }
};

// Exportar o serviço completo
const mangasService = {
  getMangas,
  getMangaBySlug,
  getPaginatedMangas,
  createManga,
  updateManga,
  deleteManga,
  getChaptersByManga,
  getChapterById,
  createChapter,
  getPagesByChapter,
  createPage,
  toggleFavorite,
  getMyFavorites,
  updateReadingProgress,
  addComment,
  getComments,
  recordMangaView,
  getViewHistory,
  getRecommendations,
  getUserStatistics,
  getLeaderboard
};

export default mangasService;
