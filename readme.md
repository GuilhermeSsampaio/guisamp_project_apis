# Guisamp_project_apis

Este repositório contém a API unificada para múltiplos micro-projetos pessoais: Make Music (gestão de cifras e composições), Cook Ai (IA para receitas e scraping), MyLove4U (app para casais), e Liturgic Musics(app para músicas liturgicas católicas). O objetivo é manter um backend compartilhado com módulos independentes por projeto, reutilizando autenticação e configuração de banco.

## Visão geral

- Framework: FastAPI
- ORM: SQLModel (SQLAlchemy por baixo)
- Banco: SQLite (arquivo `database.db` por padrão)
- Estrutura: cada projeto fica em `backend/projects/<project_name>`; arquivos compartilhados em `backend/shared` (auth, db, etc.)

## Estrutura do repositório (relevante)

backend/

- main.py — ponto de entrada da API (inclui rotas e cria as tabelas)
- readme.md — este arquivo
- shared/ - auth/ — modelos, rotas e utilitários de autenticação compartilhada - db/ — configuração do banco, dependências de sessão
  projects/
- make_music/ — rotas, modelos e utils relacionados às cifras
- cookAi/ — rotas e modelos para receitas (scraping e IA)
- mylove4u/ — app para casais com diário, lembranças, jogos
- liturgic_musics/ — músicas litúrgicas

frontends — aplicação separada

## Como rodar (desenvolvimento)

1. Crie/ative o ambiente virtual (Windows PowerShell):

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Exportar/definir variáveis de ambiente (opcional):

- `GOOGLE_API_KEY` — chave para integração com Gemini (usada em `cookAi/services/gemini.py`) se necessário

3. Inicie a API (modo desenvolvimento):

```powershell
cd backend
fastapi dev main.py
```

> Observação: o `main.py` importa os modelos antes de chamar `create_db_and_tables()` para que todas as tabelas sejam registradas corretamente.

## Rotas principais

As rotas são organizadas por projeto e por prefix. Exemplos relevantes:

- Autenticação (compartilhada)

  - `POST /auth/users/` — criar usuário (ver `shared/auth/routes/users.py`)
  - `POST /auth/login/` — login

- Make Music

  - `GET /make_music/musical_compositions/list` — listar composições
  - `POST /make_music/musical_compositions/create_music` — criar composição
  - `GET /make_music/musical_compositions/view/{id}` — ver cifra formatada (HTML)

- Cook Ai
  - `GET /cook_ai/recipes/list` — listar receitas
  - `POST /cook_ai/recipes/create` — criar receita
  - `POST /cook_ai/recipes/scrap` — extrair receita de uma URL (scraper)
  - `POST /cook_ai/recipes/search` — gerar sugestões via IA (Gemini)

## Banco de dados e modelos

- Configuração: `backend/shared/db/config_db.py` cria o engine e provê a dependência `SessionDep` usada nas rotas.
- Quando o servidor inicia, `create_db_and_tables()` é chamado para criar as tabelas com base nos modelos carregados.
- Caso adicione novos modelos, importe-os em `main.py` antes de `create_db_and_tables()` ou certifique-se de que o módulo que os define seja importado ao iniciar a aplicação.

## Variáveis de ambiente úteis

- `GOOGLE_API_KEY` — (opcional) chave da Google Gemini/GenAI para endpoints que usam IA

## Testes rápidos e verificação

- Use um cliente HTTP (Insomnia, Postman, curl) para testar as rotas. Ou o swagger em /docs.
- Exemplo: listar composições

```powershell
curl http://127.0.0.1:8000/make_music/musical_compositions/list
```

## Boas práticas e notas de manutenção

- Mantenha modelos compartilhados (ex.: `User`) em `shared/` para evitar referências cruzadas quebradas.
- Importar modelos/registrá-los antes de criar tabelas evita erros como `NoReferencedTableError`.
- Use `TYPE_CHECKING` e imports locais em modelos para evitar importações circulares quando declarar `Relationship` entre modelos que vivem em módulos diferentes.

## Contribuindo

1. Crie uma branch para sua feature: `git checkout -b feat/minha-coisa`
2. Faça commits pequenos e atômicos
3. Abra PR descrevendo as mudanças

## Próximos passos recomendados

- Testes automatizados para os endpoints principais
- Adicionar autenticação JWT completa e autorização por rota
- Mover banco para Postgres em produção e ajustar URL em `config_db.py`

---
