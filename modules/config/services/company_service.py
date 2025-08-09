from typing import List, Optional
from django.db.models import QuerySet
from ..domain.company import Company
from ..domain.module import Module, CompanyModule
from ..repositories.company_repository import CompanyRepository

class CompanyService:
    def __init__(self):
        self.repository = CompanyRepository()
    
    def get_company_by_id(self, company_id: int) -> Optional[Company]:
        return self.repository.get_by_id(company_id)
    
    def get_company_by_domain(self, domain: str) -> Optional[Company]:
        return self.repository.get_by_domain(domain)
    
    def get_available_modules(self) -> QuerySet[Module]:
        return Module.objects.filter(is_active=True).order_by('order')
    
    def get_company_active_modules(self, company: Company) -> QuerySet[Module]:
        return Module.objects.filter(
            companymodule__company=company,
            companymodule__is_active=True
        ).order_by('order')
    
    def activate_module(self, company: Company, module: Module) -> CompanyModule:
        company_module, created = CompanyModule.objects.get_or_create(
            company=company,
            module=module,
            defaults={'is_active': True}
        )
        
        if not created and not company_module.is_active:
            company_module.is_active = True
            company_module.save()
        
        return company_module
    
    def deactivate_module(self, company: Company, module: Module) -> bool:
        # Não permitir desativar módulos core
        if module.is_core:
            return False
            
        try:
            company_module = CompanyModule.objects.get(
                company=company,
                module=module
            )
            company_module.is_active = False
            company_module.save()
            return True
        except CompanyModule.DoesNotExist:
            return False
    
    def get_core_modules(self) -> QuerySet[Module]:
        """Retorna módulos core do sistema"""
        return Module.objects.filter(is_core=True, is_active=True).order_by('order')
    
    def get_optional_modules(self) -> QuerySet[Module]:
        """Retorna módulos opcionais (não core)"""
        return Module.objects.filter(is_core=False, is_active=True).order_by('order')
    
    def can_deactivate_module(self, module: Module) -> bool:
        """Verifica se um módulo pode ser desativado"""
        return not module.is_core
    
    def get_company_optional_modules(self, company: Company) -> QuerySet[Module]:
        """Retorna módulos opcionais ativos para uma empresa"""
        return Module.objects.filter(
            is_core=False,
            is_active=True,
            companymodule__company=company,
            companymodule__is_active=True
        ).order_by('order')
    
    def get_optional_modules_for_company(self, company: Company):
        """Retorna módulos opcionais ativos para uma empresa específica"""
        return CompanyModule.objects.filter(
            company=company,
            module__is_core=False,
            module__is_active=True,
            is_active=True,
            is_licensed=True
        ).select_related('module')
    
    def license_module_for_company(self, company: Company, module: Module, expires_at=None) -> bool:
        """Licencia um módulo para uma empresa"""
        if module.is_core:
            return True  # Módulos core são sempre licenciados
        
        company_module, created = CompanyModule.objects.get_or_create(
            company=company,
            module=module,
            defaults={
                'is_licensed': True, 
                'is_active': False,
                'license_expires_at': expires_at
            }
        )
        
        if not created and not company_module.is_licensed:
            company_module.is_licensed = True
            company_module.license_expires_at = expires_at
            company_module.save()
        
        return True
    
    def revoke_module_license(self, company: Company, module: Module) -> bool:
        """Remove a licença de um módulo para uma empresa"""
        if module.is_core:
            return False  # Não pode remover licença de módulos core
        
        try:
            company_module = CompanyModule.objects.get(
                company=company,
                module=module
            )
            company_module.is_licensed = False
            company_module.is_active = False  # Desativar também se remover licença
            company_module.save()
            return True
        except CompanyModule.DoesNotExist:
            return False
    
    def get_licensed_companies_for_module(self, module: Module):
        """Retorna empresas que têm licença para um módulo"""
        if module.is_core:
            # Módulos core são licenciados para todas as empresas
            return Company.objects.filter(is_active=True)
        
        return Company.objects.filter(
            companymodule__module=module,
            companymodule__is_licensed=True,
            is_active=True
        ).distinct()
    
    def get_unlicensed_companies_for_module(self, module: Module):
        """Retorna empresas que NÃO têm licença para um módulo"""
        if module.is_core:
            return Company.objects.none()  # Módulos core são licenciados para todos
        
        licensed_company_ids = CompanyModule.objects.filter(
            module=module,
            is_licensed=True
        ).values_list('company_id', flat=True)
        
        return Company.objects.filter(
            is_active=True
        ).exclude(id__in=licensed_company_ids)
    
    def bulk_license_module(self, module: Module, company_ids: list) -> int:
        """Licencia um módulo para múltiplas empresas"""
        if module.is_core:
            return 0  # Módulos core já são licenciados
        
        licensed_count = 0
        for company_id in company_ids:
            try:
                company = Company.objects.get(id=company_id, is_active=True)
                if self.license_module_for_company(company, module):
                    licensed_count += 1
            except Company.DoesNotExist:
                continue
        
        return licensed_count
    
    def bulk_revoke_module_license(self, module: Module, company_ids: list) -> int:
        """Remove licença de um módulo para múltiplas empresas"""
        if module.is_core:
            return 0  # Não pode remover licença de módulos core
        
        revoked_count = 0
        for company_id in company_ids:
            try:
                company = Company.objects.get(id=company_id, is_active=True)
                if self.revoke_module_license(company, module):
                    revoked_count += 1
            except Company.DoesNotExist:
                continue
        
        return revoked_count
    
    def get_expiring_licenses(self, days_ahead=30):
        """Retorna licenças que expiram nos próximos X dias"""
        from django.utils import timezone
        from datetime import timedelta
        
        expiration_date = timezone.now() + timedelta(days=days_ahead)
        
        return CompanyModule.objects.filter(
            is_licensed=True,
            license_expires_at__isnull=False,
            license_expires_at__lte=expiration_date,
            license_expires_at__gt=timezone.now()
        ).select_related('company', 'module')
    
    def get_expired_licenses(self):
        """Retorna licenças já expiradas"""
        from django.utils import timezone
        
        return CompanyModule.objects.filter(
            is_licensed=True,
            license_expires_at__isnull=False,
            license_expires_at__lte=timezone.now()
        ).select_related('company', 'module')
    
    def extend_license(self, company: Company, module: Module, new_expiration_date) -> bool:
        """Estende a licença de um módulo para uma empresa"""
        if module.is_core:
            return True  # Módulos core não têm expiração
        
        try:
            company_module = CompanyModule.objects.get(
                company=company,
                module=module
            )
            company_module.license_expires_at = new_expiration_date
            company_module.save()
            return True
        except CompanyModule.DoesNotExist:
            return False
    
    def renew_license(self, company: Company, module: Module, duration_days=365) -> bool:
        """Renova a licença de um módulo por X dias a partir de hoje"""
        from django.utils import timezone
        from datetime import timedelta
        
        new_expiration = timezone.now() + timedelta(days=duration_days)
        return self.extend_license(company, module, new_expiration)
    
    def auto_deactivate_expired_licenses(self) -> int:
        """Desativa automaticamente licenças expiradas"""
        expired_licenses = self.get_expired_licenses()
        deactivated_count = 0
        
        for company_module in expired_licenses:
            if company_module.is_active:
                company_module.is_active = False
                company_module.save()
                deactivated_count += 1
        
        return deactivated_count
    
    def update_company(self, company: Company, **kwargs) -> Company:
        return self.repository.update(company, **kwargs)