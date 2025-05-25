from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Article, Category
from .forms import ArticleForm

User = get_user_model()


class ArticleModelTestCase(TestCase):
    """Testes para o modelo Article"""

    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_active=True
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

    def test_create_article(self):
        """Testa criação de artigo"""
        article = Article.objects.create(
            title='Test Article',
            content='This is a test article content.',
            author=self.user,
            category=self.category,
            status='published'
        )
        self.assertEqual(article.title, 'Test Article')
        self.assertEqual(article.author, self.user)
        self.assertEqual(article.category, self.category)
        self.assertEqual(article.status, 'published')

    def test_article_slug_generation(self):
        """Testa geração automática de slug"""
        article = Article.objects.create(
            title='Test Article With Spaces',
            content='Content',
            author=self.user,
            category=self.category
        )
        self.assertEqual(article.slug, 'test-article-with-spaces')

    def test_article_str_method(self):
        """Testa método __str__ do artigo"""
        article = Article.objects.create(
            title='Test Article',
            content='Content',
            author=self.user,
            category=self.category
        )
        self.assertEqual(str(article), 'Test Article')


class CategoryModelTestCase(TestCase):
    """Testes para o modelo Category"""

    def test_create_category(self):
        """Testa criação de categoria"""
        category = Category.objects.create(
            name='Technology',
            slug='technology',
            description='Tech articles'
        )
        self.assertEqual(category.name, 'Technology')
        self.assertEqual(category.slug, 'technology')

    def test_category_str_method(self):
        """Testa método __str__ da categoria"""
        category = Category.objects.create(
            name='Technology',
            slug='technology'
        )
        self.assertEqual(str(category), 'Technology')


class ArticleViewsTestCase(TestCase):
    """Testes para as views de artigos"""

    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_active=True
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.article = Article.objects.create(
            title='Test Article',
            content='Test content',
            author=self.user,
            category=self.category,
            status='published'
        )

    def test_article_list_view(self):
        """Testa a view de listagem de artigos"""
        response = self.client.get(reverse('articles:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Article')

    def test_article_detail_view(self):
        """Testa a view de detalhes do artigo"""
        response = self.client.get(
            reverse('articles:detail', kwargs={'slug': self.article.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Article')

    def test_article_create_requires_login(self):
        """Testa se criação de artigo requer login"""
        response = self.client.get(reverse('articles:create'))
        self.assertEqual(response.status_code, 302)  # Redirect para login

    def test_article_create_authenticated(self):
        """Testa criação de artigo com usuário autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('articles:create'))
        self.assertEqual(response.status_code, 200)


class ArticleFormTestCase(TestCase):
    """Testes para o formulário de artigos"""

    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

    def test_valid_article_form(self):
        """Testa formulário válido de artigo"""
        form_data = {
            'title': 'New Article',
            'content': 'This is the content of the new article.',
            'category': self.category.id,
            'status': 'draft'
        }
        form = ArticleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_article_form(self):
        """Testa formulário inválido de artigo"""
        form_data = {
            'title': '',  # Título vazio
            'content': 'Content',
            'category': self.category.id
        }
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
