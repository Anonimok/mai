# Arquitetura do Sistema - Aplicação de Grade Horária com IA

Esta seção descreve a arquitetura proposta para a aplicação de geração de grades horárias, detalhando seus componentes principais, suas responsabilidades e as interações entre eles.

## 1. Visão Geral

A aplicação seguirá uma arquitetura cliente-servidor desacoplada:

*   **Frontend (Cliente):** Uma aplicação web Single Page Application (SPA) desenvolvida em React, responsável pela interface do usuário, coleta de dados e interação.
*   **Backend (Servidor):** Uma API RESTful desenvolvida em Python com Flask, responsável pelo processamento dos dados, lógica de negócio, execução do algoritmo de IA para otimização da grade e comunicação com o frontend.

## 2. Componentes Detalhados

### 2.1. Frontend (React)

*   **Responsabilidades:**
    *   Renderizar a interface do usuário (UI).
    *   Fornecer formulários e componentes para upload de arquivos (catálogo, histórico, currículo).
    *   Apresentar formulários para o usuário inserir e editar suas preferências (interesses, horários, meta de conclusão, carga horária).
    *   Enviar os dados e arquivos para o backend através de chamadas à API RESTful.
    *   Receber a(s) grade(s) horária(s) gerada(s) pelo backend.
    *   Exibir a grade horária de forma clara e organizada (tabela, calendário).
    *   (Opcional) Permitir ajustes manuais na grade sugerida.
    *   Gerenciar o estado da aplicação no lado do cliente.
*   **Módulos Principais:**
    *   `components/`: Componentes reutilizáveis da UI (botões, inputs, tabelas, modal de upload, visualizador de grade).
    *   `pages/` ou `views/`: Componentes que representam as diferentes telas da aplicação (página inicial/upload, página de perfil, página de resultados).
    *   `services/` ou `api/`: Funções para interagir com a API do backend.
    *   `hooks/`: Hooks customizados para lógica reutilizável (ex: gerenciamento de estado de upload).
    *   `contexts/` ou `store/`: Para gerenciamento de estado global (preferências do usuário, dados carregados).

### 2.2. Backend (Flask)

*   **Responsabilidades:**
    *   Expor endpoints da API RESTful para comunicação com o frontend.
    *   Receber e validar os arquivos e dados enviados pelo frontend.
    *   Orquestrar o fluxo de processamento de dados e geração da grade.
    *   Gerenciar o armazenamento temporário (ou persistente, se DB for usado) dos dados processados.
    *   Executar o módulo de IA para resolver o problema de otimização da grade.
    *   Formatar os resultados e enviá-los de volta ao frontend.
    *   Lidar com erros e exceções.
*   **Módulos Principais (seguindo o template `create_flask_app`):**
    *   `src/main.py`: Ponto de entrada da aplicação Flask, configuração inicial, registro de blueprints.
    *   `src/routes/`: Definição dos endpoints da API (ex: `upload_routes.py`, `schedule_routes.py`, `profile_routes.py`). Cada arquivo define um `Blueprint` Flask.
        *   `/api/upload/catalog` (POST): Recebe e processa o arquivo do catálogo.
        *   `/api/upload/history` (POST): Recebe e processa o arquivo de histórico.
        *   `/api/upload/curriculum` (POST): Recebe e processa o arquivo do currículo.
        *   `/api/profile` (GET, POST, PUT): Gerencia as preferências do usuário.
        *   `/api/schedule/generate` (POST): Dispara a geração da grade, usando os dados já processados e as preferências do perfil.
    *   `src/modules/`: Contém a lógica de negócio principal, separada das rotas.
        *   `data_parser.py`: Funções para ler e pré-processar os diferentes tipos de arquivos (Excel, CSV). Lógica para lidar com o formato "D.HHMM-C".
        *   `pdf_parser.py` (Potencialmente complexo): Funções para tentar extrair dados de PDFs (histórico, currículo). *Nota: Esta parte pode exigir ferramentas externas ou ser substituída por entrada manual se a extração automática for inviável.*
        *   `scheduler_ai.py`: Implementação do núcleo de IA. Contém a lógica para:
            *   Modelar o problema (variáveis, domínios).
            *   Definir as restrições (conflitos, pré-requisitos, vagas, etc.).
            *   Definir a função objetivo ou critérios de preferência.
            *   Utilizar a biblioteca de otimização (`python-constraint` ou `ortools`) para encontrar soluções.
        *   `data_manager.py`: Gerencia o acesso aos dados processados (armazenamento temporário em memória/disco por sessão, ou interação com DB no futuro).
    *   `src/static/` (Se necessário): Arquivos estáticos servidos diretamente pelo Flask (menos provável com frontend React separado).
    *   `venv/`: Ambiente virtual Python.
    *   `requirements.txt`: Dependências Python.

## 3. Fluxo de Dados (Exemplo de Geração de Grade)

1.  **Usuário (Frontend):** Faz upload dos arquivos (catálogo, histórico, currículo) e preenche/confirma suas preferências.
2.  **Frontend -> Backend:** Envia os arquivos e preferências para os endpoints da API Flask (`/api/upload/*`, `/api/profile`).
3.  **Backend (Data Processing):** Os módulos `data_parser.py` e `pdf_parser.py` processam os arquivos. O `data_manager.py` armazena os dados processados associados à sessão do usuário.
4.  **Usuário (Frontend):** Clica no botão "Gerar Grade".
5.  **Frontend -> Backend:** Envia uma requisição para `/api/schedule/generate`.
6.  **Backend (Orquestração):** A rota correspondente em `schedule_routes.py` chama o `data_manager.py` para obter os dados processados e as preferências do usuário.
7.  **Backend (IA):** A rota chama a função principal em `scheduler_ai.py`, passando os dados necessários.
8.  **Backend (IA - `scheduler_ai.py`):**
    *   Modela o problema com base nos dados.
    *   Aplica restrições e preferências.
    *   Executa o solver (`python-constraint` ou `ortools`).
    *   Retorna a(s) solução(ões) encontradas.
9.  **Backend -> Frontend:** A rota formata a(s) grade(s) em JSON e envia como resposta à requisição do passo 5.
10. **Frontend:** Recebe a resposta, processa o JSON e exibe a(s) grade(s) para o usuário.

## 4. Considerações Adicionais

*   **Gerenciamento de Estado:** Inicialmente, os dados processados podem ser armazenados em memória no servidor associados a um ID de sessão, ou em arquivos temporários. Para persistência entre sessões ou múltiplos usuários, a integração com um banco de dados (MySQL, conforme planejado na stack) será necessária.
*   **Tratamento de Erros:** Implementar tratamento robusto de erros em ambos os lados (frontend e backend) para lidar com falhas no upload, processamento de dados inválidos, ou cenários onde nenhuma grade viável pode ser encontrada.
*   **Extração de PDF:** A extração de dados estruturados de PDFs (especialmente históricos e currículos) é notoriamente difícil e propensa a erros. Uma abordagem inicial mais segura pode ser focar em formatos mais estruturados (CSV/Excel) ou permitir que o usuário insira manualmente as informações chave desses documentos.

