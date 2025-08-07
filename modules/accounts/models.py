from .domain.user import CustomUser

# Exportar para que o Django encontre os modelos
__all__ = ['CustomUser']
from django.db import models

# Create your models here.
