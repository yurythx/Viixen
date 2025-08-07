from django.db import models
from django.utils.text import slugify
from .company import Company  # Adicionar este import

class Module(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    slug = models.SlugField(unique=True)
    app_label = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-cube')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['order', 'name']

class CompanyModule(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    activated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.company.name} - {self.module.name}"
    
    class Meta:
        unique_together = ['company', 'module']
        verbose_name = 'Módulo da Empresa'
        verbose_name_plural = 'Módulos das Empresas'