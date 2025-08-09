# Sistema de Gerenciamento de Módulos - Viixen

## Visão Geral

O sistema de gerenciamento de módulos permite controlar quais funcionalidades estão disponíveis globalmente e por empresa, com distinção entre módulos core (essenciais) e opcionais.

## Arquitetura

### Modelos

#### Module
- `name`: Nome do módulo
- `slug`: Identificador único
- `app_label`: Label da aplicação Django
- `description`: Descrição do módulo
- `icon`: Ícone FontAwesome
- `is_active`: Status global do módulo
- `is_core`: Marca módulos essenciais (não podem ser desabilitados)
- `order`: Ordem de exibição

#### CompanyModule
- `company`: Empresa associada
- `module`: Módulo associado
- `is_active`: Status do módulo para a empresa específica
- `activated_at`: Data de ativação

### Regras de Negócio

#### Módulos Core
- **Sempre ativos**: Não podem ser desabilitados
- **Essenciais**: pages, accounts, config
- **Acesso universal**: Disponíveis para todas as empresas

#### Módulos Opcionais
- **Controle global**: Superadmins/Admins podem ativar/desativar globalmente
- **Controle por empresa**: Admins de empresa podem ativar/desativar para sua empresa
- **Dependência**: Só podem ser ativados por empresa se estiverem ativos globalmente

### Permissões

#### Superadmin + Administrador (Grupo)
- ✅ Ver todos os módulos
- ✅ Ativar/desativar módulos globalmente
- ✅ Gerenciar módulos de qualquer empresa
- ✅ Acesso irrestrito a todas as funcionalidades

#### Admin de Empresa
- ✅ Ver módulos da própria empresa
- ✅ Ativar/desativar módulos opcionais da empresa
- ❌ Não pode desativar módulos core
- ❌ Não pode ativar módulos inativos globalmente

#### Usuário Regular
- ✅ Ver status dos módulos da empresa
- ❌ Não pode alterar configurações de módulos

## Componentes Implementados

### Views
- `ModuleGlobalListView`: Listagem global de módulos (superadmin/admin)
- `ModuleGlobalToggleView`: Toggle global de módulos
- `CompanyModuleListView`: Listagem de módulos por empresa
- `CompanyModuleToggleView`: Toggle de módulos por empresa
- `CompanyModuleToggleAjaxView`: Toggle via AJAX

### Templates
- `config/modules/global_list.html`: Interface de gerenciamento global
- `config/modules/company_list.html`: Interface de gerenciamento por empresa
- `config/includes/module_status_badge.html`: Badge de status do módulo

### URLs
```
# Gerenciamento global (superadmin/admin)
/config/modules/                           # Lista global
/config/modules/<id>/toggle/              # Toggle global

# Gerenciamento por empresa
/config/company/modules/                   # Lista da empresa
/config/company/modules/<id>/toggle/      # Toggle da empresa
/config/company/modules/<id>/ajax-toggle/ # Toggle AJAX
```

### Middleware
- `ModuleAccessMiddleware`: Bloqueia acesso a módulos desativados

### Template Tags
- `is_module_active`: Verifica se módulo está ativo para usuário
- `get_active_modules`: Lista módulos ativos do usuário
- `get_module_count`: Conta módulos por tipo
- `module_status_badge`: Renderiza badge de status

### Comandos de Gerenciamento
- `setup_modules`: Popula módulos iniciais do sistema

## Fluxos de Uso

### Como Superadmin/Administrador
1. Acessar "Gerenciar Módulos" no dashboard ou navbar
2. Ver todos os módulos (core e opcionais)
3. Ativar/desativar módulos globalmente
4. Gerenciar módulos de qualquer empresa

### Como Admin de Empresa
1. Acessar "Módulos da Empresa" no dashboard ou navbar
2. Ver módulos core (sempre ativos) e opcionais disponíveis
3. Ativar/desativar módulos opcionais para a empresa
4. Usar toggle switch para mudanças rápidas

### Segurança e Validações
- Módulos core não podem ser desativados
- Validações impedem ações não autorizadas
- Middleware bloqueia acesso a módulos inativos
- Permissões verificadas em todas as operações

## Integração com Sistema Existente

### Dashboard
- Links para gerenciamento adicionados
- Estatísticas de módulos exibidas
- Seção específica para admins globais

### Navbar
- Links de acesso rápido no menu do usuário
- Visibilidade baseada em permissões

### Admin Django
- Interface administrativa para módulos
- Proteção contra alteração de módulos core

## Próximos Passos

1. **Executar Migrações**: Aplicar migration do campo `is_core`
2. **Popular Módulos**: Executar comando `setup_modules`
3. **Testar Funcionalidades**: Validar todos os fluxos
4. **Configurar Middleware**: Adicionar às configurações do Django
5. **Documentar para Usuários**: Criar guia de uso

## Tecnologias Utilizadas

- Django Class-Based Views
- Bootstrap 5 para UI
- FontAwesome para ícones
- AJAX para interações dinâmicas
- Django Template Tags personalizadas
- Middleware personalizado

## Status

✅ **IMPLEMENTAÇÃO COMPLETA**
- Todos os componentes desenvolvidos
- Permissões e validações implementadas
- Interface responsiva e intuitiva
- Documentação técnica criada

O sistema está pronto para testes e uso em produção após aplicação das migrações e configuração do middleware.
