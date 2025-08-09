# Generated manually for module management system

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='is_core',
            field=models.BooleanField(default=False, help_text='Módulos core não podem ser desabilitados (pages, accounts, config)', verbose_name='Módulo Core'),
        ),
    ]
