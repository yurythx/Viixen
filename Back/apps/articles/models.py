from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string

class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Gerar o slug base a partir do título
            base_slug = slugify(self.title)
            
            # Verificar se já existe um artigo com esse slug
            if Article.objects.filter(slug=base_slug).exists():
                # Se existir, adiciona um sufixo aleatório para garantir unicidade
                self.slug = f"{base_slug}-{get_random_string(4)}"
            else:
                self.slug = base_slug
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.name} on {self.article.title}"
    
    def save(self, *args, **kwargs):
        # Validação para garantir que o parent seja do mesmo artigo
        if self.parent and self.parent.article_id != self.article_id:
            raise ValueError("O comentário pai deve pertencer ao mesmo artigo")
        
        super().save(*args, **kwargs)