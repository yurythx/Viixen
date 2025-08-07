from .domain.company import Company
from .domain.module import Module, CompanyModule

# Exportar para que o Django encontre os modelos
__all__ = ['Company', 'Module', 'CompanyModule']
from django.db import models

# Create your models here.
