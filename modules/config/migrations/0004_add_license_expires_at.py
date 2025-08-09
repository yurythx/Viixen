# Generated manually for license expiration functionality

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0003_add_licensing_to_companymodule'),
    ]

    operations = [
        migrations.AddField(
            model_name='companymodule',
            name='license_expires_at',
            field=models.DateTimeField(blank=True, help_text='Data de expiração da licença. Deixe em branco para licença permanente.', null=True, verbose_name='Licença expira em'),
        ),
    ]
