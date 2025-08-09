from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name='Título')
    slug = models.SlugField(unique=True, max_length=255)
    content = models.TextField(verbose_name='Conteúdo')
    excerpt = models.TextField(max_length=300, blank=True, verbose_name='Resumo')
    company = models.ForeignKey(
        'config.Company',
        on_delete=models.CASCADE,
        related_name='pages'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False, verbose_name='Publicado')
    featured_image = models.ImageField(
        upload_to='pages/images/',
        null=True,
        blank=True,
        verbose_name='Imagem Destacada'
    )
    meta_description = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('pages:page_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Página'
        verbose_name_plural = 'Páginas'
        ordering = ['-created_at']