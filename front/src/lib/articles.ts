// src/lib/articles.ts
import { api } from './api';

interface Article {
  slug: string;
  title: string;
  content: string;
}

export const fetchArticles = async (): Promise<Article[]> => (await api.get('/v1/articles/api/')).data;

export const fetchArticle = async (slug: string): Promise<Article> =>
  (await api.get(`/v1/articles/api/${slug}/`)).data;

export const createArticle = async (data: Omit<Article, 'slug'>): Promise<Article> =>
  (await api.post('/v1/articles/api/', data)).data;

export const updateArticle = async (slug: string, data: Omit<Article, 'slug'>): Promise<Article> =>
  (await api.put(`/v1/articles/api/${slug}/`, data)).data;

export const deleteArticle = async (slug: string): Promise<void> =>
  (await api.delete(`/v1/articles/api/${slug}/`)).data;