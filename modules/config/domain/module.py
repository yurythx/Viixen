from django.db import models
from django.utils.text import slugify
from .company import Company  # Adicionar este import

class Module(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    slug = models.SlugField(unique=True)
    app_label = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-cube')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    is_core = models.BooleanField(
        default=False, 
        verbose_name='Módulo Core',
        help_text='Módulos core não podem ser desabilitados (pages, accounts, config)'
    )
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
    is_active = models.BooleanField(default=False, verbose_name='Ativo')
    is_licensed = models.BooleanField(
        default=True, 
        verbose_name='Licenciado',
        help_text='Define se a empresa tem licença para usar este módulo'
    )
    license_expires_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name='Licença expira em',
        help_text='Data de expiração da licença. Deixe em branco para licença permanente.'
    )
    activated_at = models.DateTimeField(auto_now_add=True)
    licensed_at = models.DateTimeField(auto_now_add=True, verbose_name='Licenciado em')

    def __str__(self):
        return f"{self.company.name} - {self.module.name}"
    
    @property
    def can_be_activated(self):
        """Verifica se o módulo pode ser ativado (deve estar licenciado, não expirado e ativo globalmente)"""
        return self.is_licensed and not self.is_license_expired and self.module.is_active
    
    @property
    def is_license_expired(self):
        """Verifica se a licença está expirada"""
        if not self.license_expires_at:
            return False  # Licença permanente
        
        from django.utils import timezone
        return timezone.now() > self.license_expires_at
    
    @property
    def days_until_expiration(self):
        """Retorna quantos dias faltam para a licença expirar"""
        if not self.license_expires_at:
            return None  # Licença permanente
        
        from django.utils import timezone
        delta = self.license_expires_at - timezone.now()
        return delta.days if delta.days >= 0 else 0
    
    @property
    def is_license_expiring_soon(self):
        """Verifica se a licença está próxima do vencimento (30 dias)"""
        days_left = self.days_until_expiration
        return days_left is not None and 0 <= days_left <= 30
    
    @property
    def license_status(self):
        """Retorna o status da licença"""
        if not self.is_licensed:
            return 'unlicensed'
        elif self.is_license_expired:
            return 'expired'
        elif self.is_license_expiring_soon:
            return 'expiring_soon'
        else:
            return 'active'
    
    class Meta:
        unique_together = ['company', 'module']
        verbose_name = 'Módulo da Empresa'
        verbose_name_plural = 'Módulos das Empresas'