import React from 'react';
import { render, screen } from '@testing-library/react';
import ArticleCard from '../ArticleCard';
import '@testing-library/jest-dom';

// Mock do next/link
jest.mock('next/link', () => {
  return ({ children, href }: { children: React.ReactNode; href: string }) => {
    return <a href={href}>{children}</a>;
  };
});

describe('ArticleCard', () => {
  const mockArticle = {
    id: 1,
    title: 'Test Article',
    slug: 'test-article',
    content: '<p>This is a test article content</p>',
    created_at: '2023-01-01T00:00:00Z',
    comments_count: 5,
    category: {
      id: 1,
      name: 'Test Category',
      slug: 'test-category'
    }
  };

  it('renders article title correctly', () => {
    render(<ArticleCard article={mockArticle} />);
    expect(screen.getByText('Test Article')).toBeInTheDocument();
  });

  it('renders article excerpt correctly', () => {
    render(<ArticleCard article={mockArticle} />);
    expect(screen.getByText('This is a test article content')).toBeInTheDocument();
  });

  it('renders article category correctly', () => {
    render(<ArticleCard article={mockArticle} />);
    expect(screen.getByText('Test Category')).toBeInTheDocument();
  });

  it('renders article comments count correctly', () => {
    render(<ArticleCard article={mockArticle} />);
    expect(screen.getByText('5')).toBeInTheDocument();
  });

  it('links to the correct article page', () => {
    render(<ArticleCard article={mockArticle} />);
    const link = screen.getByRole('link');
    expect(link).toHaveAttribute('href', '/artigos/test-article');
  });

  it('formats the date correctly', () => {
    render(<ArticleCard article={mockArticle} />);
    // Verificar se a data formatada está presente
    // O formato exato pode variar dependendo da localização
    expect(screen.getByText(/1 de janeiro de 2023/i)).toBeInTheDocument();
  });

  it('handles articles without category', () => {
    const articleWithoutCategory = { ...mockArticle, category: undefined };
    render(<ArticleCard article={articleWithoutCategory} />);
    // Não deve quebrar e ainda deve renderizar o título
    expect(screen.getByText('Test Article')).toBeInTheDocument();
  });

  it('handles articles without comments count', () => {
    const articleWithoutComments = { ...mockArticle, comments_count: undefined };
    render(<ArticleCard article={articleWithoutComments} />);
    // Deve mostrar 0 como valor padrão
    expect(screen.getByText('0')).toBeInTheDocument();
  });
});
