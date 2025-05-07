/**
 * Interfaces para os modelos do backend
 */

// Usuário
export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  avatar: string | null;
  bio: string | null;
  position: string | null;
  slug: string;
  created_at: string;
  updated_at: string;
}

// Usuário detalhado
export interface UserDetail extends User {
  full_name: string;
  is_active: boolean;
  last_login: string | null;
}

// Dados para criação de usuário
export interface UserCreateData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name?: string;
  last_name?: string;
  avatar?: File | null;
  bio?: string;
  position?: string;
}

// Dados para alteração de senha
export interface PasswordChangeData {
  current_password: string;
  new_password: string;
  new_password_confirm: string;
}

// Comentário
export interface Comment {
  id: number;
  article: number;
  name: string;
  text: string;
  created_at: string;
  parent: number | null;
  replies?: Comment[];
}

// Dados para criação de comentário
export interface CommentCreateData {
  name: string;
  text: string;
  article: number;  // ID do artigo
  parent?: number | null;  // ID do comentário pai (para respostas)
}

// Dados para atualização de comentário
export interface CommentUpdateData {
  name?: string;
  text?: string;
}

// Categoria de artigo
export interface Category {
  id: number;
  name: string;
  slug: string;
}

// Artigo
export interface Article {
  id: number;
  title: string;
  slug: string;
  content: string;
  created_at: string;
  comments?: Comment[];
  comments_count?: number;
  author?: User;
  author_id?: string;
  category?: Category;
  category_id?: number;
}

// Dados para criação de artigo
export interface ArticleCreateData {
  title: string;
  content: string;
  category_id?: number;
}

// Dados para atualização de artigo
export interface ArticleUpdateData {
  title?: string;
  content?: string;
  category_id?: number;
}

// Tokens de autenticação
export interface AuthTokens {
  access: string;
  refresh: string;
}

// Resposta de login
export interface LoginResponse {
  tokens: AuthTokens;
  user: User;
}

// Dados de login
export interface LoginData {
  email: string;
  password: string;
}

// Resposta de erro da API
export interface ApiError {
  status: number;
  statusText: string;
  data: Record<string, any>;
}

// Resposta paginada da API
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
