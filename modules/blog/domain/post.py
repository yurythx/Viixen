from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.mixins.auto_slug import AutoSlugMixin, custom_slugify

User = get_user_model()

class Category(AutoSlugMixin, models.Model):
    """
    Model representing a blog post category.
    Uses AutoSlugMixin to automatically generate a slug from the name.
    """
    name = models.CharField(max_length=100, verbose_name='Nome')
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True, verbose_name='Descrição')
    color = models.CharField(max_length=7, default='#007bff', help_text='Cor em hexadecimal')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __init__(self, *args, **kwargs):
        self.slug_source = 'name'  # Field to generate slug from
        self.slug_field = 'slug'   # Field to store the slug in
        super().__init__(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        """Meta options for Category model."""
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

class BlogPost(AutoSlugMixin, models.Model):
    """
    Model representing a blog post.
    Uses AutoSlugMixin to automatically generate a slug from the title.
    """
    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
        ('archived', 'Arquivado'),
    ]
    
    title = models.CharField(max_length=255, verbose_name='Título')
    slug = models.SlugField(max_length=255)
    content = models.TextField(verbose_name='Conteúdo')
    excerpt = models.TextField(max_length=300, blank=True, verbose_name='Resumo')
    
    def __init__(self, *args, **kwargs):
        self.slug_source = 'title'  # Field to generate slug from
        self.slug_field = 'slug'    # Field to store the slug in
        super().__init__(*args, **kwargs)
    
    # Relacionamentos
    company = models.ForeignKey(
        'config.Company',
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='posts'
    )
    
    # Mídia
    featured_image = models.ImageField(
        upload_to='blog/images/',
        null=True,
        blank=True,
        verbose_name='Imagem Destacada'
    )
    
    # Status e SEO
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    is_featured = models.BooleanField(default=False, verbose_name='Destaque')
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Estatísticas
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def generate_unique_slug(self):
        """
        Generate a unique slug for the blog post, ensuring it's unique per company.
        """
        base_slug = custom_slugify(self.title)
        unique_slug = base_slug
        counter = 1
        
        while BlogPost.objects.filter(company=self.company, slug=unique_slug).exclude(pk=getattr(self, 'pk', None)).exists():
            unique_slug = f"{base_slug}-{counter}"
            counter += 1
            
        return unique_slug
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def is_published(self):
        return self.status == 'published'
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Post do Blog'
        verbose_name_plural = 'Posts do Blog'
        ordering = ['-created_at']
        unique_together = [['company', 'slug']]  # Slug único por empresa
        indexes = [
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['company', 'status']),
            models.Index(fields=['company', 'slug']),
        ]

class View(models.Model):
    """
    Model representing a view/visit to a blog post.
    Used for tracking unique views and analytics.
    """
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='views',
        verbose_name='Post'
    )
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='Endereço IP')
    session_key = models.CharField(max_length=40, blank=True, null=True, verbose_name='Chave de sessão')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='post_views',
        verbose_name='Usuário'
    )
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name='Data da visualização')
    
    class Meta:
        verbose_name = 'Visualização'
        verbose_name_plural = 'Visualizações'
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['post', 'viewed_at']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['session_key']),
        ]
    
    def __str__(self):
        return f"Visualização de {self.post.title} em {self.viewed_at}"

class Tag(AutoSlugMixin, models.Model):
    """
    Model representing a tag for blog posts.
    Uses AutoSlugMixin to automatically generate a slug from the name.
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, max_length=50)
    
    def __init__(self, *args, **kwargs):
        self.slug_source = 'name'  # Field to generate slug from
        self.slug_field = 'slug'   # Field to store the slug in
        super().__init__(*args, **kwargs)
    
    class Meta:
        """Meta options for Tag model."""
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']
        
    def __str__(self):
        return self.name

class Comment(models.Model):
    """
    Model representing a comment on a blog post.
    """
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('spam', 'Spam'),
        ('trash', 'Lixeira'),
    ]
    
    post = models.ForeignKey(
        'BlogPost', 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name='Post'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_comments',
        verbose_name='Autor'
    )
    author_name = models.CharField(max_length=100, blank=True, verbose_name='Nome do autor')
    author_email = models.EmailField(blank=True, verbose_name='E-mail do autor')
    author_url = models.URLField(blank=True, verbose_name='Website')
    content = models.TextField(verbose_name='Comentário')
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name='Status'
    )
    is_spam = models.BooleanField(default=False, verbose_name='É spam?')
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='Endereço IP')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name='Resposta a'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de atualização')
    
    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']
    
    def __str__(self):
        return f'Comentário de {self.author_name} em {self.post.title}'
    
    def approve(self):
        """Aprova o comentário."""
        self.status = 'approved'
        self.is_spam = False
        self.save()
    
    def mark_as_spam(self):
        """Marca o comentário como spam."""
        self.status = 'spam'
        self.is_spam = True
        self.save()
    
    def move_to_trash(self):
        """Move o comentário para a lixeira."""
        self.status = 'trash'
        self.save()
    
    @property
    def is_approved(self):
        """Retorna True se o comentário estiver aprovado."""
        return self.status == 'approved'
    
    @property
    def is_pending(self):
        """Retorna True se o comentário estiver pendente."""
        return self.status == 'pending'
    
    @property
    def has_replies(self):
        """Retorna True se o comentário tiver respostas."""
        return self.replies.exists()
    
    @property
    def depth(self):
        """Retorna a profundidade do comentário na árvore de respostas."""
        if self.parent is None:
            return 0
        return self.parent.depth + 1

class Favorite(models.Model):
    """
    Model representing a user's favorite blog post.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_posts',
        verbose_name='Usuário'
    )
    post = models.ForeignKey(
        'BlogPost',
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Post'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    
    class Meta:
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
        ordering = ['-created_at']
        unique_together = ['user', 'post']  # Evita duplicatas
    
    def __str__(self):
        return f"{self.user.username} favoritou {self.post.title}"
    
    @classmethod
    def toggle_favorite(cls, user, post):
        """
        Adiciona ou remove um post dos favoritos do usuário.
        Retorna True se o post foi adicionado, False se foi removido.
        """
        favorite, created = cls.objects.get_or_create(user=user, post=post)
        if not created:
            favorite.delete()
            return False
        return True
    
    @classmethod
    def is_favorite(cls, user, post):
        """Verifica se um post está nos favoritos do usuário."""
        return cls.objects.filter(user=user, post=post).exists()
    
    @classmethod
    def get_user_favorites(cls, user, limit=None):
        """
        Retorna os posts favoritos do usuário.
        
        Args:
            user: O usuário
            limit: Número máximo de favoritos a retornar (opcional)
            
        Returns:
            QuerySet de posts favoritos
        """
        queryset = cls.objects.filter(user=user).select_related('post')
        if limit is not None:
            queryset = queryset[:limit]
        return queryset