"""
Testes de integração para o fluxo de artigos
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.articles.models import Article, Comment, Tag
from apps.categories.models import Category
import json

User = get_user_model()

class ArticleFlowTestCase(TestCase):
    """
    Testes de integração para o fluxo de artigos
    """
    def setUp(self):
        """
        Configuração inicial para os testes
        """
        self.client = Client()

        # Criar um usuário para os testes
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        # Criar um usuário admin para os testes
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )

        # Criar uma categoria para os testes
        self.category = Category.objects.create(
            name='Categoria de Teste',
            description='Descrição da categoria de teste'
        )

        # Criar algumas tags para os testes
        self.tag1 = Tag.objects.create(name='Tag 1')
        self.tag2 = Tag.objects.create(name='Tag 2')

        # Criar alguns artigos para os testes
        self.article1 = Article.objects.create(
            title='Artigo 1',
            content='Conteúdo do artigo 1',
            featured=True,
            author=self.user,
            category=self.category
        )
        self.article1.tags.add(self.tag1)

        self.article2 = Article.objects.create(
            title='Artigo 2',
            content='Conteúdo do artigo 2',
            featured=False,
            author=self.user,
            category=self.category
        )
        self.article2.tags.add(self.tag2)

        # Criar alguns comentários para os testes
        self.comment1 = Comment.objects.create(
            article=self.article1,
            name='Usuário 1',
            text='Comentário 1',
            is_approved=True
        )

        self.comment2 = Comment.objects.create(
            article=self.article1,
            name='Usuário 2',
            text='Comentário 2',
            is_approved=False
        )

    def test_list_articles(self):
        """
        Testa a listagem de artigos
        """
        url = reverse('article-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['count'], 2)

    def test_get_article_detail(self):
        """
        Testa a obtenção de detalhes de um artigo
        """
        url = reverse('article-detail', kwargs={'slug': self.article1.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Artigo 1')
        self.assertEqual(data['content'], 'Conteúdo do artigo 1')
        self.assertTrue(data['featured'])

    def test_create_article(self):
        """
        Testa a criação de um artigo
        """
        # Fazer login como usuário
        self.client.login(username='testuser', password='testpassword')

        url = reverse('article-list')
        data = {
            'title': 'Novo Artigo',
            'content': 'Conteúdo do novo artigo',
            'featured': False,
            'category': self.category.id,
            'tags': [self.tag1.id, self.tag2.id]
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Novo Artigo')
        self.assertEqual(data['content'], 'Conteúdo do novo artigo')
        self.assertFalse(data['featured'])

        # Verificar se o artigo foi realmente criado no banco de dados
        self.assertTrue(Article.objects.filter(title='Novo Artigo').exists())

    def test_update_article(self):
        """
        Testa a atualização de um artigo
        """
        # Fazer login como usuário
        self.client.login(username='testuser', password='testpassword')

        url = reverse('article-detail', kwargs={'slug': self.article1.slug})
        data = {
            'title': 'Artigo 1 Atualizado',
            'content': 'Conteúdo atualizado',
            'featured': False
        }
        response = self.client.patch(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Artigo 1 Atualizado')
        self.assertEqual(data['content'], 'Conteúdo atualizado')
        self.assertFalse(data['featured'])

        # Verificar se o artigo foi realmente atualizado no banco de dados
        article = Article.objects.get(id=self.article1.id)
        self.assertEqual(article.title, 'Artigo 1 Atualizado')
        self.assertEqual(article.content, 'Conteúdo atualizado')
        self.assertFalse(article.featured)

    def test_delete_article(self):
        """
        Testa a exclusão de um artigo
        """
        # Fazer login como usuário
        self.client.login(username='testuser', password='testpassword')

        url = reverse('article-detail', kwargs={'slug': self.article1.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        # Verificar se o artigo foi realmente excluído do banco de dados
        self.assertFalse(Article.objects.filter(id=self.article1.id).exists())

    def test_increment_views(self):
        """
        Testa o incremento de visualizações de um artigo
        """
        # Verificar contagem inicial de visualizações
        self.assertEqual(self.article1.views_count, 0)

        url = reverse('article-increment-views', kwargs={'slug': self.article1.slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['views_count'], 1)

        # Verificar se a contagem de visualizações foi incrementada no banco de dados
        article = Article.objects.get(id=self.article1.id)
        self.assertEqual(article.views_count, 1)

    def test_favorite_article(self):
        """
        Testa a funcionalidade de favoritar um artigo
        """
        # Fazer login como usuário
        self.client.login(username='testuser', password='testpassword')

        # Verificar que o artigo não está nos favoritos do usuário
        self.assertFalse(self.article1.favorites.filter(id=self.user.id).exists())

        url = reverse('article-favorite', kwargs={'slug': self.article1.slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'added to favorites')
        self.assertTrue(data['is_favorite'])

        # Verificar que o artigo está nos favoritos do usuário
        self.assertTrue(self.article1.favorites.filter(id=self.user.id).exists())

        # Desfavoritar o artigo
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'removed from favorites')
        self.assertFalse(data['is_favorite'])

        # Verificar que o artigo não está mais nos favoritos do usuário
        self.assertFalse(self.article1.favorites.filter(id=self.user.id).exists())

    def test_list_comments(self):
        """
        Testa a listagem de comentários de um artigo
        """
        url = reverse('article-comments', kwargs={'slug': self.article1.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)  # Apenas o comentário aprovado deve ser retornado
        self.assertEqual(data[0]['text'], 'Comentário 1')

    def test_create_comment(self):
        """
        Testa a criação de um comentário
        """
        url = reverse('comment-list')
        data = {
            'article': self.article1.id,
            'name': 'Usuário Teste',
            'email': 'usuario@teste.com',
            'text': 'Novo comentário'
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['text'], 'Novo comentário')
        self.assertEqual(data['name'], 'Usuário Teste')
        self.assertEqual(data['email'], 'usuario@teste.com')

        # Verificar se o comentário foi realmente criado no banco de dados
        self.assertTrue(Comment.objects.filter(text='Novo comentário').exists())

    def test_approve_comment(self):
        """
        Testa a aprovação de um comentário
        """
        # Fazer login como admin
        self.client.login(username='admin', password='adminpassword')

        # Verificar estado inicial
        self.assertFalse(self.comment2.is_approved)

        url = reverse('comment-approve', kwargs={'pk': self.comment2.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'approved')

        # Verificar se o comentário foi aprovado no banco de dados
        comment = Comment.objects.get(id=self.comment2.id)
        self.assertTrue(comment.is_approved)

    def test_reject_comment(self):
        """
        Testa a rejeição de um comentário
        """
        # Fazer login como admin
        self.client.login(username='admin', password='adminpassword')

        # Verificar estado inicial
        self.assertTrue(self.comment1.is_approved)

        url = reverse('comment-reject', kwargs={'pk': self.comment1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'rejected')

        # Verificar se o comentário foi rejeitado no banco de dados
        comment = Comment.objects.get(id=self.comment1.id)
        self.assertFalse(comment.is_approved)
