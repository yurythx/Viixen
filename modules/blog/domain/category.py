from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True, verbose_name='Descrição')
    color = models.CharField(max_length=7, default='#007bff')
    icon = models.CharField(max_length=50, default='fas fa-folder')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:category-posts', kwargs={'slug': self.slug})
    
    def posts_count(self):
        return self.posts.filter(status='published').count()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['order', 'name']