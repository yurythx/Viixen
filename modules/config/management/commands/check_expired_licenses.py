from django.core.management.base import BaseCommand
from django.utils import timezone
from modules.config.services.company_service import CompanyService
from modules.config.domain.module import CompanyModule


class Command(BaseCommand):
    help = 'Verifica e desativa módulos com licenças expiradas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Executa sem fazer alterações, apenas mostra o que seria feito',
        )
        parser.add_argument(
            '--notify-expiring',
            type=int,
            default=7,
            help='Notifica sobre licenças que expiram em X dias (padrão: 7)',
        )

    def handle(self, *args, **options):
        service = CompanyService()
        dry_run = options['dry_run']
        notify_days = options['notify_expiring']
        
        self.stdout.write(
            self.style.SUCCESS(f'=== Verificação de Licenças Expiradas ===')
        )
        self.stdout.write(f'Data/Hora: {timezone.now().strftime("%d/%m/%Y %H:%M:%S")}')
        self.stdout.write(f'Modo: {"DRY RUN" if dry_run else "EXECUÇÃO"}')
        self.stdout.write('')

        # 1. Verificar licenças expiradas
        expired_licenses = service.get_expired_licenses()
        self.stdout.write(
            self.style.WARNING(f'Licenças Expiradas: {expired_licenses.count()}')
        )
        
        if expired_licenses.exists():
            for company_module in expired_licenses:
                status = "ATIVO" if company_module.is_active else "INATIVO"
                self.stdout.write(
                    f'  - {company_module.company.name}: {company_module.module.name} '
                    f'(expirou em {company_module.license_expires_at.strftime("%d/%m/%Y")}) '
                    f'[{status}]'
                )
            
            if not dry_run:
                deactivated_count = service.auto_deactivate_expired_licenses()
                self.stdout.write(
                    self.style.SUCCESS(f'✓ {deactivated_count} módulo(s) desativado(s)')
                )
            else:
                active_expired = expired_licenses.filter(is_active=True).count()
                self.stdout.write(
                    self.style.WARNING(f'→ {active_expired} módulo(s) seriam desativados')
                )
        else:
            self.stdout.write('  Nenhuma licença expirada encontrada.')

        self.stdout.write('')

        # 2. Verificar licenças expirando
        expiring_licenses = service.get_expiring_licenses(days_ahead=notify_days)
        self.stdout.write(
            self.style.WARNING(f'Licenças Expirando ({notify_days} dias): {expiring_licenses.count()}')
        )
        
        if expiring_licenses.exists():
            for company_module in expiring_licenses:
                days_left = company_module.days_until_expiration
                self.stdout.write(
                    f'  - {company_module.company.name}: {company_module.module.name} '
                    f'(expira em {days_left} dias - {company_module.license_expires_at.strftime("%d/%m/%Y")})'
                )
        else:
            self.stdout.write(f'  Nenhuma licença expirando nos próximos {notify_days} dias.')

        self.stdout.write('')

        # 3. Estatísticas gerais
        total_licensed = CompanyModule.objects.filter(is_licensed=True).count()
        total_active = CompanyModule.objects.filter(is_licensed=True, is_active=True).count()
        
        self.stdout.write('=== Estatísticas Gerais ===')
        self.stdout.write(f'Total de licenças ativas: {total_licensed}')
        self.stdout.write(f'Módulos ativos: {total_active}')
        self.stdout.write(f'Licenças expiradas: {expired_licenses.count()}')
        self.stdout.write(f'Licenças expirando ({notify_days} dias): {expiring_licenses.count()}')
        
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS('=== Verificação Concluída ===')
        )
        
        # Sugestões de ação
        if expired_licenses.exists() or expiring_licenses.exists():
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('AÇÕES RECOMENDADAS:'))
            
            if expired_licenses.exists():
                self.stdout.write('• Renovar licenças expiradas ou confirmar desativação')
                
            if expiring_licenses.exists():
                self.stdout.write(f'• Renovar licenças que expiram nos próximos {notify_days} dias')
                
            self.stdout.write('• Acessar: /config/modules/expiration/ para gerenciar')
