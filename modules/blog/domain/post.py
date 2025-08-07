from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True, verbose_name='Descrição')
    color = models.CharField(max_length=7, default='#007bff', help_text='Cor em hexadecimal')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
        ('archived', 'Arquivado'),
    ]
    
    title = models.CharField(max_length=255, verbose_name='Título')
    slug = models.SlugField(max_length=255)  # Removido unique=True
    content = models.TextField(verbose_name='Conteúdo')
    excerpt = models.TextField(max_length=300, blank=True, verbose_name='Resumo')
    
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
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            
            # Garantir slug único por empresa
            while BlogPost.objects.filter(company=self.company, slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        super().save(*args, **kwargs)
    
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

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, max_length=50)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']