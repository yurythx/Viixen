"""
Utilitários para configuração dinâmica de email
"""

from django.core.mail import get_connection, send_mail
from django.conf import settings
from .models import EmailConfig
import logging

logger = logging.getLogger(__name__)

def get_active_email_config():
    """
    Retorna a configuração de email ativa (prioriza a padrão)
    """
    try:
        # Primeiro, tentar obter a configuração padrão
        default_config = EmailConfig.objects.filter(is_default=True, is_active=True).first()
        if default_config:
            return default_config

        # Se não houver padrão, pegar qualquer configuração ativa
        return EmailConfig.objects.filter(is_active=True).first()
    except EmailConfig.DoesNotExist:
        return None

def get_email_connection(config=None):
    """
    Cria uma conexão de email usando a configuração especificada ou a ativa
    """
    if config is None:
        config = get_active_email_config()

    if not config:
        # Usar configurações padrão do Django
        return get_connection()

    try:
        # Escolher backend baseado na configuração
        if config.use_console_backend:
            # Usar backend de console para desenvolvimento
            connection = get_connection(
                backend='django.core.mail.backends.console.EmailBackend',
                fail_silently=False,
            )
        else:
            # Usar backend SMTP para produção
            connection = get_connection(
                backend='django.core.mail.backends.smtp.EmailBackend',
                host=config.email_host,
                port=config.email_port,
                username=config.email_host_user,
                password=config.get_password(),
                use_tls=config.email_use_tls,
                fail_silently=False,
            )
        return connection
    except Exception as e:
        logger.error(f"Erro ao criar conexão de email: {e}")
        return None

def send_email_with_config(subject, message, from_email=None, recipient_list=None, config=None, html_message=None):
    """
    Envia email usando a configuração especificada ou a ativa
    """
    if config is None:
        config = get_active_email_config()

    if not config:
        logger.warning("Nenhuma configuração de email ativa encontrada")
        return False

    if from_email is None:
        from_email = config.default_from_email

    if not recipient_list:
        logger.error("Lista de destinatários não fornecida")
        return False

    try:
        connection = get_email_connection(config)
        if not connection:
            return False

        result = send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            connection=connection,
            fail_silently=False,
            html_message=html_message
        )

        logger.info(f"Email enviado com sucesso para {recipient_list}")
        return result > 0

    except Exception as e:
        logger.error(f"Erro ao enviar email: {e}")
        return False

def test_email_connection(config=None):
    """
    Testa a conexão de email
    """
    if config is None:
        config = get_active_email_config()

    if not config:
        return False, "Nenhuma configuração de email ativa encontrada"

    try:
        connection = get_email_connection(config)
        if not connection:
            return False, "Erro ao criar conexão"

        # Testar abertura da conexão
        connection.open()
        connection.close()

        return True, "Conexão testada com sucesso"

    except Exception as e:
        return False, f"Erro na conexão: {str(e)}"

def send_test_email(recipient_email, config=None):
    """
    Envia um email de teste
    """
    if config is None:
        config = get_active_email_config()

    if not config:
        return False, "Nenhuma configuração de email ativa encontrada"

    subject = "🧪 Teste de Configuração de Email - Viixen"
    message = f"""
Olá!

Este é um email de teste do sistema Viixen.

Configuração utilizada:
- Servidor: {config.email_host}:{config.email_port}
- TLS: {'Sim' if config.email_use_tls else 'Não'}
- Usuário: {config.email_host_user}
- Email padrão: {config.default_from_email}

Se você recebeu este email, a configuração está funcionando corretamente! ✅

Data/Hora: {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}

Atenciosamente,
Sistema Viixen
    """

    html_message = f"""
    <html>
    <body>
        <h2>🧪 Teste de Configuração de Email - Viixen</h2>

        <p>Olá!</p>

        <p>Este é um email de teste do sistema Viixen.</p>

        <h3>Configuração utilizada:</h3>
        <ul>
            <li><strong>Servidor:</strong> {config.email_host}:{config.email_port}</li>
            <li><strong>TLS:</strong> {'Sim' if config.email_use_tls else 'Não'}</li>
            <li><strong>Usuário:</strong> {config.email_host_user}</li>
            <li><strong>Email padrão:</strong> {config.default_from_email}</li>
        </ul>

        <p style="color: green; font-weight: bold;">
            Se você recebeu este email, a configuração está funcionando corretamente! ✅
        </p>

        <p><small>Data/Hora: {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}</small></p>

        <p>Atenciosamente,<br>
        <strong>Sistema Viixen</strong></p>
    </body>
    </html>
    """

    try:
        success = send_email_with_config(
            subject=subject,
            message=message,
            recipient_list=[recipient_email],
            config=config,
            html_message=html_message
        )

        if success:
            return True, f"Email de teste enviado com sucesso para {recipient_email}"
        else:
            return False, "Falha no envio do email de teste"

    except Exception as e:
        return False, f"Erro ao enviar email de teste: {str(e)}"

def apply_email_settings_to_django(config=None):
    """
    Aplica as configurações de email ao Django (para uso em desenvolvimento)
    ATENÇÃO: Isso modifica as configurações em tempo de execução
    """
    if config is None:
        config = get_active_email_config()

    if not config:
        logger.warning("Nenhuma configuração de email ativa para aplicar")
        return False

    try:
        # Aplicar configurações ao Django baseado no modo
        if config.use_console_backend:
            # Modo desenvolvimento - emails no terminal
            settings.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
            logger.info("Backend de console aplicado - emails aparecerão no terminal")
        else:
            # Modo produção - envio real via SMTP
            settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
            settings.EMAIL_HOST = config.email_host
            settings.EMAIL_PORT = config.email_port
            settings.EMAIL_HOST_USER = config.email_host_user
            settings.EMAIL_HOST_PASSWORD = config.get_password()
            settings.EMAIL_USE_TLS = config.email_use_tls
            logger.info(f"Backend SMTP aplicado: {config.email_host}:{config.email_port}")

        settings.DEFAULT_FROM_EMAIL = config.default_from_email
        return True

    except Exception as e:
        logger.error(f"Erro ao aplicar configurações de email: {e}")
        return False

# Importar timezone no final para evitar problemas de importação circular
from django.utils import timezone
