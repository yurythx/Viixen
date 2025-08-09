# 🎨 Guia do Tema Ubuntu/Yaru - Projeto Viixen

## 📋 Visão Geral

Este guia documenta as melhorias implementadas para tornar o tema do projeto Viixen mais fiel ao design system oficial do Ubuntu/Yaru.

## 🎨 Paleta de Cores Ubuntu Oficial

### Cores Primárias
- **Ubuntu Orange**: `#E95420` - Cor principal do Ubuntu
- **Ubuntu Orange Light**: `#FF7139` - Para hover states
- **Ubuntu Orange Dark**: `#C7431A` - Para pressed states

### Cores Neutras
- **Ubuntu Cool Grey**: `#333333` - Texto principal
- **Ubuntu Warm Grey**: `#AEA79F` - Texto secundário
- **Ubuntu Light Grey**: `#F7F7F7` - Background claro
- **Ubuntu Mid Grey**: `#CDCDCD` - Bordas e divisores

### Cores de Estado
- **Ubuntu Green**: `#0E8420` - Sucesso
- **Ubuntu Red**: `#C7162B` - Erro/Perigo
- **Ubuntu Yellow**: `#F99B11` - Aviso
- **Ubuntu Blue**: `#19B6EE` - Informação

## 🧩 Componentes Implementados

### 1. Cards com Variantes Ubuntu
```html
<!-- Card com accent Ubuntu (borda laranja) -->
<div class="card card-ubuntu-accent">
    <div class="card-body">
        <h5 class="card-title">Título do Card</h5>
        <p class="card-text">Conteúdo do card...</p>
    </div>
</div>

<!-- Outras variantes -->
<div class="card card-ubuntu-success">...</div>  <!-- Verde -->
<div class="card card-ubuntu-warning">...</div>  <!-- Amarelo -->
<div class="card card-ubuntu-danger">...</div>   <!-- Vermelho -->
```

### 2. Botões com Estilo Ubuntu
```html
<!-- Botões com cores Ubuntu -->
<button class="btn btn-primary">Primário</button>
<button class="btn btn-ubuntu-success">Sucesso</button>
<button class="btn btn-ubuntu-warning">Aviso</button>
<button class="btn btn-ubuntu-danger">Perigo</button>
```

### 3. Formulários Ubuntu
- Inputs com focus laranja característico
- Border-radius de 4px (menos arredondado)
- Sombras internas sutis
- Checkbox/radio com accent-color Ubuntu

## 📐 Design System

### Tipografia
- **Fonte**: Ubuntu (Google Fonts)
- **Pesos**: 300 (Light), 400 (Regular), 500 (Medium), 700 (Bold)
- **Line-height**: 1.5 para texto, 1.2 para headings

### Espaçamentos
Baseado em múltiplos de 4px (padrão Ubuntu):
- **XS**: 4px
- **SM**: 8px  
- **MD**: 16px
- **LG**: 24px
- **XL**: 32px

### Sombras
- **Light**: `0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)`
- **Medium**: `0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23)`
- **Heavy**: `0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23)`

### Border Radius
- **Padrão**: 4px (menos arredondado que o comum)
- **Cards**: 8px
- **Botões**: 4px

## 🌓 Tema Escuro

O tema escuro usa:
- **Background**: `#1E1E1E` (Ubuntu Darker Grey)
- **Cards**: `#2C2C2C` (Ubuntu Dark Grey)
- **Texto**: `#FFFFFF` (branco puro)
- **Bordas**: `#555555`

## 🚀 Como Usar

### 1. Classes de Espaçamento Ubuntu
```html
<div class="ubuntu-spacing-md">Conteúdo com espaçamento médio</div>
```

### 2. Componentes Reutilizáveis
```html
<!-- Modal Ubuntu -->
{% include 'components/_modal.html' with modal_id='exemploModal' modal_title='Título' modal_icon='fas fa-info' %}

<!-- Toast Ubuntu -->
{% include 'components/_toast.html' %}

<!-- Card Ubuntu -->
{% include 'components/_card.html' with card_title='Título' card_class='card-ubuntu-accent' %}
```

### 3. Exemplo Completo de Página
```html
<div class="container ubuntu-spacing-lg">
    <h1>Título da Página</h1>
    
    <div class="row">
        <div class="col-md-6">
            <div class="card card-ubuntu-accent">
                <div class="card-body">
                    <h5 class="card-title">Informações</h5>
                    <p class="card-text">Conteúdo importante...</p>
                    <button class="btn btn-primary">Ação Principal</button>
                </div>
            </div>
        </div>
        
        <div class="col-md-6">
            <form>
                <div class="mb-3">
                    <label class="form-label">Campo</label>
                    <input type="text" class="form-control" placeholder="Digite...">
                </div>
                <button type="submit" class="btn btn-ubuntu-success">Enviar</button>
            </form>
        </div>
    </div>
</div>
```

## 📱 Responsividade

O tema inclui breakpoints específicos:
- **Mobile**: até 576px
- **Tablet**: 577px - 768px  
- **Desktop**: 769px+

## ♿ Acessibilidade

- Contraste adequado em todas as cores
- Focus visível com outline laranja
- Skip links implementados
- Atributos ARIA em componentes
- Navegação por teclado completa

## 🎯 Diferenças do Tema Anterior

### Melhorias Implementadas:
1. **Cores mais fiéis** ao Ubuntu oficial
2. **Border-radius reduzido** (4px vs 6px)
3. **Sombras padronizadas** do design system
4. **Tipografia refinada** com line-heights corretos
5. **Espaçamentos baseados em 4px**
6. **Focus states** com cor Ubuntu
7. **Variantes de componentes** específicas do Ubuntu

## 📖 Referências

- [Ubuntu Design System](https://design.ubuntu.com/)
- [Yaru Theme Guidelines](https://github.com/ubuntu/yaru)
- [Ubuntu Brand Guidelines](https://design.ubuntu.com/brand/)

---

**Resultado**: Tema 100% fiel ao Ubuntu/Yaru com componentes reutilizáveis e design system completo! 🎉
