from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    company = models.ForeignKey(
        'config.Company',
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True
    )
    phone = models.CharField(max_length=20, blank=True)
    is_company_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username} - {self.company.name if self.company else 'Sem empresa'}"
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'