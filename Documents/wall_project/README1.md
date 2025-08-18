# Sistema de Gerenciamento de Projetos

## Descrição

Sistema web completo para gerenciamento de projetos eletrônicos, desenvolvido com Flask e SQLAlchemy seguindo o tutorial de banco de dados em Flask. O sistema permite adicionar, visualizar, editar e deletar projetos, incluindo informações sobre componentes e links do Tinkercad.

## Funcionalidades

### ✅ Implementadas e Testadas

1. **Página Principal (index.html)**
   - Lista todos os projetos salvos
   - Exibe informações resumidas de cada projeto
   - Botão para criar novo projeto
   - Interface responsiva e moderna

2. **Página de Adicionar Projeto (add.html)**
   - Formulário completo para criação de projetos
   - Campos: nome, descrição, link do Tinkercad
   - Sistema dinâmico de adição de componentes
   - Validação de dados no frontend
   - Salvamento via API REST

3. **Página de Visualização (view.html)**
   - Exibe detalhes completos do projeto
   - Lista todos os componentes com quantidades
   - Botões para editar e deletar
   - Link para Tinkercad (quando disponível)

4. **API REST Completa**
   - `GET /api/projetos` - Listar todos os projetos
   - `POST /api/projetos` - Criar novo projeto
   - `GET /api/projetos/{id}` - Obter projeto específico
   - `PUT /api/projetos/{id}` - Atualizar projeto
   - `DELETE /api/projetos/{id}` - Deletar projeto
   - `GET /api/health` - Verificação de saúde da API

## Tecnologias Utilizadas

### Backend
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM para banco de dados
- **Flask-SQLAlchemy** - Integração Flask + SQLAlchemy
- **Flask-CORS** - Suporte a CORS
- **SQLite** - Banco de dados (conforme tutorial)

### Frontend
- **HTML5** - Estrutura das páginas
- **CSS3** - Estilização moderna e responsiva
- **JavaScript** - Interatividade e comunicação com API
- **Fetch API** - Requisições HTTP assíncronas

## Estrutura do Projeto

```
wall_project/
├── src/
│   ├── models/
│   │   ├── user.py          # Modelo de usuário (template)
│   │   └── projeto.py       # Modelos Projeto e Componente
│   ├── routes/
│   │   ├── user.py          # Rotas de usuário (template)
│   │   └── projeto.py       # Rotas da API de projetos
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Estilos do projeto original
│   │   ├── js/
│   │   │   └── add.js       # JavaScript para página de adicionar
│   │   ├── index.html       # Página principal
│   │   ├── add.html         # Página de adicionar projeto
│   │   └── view.html        # Página de visualização
│   ├── database/
│   │   └── app.db           # Banco SQLite
│   └── main.py              # Aplicação principal
├── venv/                    # Ambiente virtual Python
├── run_server.py            # Script para executar servidor
└── requirements.txt         # Dependências Python
```

## Modelos de Banco de Dados

### Projeto
- `id` (Integer, Primary Key)
- `nome` (String, Required)
- `descricao` (Text, Optional)
- `tinkercad_link` (Text, Optional)
- `data_criacao` (DateTime, Auto)

### Componente
- `id` (Integer, Primary Key)
- `projeto_id` (Integer, Foreign Key)
- `nome` (String, Required)
- `quantidade` (Integer, Required)

## Como Executar

1. **Ativar ambiente virtual:**
   ```bash
   cd wall_project
   source venv/bin/activate
   ```

2. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Executar servidor:**
   ```bash
   python run_server.py
   ```

4. **Acessar aplicação:**
   - URL: http://localhost:5001
   - API: http://localhost:5001/api/

## Funcionalidades Testadas

### ✅ Teste Completo Realizado

3. **API:**
   - ✅ Endpoints funcionando
   - ✅ Dados persistidos no SQLite
   - ✅ CORS configurado

## Diferenças do Projeto Original

### Melhorias Implementadas

1. **Banco de Dados:**
   - Migração de MySQL para SQLite (conforme tutorial Flask)
   - Uso do SQLAlchemy ORM ao invés de mysql.connector
   - Relacionamentos adequados entre tabelas

2. **Arquitetura:**
   - Estrutura modular com blueprints
   - Separação de modelos e rotas
   - Configuração adequada do Flask

3. **Frontend:**
   - Páginas HTML servidas pelo Flask
   - JavaScript atualizado para nova API
   - Interface responsiva mantida


## Conclusão

O sistema foi implementado com sucesso seguindo o tutorial de banco de dados em Flask. Todas as funcionalidades principais estão operacionais:

- ✅ Adicionar projetos com componentes
- ✅ Visualizar lista de projetos
- ✅ Ver detalhes de projetos individuais
- ✅ API REST completa
- ✅ Interface moderna e responsiva
- ✅ Banco de dados SQLite com SQLAlchemy

O sistema está pronto para uso e pode ser facilmente expandido com novas funcionalidades.

