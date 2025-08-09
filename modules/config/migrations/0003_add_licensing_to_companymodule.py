# Generated manually for module licensing system

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_add_is_core_to_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='companymodule',
            name='is_licensed',
            field=models.BooleanField(default=True, help_text='Define se a empresa tem licença para usar este módulo', verbose_name='Licenciado'),
        ),
        migrations.AddField(
            model_name='companymodule',
            name='licensed_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Licenciado em'),
            preserve_default=False,
        ),
    ]
