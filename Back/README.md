# Viixen Backend

Este é o backend do projeto Viixen, desenvolvido com Django e Django REST Framework.

## Arquitetura do Projeto

O projeto segue uma arquitetura em camadas, implementando os padrões de Repository e Service para separar as responsabilidades e facilitar a manutenção e os testes.

### Estrutura de Diretórios

```
Back/
├── apps/                 # Apps Django
│   ├── accounts/         # App de contas de usuário
│   ├── articles/         # App de artigos
│   ├── categories/       # App de categorias
│   └── mangas/           # App de mangás
├── core/                 # Configurações e módulos centrais
│   ├── repositories/     # Repositórios para acesso a dados
│   ├── services/         # Serviços para lógica de negócios
│   └── settings.py       # Configurações do Django
└── manage.py             # Script de gerenciamento do Django
```

### Padrões de Design Implementados

#### 1. Padrão de Repositório

O padrão de repositório encapsula a lógica de acesso a dados, fornecendo uma interface abstrata para as operações de CRUD (Create, Read, Update, Delete).

**Benefícios:**
- Separa a lógica de acesso a dados da lógica de negócios
- Facilita a manutenção e os testes
- Permite trocar a fonte de dados sem afetar a lógica de negócios

**Implementação:**
- `BaseRepository`: Classe base com métodos comuns para todos os repositórios
- Repositórios específicos: `ArticleRepository`, `UserRepository`, `CategoryRepository`, etc.

#### 2. Padrão de Serviço

O padrão de serviço encapsula a lógica de negócios, fornecendo uma interface para as operações de negócios.

**Benefícios:**
- Separa a lógica de negócios da lógica de apresentação
- Facilita a reutilização de código
- Melhora a testabilidade

**Implementação:**
- `BaseService`: Classe base com métodos comuns para todos os serviços
- Serviços específicos: `ArticleService`, `UserService`, `CategoryService`, etc.

### Fluxo de Dados

```
Cliente HTTP → Views → Serviços → Repositórios → Modelos → Banco de Dados
```

1. **Views (Controllers)**: Recebem as requisições HTTP, validam os dados e chamam os serviços apropriados
2. **Serviços**: Implementam a lógica de negócios e chamam os repositórios para acessar os dados
3. **Repositórios**: Acessam os modelos do Django para realizar operações no banco de dados
4. **Modelos**: Representam as entidades do domínio e são mapeados para tabelas no banco de dados

### Diagrama de Componentes

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    Views    │────▶│  Serviços   │────▶│ Repositórios│────▶│   Modelos   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Serializers │     │Lógica de    │     │Acesso a     │     │Banco de     │
│             │     │Negócios     │     │Dados        │     │Dados        │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

## Componentes Principais

### Repositórios

Os repositórios são responsáveis por encapsular a lógica de acesso a dados. Cada repositório é especializado em um modelo específico.

**Exemplo:**
```python
class ArticleRepository(BaseRepository):
    def get_featured(self) -> QuerySet:
        return self.model_class.objects.filter(featured=True)
```

### Serviços

Os serviços são responsáveis por encapsular a lógica de negócios. Cada serviço utiliza um ou mais repositórios para acessar os dados.

**Exemplo:**
```python
class ArticleService(BaseService):
    def get_featured_articles(self) -> QuerySet:
        return self.repository.get_featured()
```

### Views

As views são responsáveis por receber as requisições HTTP, validar os dados e chamar os serviços apropriados.

**Exemplo:**
```python
class ArticleViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'])
    def increment_views(self, request, slug=None):
        article = self.get_object()
        article_service.view_article(article.id)
        return Response({
            'status': 'success',
            'views_count': article.views_count
        })
```

## Benefícios da Arquitetura

1. **Separação de Responsabilidades**: Cada componente tem uma responsabilidade clara e bem definida
2. **Testabilidade**: Facilita a escrita de testes unitários e de integração
3. **Manutenibilidade**: Facilita a manutenção e evolução do código
4. **Reutilização**: Facilita a reutilização de código em diferentes partes do sistema
5. **Escalabilidade**: Facilita a escalabilidade do sistema, permitindo que diferentes componentes sejam escalados independentemente

## Como Contribuir

1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv env`
3. Ative o ambiente virtual: `source env/bin/activate` (Linux/Mac) ou `env\Scripts\activate` (Windows)
4. Instale as dependências: `pip install -r requirements.txt`
5. Execute as migrações: `python manage.py migrate`
6. Execute o servidor: `python manage.py runserver`