/**
 * Serviço de usuários
 */
import { API_BASE_URL, API_ENDPOINTS, getDefaultHeaders, handleApiError } from './config';
import { PasswordChangeData, User, UserDetail } from '../../types/models';
import { getAccessToken } from './auth.service';

/**
 * Obtém a lista de usuários
 */
export const getUsers = async (): Promise<User[]> => {
  const token = getAccessToken();

  const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.USERS.BASE}`, {
    method: 'GET',
    headers: getDefaultHeaders(token || undefined),
  });

  await handleApiError(response);
  return response.json();
};

/**
 * Obtém um usuário pelo slug
 */
export const getUserBySlug = async (slug: string): Promise<UserDetail> => {
  const token = getAccessToken();

  const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.USERS.DETAIL(slug)}`, {
    method: 'GET',
    headers: getDefaultHeaders(token || undefined),
  });

  await handleApiError(response);
  return response.json();
};

/**
 * Atualiza os dados do usuário pelo slug
 */
export const updateUser = async (slug: string, data: Partial<User>): Promise<User> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  console.log('Atualizando usuário com slug:', slug);
  console.log('Dados para atualização:', data);

  // Para enviar arquivos, precisamos usar FormData
  const formData = new FormData();

  // Adicionar campos ao FormData
  Object.entries(data).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      formData.append(key, value);
      console.log(`Adicionando campo ao FormData: ${key}`);
    }
  });

  const url = `${API_BASE_URL}${API_ENDPOINTS.USERS.DETAIL(slug)}`;
  console.log('URL da requisição:', url);

  const response = await fetch(url, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${token}`,
      // Não definimos Content-Type aqui porque o FormData define automaticamente
    },
    body: formData,
  });

  console.log('Status da resposta:', response.status);

  await handleApiError(response);
  return response.json();
};

/**
 * Atualiza o perfil do usuário atual
 */
export const updateProfile = async (data: Partial<User>): Promise<User> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  console.log('Atualizando perfil do usuário atual');
  console.log('Dados para atualização:', data);

  // Para enviar arquivos, precisamos usar FormData
  const formData = new FormData();

  // Adicionar campos ao FormData
  Object.entries(data).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      formData.append(key, value);
      console.log(`Adicionando campo ao FormData: ${key}`);
    }
  });

  const url = `${API_BASE_URL}${API_ENDPOINTS.USERS.UPDATE_PROFILE}`;
  console.log('URL da requisição:', url);

  const response = await fetch(url, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      // Não definimos Content-Type aqui porque o FormData define automaticamente
    },
    body: formData,
  });

  console.log('Status da resposta:', response.status);

  await handleApiError(response);
  return response.json();
};

/**
 * Altera a senha do usuário
 */
export const changePassword = async (data: PasswordChangeData): Promise<void> => {
  const token = getAccessToken();

  if (!token) {
    throw new Error('Usuário não autenticado');
  }

  const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.USERS.PASSWORD_CHANGE}`, {
    method: 'POST',
    headers: getDefaultHeaders(token),
    body: JSON.stringify(data),
  });

  await handleApiError(response);
};
