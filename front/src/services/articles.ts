import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface Comment {
  id: number;
  name: string;
  text: string;
  created_at: string;
  replies?: Comment[];
}

export interface Article {
  id: number;
  title: string;
  slug: string;
  content: string;
  created_at: string;
  comments?: Comment[];
  comments_count?: number;
}

export interface CreateArticleData {
  title: string;
  content: string;
}

export interface UpdateArticleData {
  title?: string;
  content?: string;
}

export interface CreateCommentData {
  name: string;
  text: string;
  article_slug: string;
  parent_id?: number;
}

export interface UpdateCommentData {
  name: string;
  text: string;
}

export async function getArticles(): Promise<Article[]> {
  const response = await axios.get(`${API_URL}/articles/`);
  return response.data;
}

export async function getArticleBySlug(slug: string): Promise<Article> {
  const response = await axios.get(`${API_URL}/articles/${slug}/`);
  return response.data;
}

export async function createArticle(data: CreateArticleData): Promise<Article> {
  const response = await axios.post(`${API_URL}/articles/`, data);
  return response.data;
}

export async function updateArticle(id: number, data: UpdateArticleData): Promise<Article> {
  const response = await axios.patch(`${API_URL}/articles/${id}/`, data);
  return response.data;
}

export async function deleteArticle(id: number): Promise<void> {
  await axios.delete(`${API_URL}/articles/${id}/`);
}

export async function createComment(data: CreateCommentData): Promise<Comment> {
  const response = await axios.post(`${API_URL}/articles/${data.article_slug}/comments/`, data);
  return response.data;
}

export async function updateComment(id: number, data: UpdateCommentData): Promise<Comment> {
  const response = await axios.patch(`${API_URL}/comments/${id}/`, data);
  return response.data;
}

export async function deleteComment(id: number): Promise<void> {
  await axios.delete(`${API_URL}/comments/${id}/`);
} 