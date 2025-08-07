from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nome')
    slug = models.SlugField(unique=True, max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    domain = models.CharField(max_length=255, unique=True, null=True, blank=True)
    logo = models.ImageField(upload_to='companies/logos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('config:company-detail', kwargs={'slug': self.slug})
    
    def active_modules_count(self):
        return self.companymodule_set.filter(is_active=True).count()
    
    def total_modules_count(self):
        return self.companymodule_set.count()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['name']