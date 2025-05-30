#!/usr/bin/env python
"""
Verificar todos os templates de accounts para ver se seguem o padrão da página de perfil
"""

import os
import glob

def verificar_templates_accounts():
    print("🎨 VERIFICAÇÃO TEMPLATES DE ACCOUNTS")
    print("=" * 60)
    
    # Encontrar todos os templates de accounts
    accounts_templates = []
    accounts_dir = "apps/accounts/templates/accounts/"
    
    if os.path.exists(accounts_dir):
        for file in glob.glob(os.path.join(accounts_dir, "*.html")):
            accounts_templates.append(file)
    
    print(f"📁 Encontrados {len(accounts_templates)} templates de accounts:")
    for template in accounts_templates:
        print(f"   - {os.path.basename(template)}")
    
    # Elementos do layout do perfil que devem estar presentes
    elementos_layout_perfil = [
        ('Container py-4', 'container py-4'),
        ('H1 title', '<h1 class="mb-4">'),
        ('Card mb-4', 'card mb-4'),
        ('Card header flex', 'card-header d-flex'),
        ('H5 mb-0', 'h5 mb-0'),
        ('Icon me-2', 'me-2'),
        ('Text primary', 'text-primary'),
        ('Btn sm', 'btn btn-sm'),
        ('Justify between', 'justify-content-between'),
        ('Form label', 'form-label'),
        ('Row structure', '<div class="row">'),
        ('Col md', 'col-md-'),
    ]
    
    # Elementos específicos de accounts
    elementos_accounts = [
        ('Extends base.html', 'extends "base.html"'),
        ('Block content', '{% block content %}'),
        ('CSRF token', '{% csrf_token %}'),
        ('User avatar', 'avatar'),
        ('Form validation', 'form.'),
        ('Bootstrap classes', 'class='),
        ('Responsive grid', 'col-'),
        ('Card body', 'card-body'),
        ('Button actions', 'btn'),
        ('Icon usage', 'fas fa-'),
    ]
    
    # Elementos que NÃO devem estar (padrões antigos)
    elementos_antigos = [
        ('Tab system', 'nav-tabs'),
        ('Tab content', 'tab-content'),
        ('Tab pane', 'tab-pane'),
        ('JavaScript tabs', 'data-bs-toggle="tab"'),
        ('Complex JS', 'addEventListener'),
        ('Old sidebar', 'sidebar'),
        ('Old layout', 'container-fluid'),
        ('Accordion old', 'accordion'),
    ]
    
    resultados = {}
    
    print("\n🔍 VERIFICANDO CADA TEMPLATE:")
    print("=" * 60)
    
    for template_path in accounts_templates:
        template_name = os.path.basename(template_path)
        print(f"\n📄 {template_name}:")
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar elementos do layout do perfil
            elementos_ok = 0
            for nome, elemento in elementos_layout_perfil:
                if elemento in content:
                    print(f"   ✅ {nome}")
                    elementos_ok += 1
                else:
                    print(f"   ❌ {nome}")
            
            # Verificar elementos específicos de accounts
            accounts_ok = 0
            for nome, elemento in elementos_accounts:
                if elemento in content:
                    accounts_ok += 1
            
            # Verificar elementos antigos (que não devem estar)
            elementos_antigos_removidos = 0
            for nome, elemento in elementos_antigos:
                if elemento not in content:
                    elementos_antigos_removidos += 1
                else:
                    print(f"   ⚠️ {nome} ainda presente")
            
            # Verificar funcionalidades específicas
            funcionalidades = []
            if 'profile' in template_name.lower():
                funcionalidades = ['avatar', 'get_full_name', 'cargo', 'departamento']
            elif 'edit' in template_name.lower():
                funcionalidades = ['form.', 'csrf_token', 'method="post"']
            elif 'list' in template_name.lower():
                funcionalidades = ['table', 'pagination', 'filter']
            elif 'login' in template_name.lower():
                funcionalidades = ['form.', 'password', 'username']
            elif 'register' in template_name.lower():
                funcionalidades = ['form.', 'email', 'password']
            
            func_ok = 0
            for func in funcionalidades:
                if func in content:
                    func_ok += 1
            
            # Calcular pontuação
            total_elementos = len(elementos_layout_perfil)
            total_accounts = len(elementos_accounts)
            total_antigos = len(elementos_antigos)
            total_func = len(funcionalidades) if funcionalidades else 1
            
            pontuacao_elementos = (elementos_ok / total_elementos) * 100
            pontuacao_accounts = (accounts_ok / total_accounts) * 100
            pontuacao_antigos = (elementos_antigos_removidos / total_antigos) * 100
            pontuacao_func = (func_ok / total_func) * 100
            
            pontuacao_total = (pontuacao_elementos + pontuacao_accounts + pontuacao_antigos + pontuacao_func) / 4
            
            resultados[template_name] = {
                'elementos_ok': elementos_ok,
                'total_elementos': total_elementos,
                'accounts_ok': accounts_ok,
                'total_accounts': total_accounts,
                'antigos_removidos': elementos_antigos_removidos,
                'total_antigos': total_antigos,
                'func_ok': func_ok,
                'total_func': total_func,
                'pontuacao': pontuacao_total
            }
            
            print(f"   📊 Layout: {pontuacao_elementos:.1f}%")
            print(f"   📊 Accounts: {pontuacao_accounts:.1f}%")
            print(f"   📊 Total: {pontuacao_total:.1f}%")
            
        except Exception as e:
            print(f"   ❌ Erro ao ler arquivo: {e}")
            resultados[template_name] = {'pontuacao': 0}
    
    print("\n" + "=" * 60)
    print("📊 RESUMO GERAL")
    print("=" * 60)
    
    templates_adaptados = 0
    pontuacao_media = 0
    
    for template_name, resultado in resultados.items():
        pontuacao = resultado.get('pontuacao', 0)
        pontuacao_media += pontuacao
        
        if pontuacao >= 80:
            status = "✅ ADAPTADO"
            templates_adaptados += 1
        elif pontuacao >= 60:
            status = "⚠️ PARCIAL"
        else:
            status = "❌ PENDENTE"
        
        print(f"{template_name:30} {pontuacao:6.1f}% {status}")
    
    pontuacao_media = pontuacao_media / len(resultados) if resultados else 0
    
    print(f"\n📈 ESTATÍSTICAS:")
    print(f"   📄 Total de templates: {len(accounts_templates)}")
    print(f"   ✅ Templates adaptados: {templates_adaptados}")
    print(f"   ⚠️ Templates parciais: {len([r for r in resultados.values() if 60 <= r.get('pontuacao', 0) < 80])}")
    print(f"   ❌ Templates pendentes: {len([r for r in resultados.values() if r.get('pontuacao', 0) < 60])}")
    print(f"   📊 Pontuação média: {pontuacao_media:.1f}%")
    
    # Verificar templates principais
    print(f"\n🎯 TEMPLATES PRINCIPAIS:")
    templates_principais = [
        'profile.html',
        'edit_profile.html', 
        'user_list.html',
        'user_detail.html',
        'user_form.html',
        'login.html',
        'register.html',
        'password_change.html',
        'password_reset.html'
    ]
    
    principais_adaptados = 0
    for template in templates_principais:
        if template in resultados:
            pontuacao = resultados[template].get('pontuacao', 0)
            if pontuacao >= 80:
                print(f"   ✅ {template} - {pontuacao:.1f}%")
                principais_adaptados += 1
            elif pontuacao >= 60:
                print(f"   ⚠️ {template} - {pontuacao:.1f}%")
            else:
                print(f"   ❌ {template} - {pontuacao:.1f}%")
        else:
            print(f"   ❓ {template} (não encontrado)")
    
    print(f"\n📊 Templates principais adaptados: {principais_adaptados}/{len([t for t in templates_principais if t in resultados])}")
    
    # Análise por categoria
    print(f"\n📋 ANÁLISE POR CATEGORIA:")
    categorias = {
        'Perfil': ['profile.html', 'edit_profile.html'],
        'Usuários': ['user_list.html', 'user_detail.html', 'user_form.html', 'user_create.html'],
        'Autenticação': ['login.html', 'register.html', 'logout.html'],
        'Senha': ['password_change.html', 'password_reset.html', 'password_reset_confirm.html'],
        'Ativação': ['activate.html', 'activation_sent.html', 'activation_complete.html']
    }
    
    for categoria, templates in categorias.items():
        adaptados = 0
        total = 0
        for template in templates:
            if template in resultados:
                total += 1
                if resultados[template].get('pontuacao', 0) >= 80:
                    adaptados += 1
        
        if total > 0:
            percentual = (adaptados / total) * 100
            print(f"   {categoria}: {adaptados}/{total} ({percentual:.1f}%)")
    
    return resultados

if __name__ == "__main__":
    verificar_templates_accounts()
