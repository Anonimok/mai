# Aplicação Geradora de Grade Horária com IA

Este projeto consiste em uma aplicação web full-stack para auxiliar estudantes universitários na criação de suas grades horárias. A aplicação utiliza inteligência artificial (via programação por restrições) para sugerir grades otimizadas com base no catálogo de disciplinas da universidade, histórico do aluno, currículo do curso e preferências do usuário.

## Estrutura do Projeto

O projeto está dividido em duas partes principais:

1.  **Backend (`grade_horaria_api/`)**: Uma API Flask (Python) responsável por:
    *   Gerenciar sessões de usuário.
    *   Receber e processar arquivos (catálogo, histórico, currículo).
    *   Armazenar dados da sessão (arquivos processados, preferências).
    *   Executar o algoritmo de IA para gerar sugestões de grade.
    *   Fornecer endpoints para comunicação com o frontend.
2.  **Frontend (`grade_horaria_ui/`)**: Uma aplicação React (TypeScript) construída com Vite, responsável por:
    *   Fornecer a interface do usuário para interação.
    *   Permitir o upload de arquivos.
    *   Coletar as preferências do usuário.
    *   Exibir as grades horárias geradas.
    *   Comunicar-se com a API backend.

## Tecnologias Utilizadas

*   **Backend**: Python, Flask, Flask-CORS, Pandas, openpyxl, python-constraint
*   **Frontend**: React, TypeScript, Vite, Tailwind CSS, shadcn/ui
*   **Gerenciamento de Pacotes**: pip (Python), pnpm (Node.js)

## Configuração e Execução

### Pré-requisitos

*   Python 3.10 ou superior
*   Node.js 20.x ou superior
*   pnpm (instalado via `npm install -g pnpm`)

### Backend (`grade_horaria_api/`)

1.  **Navegue até o diretório do backend:**
    ```bash
    cd grade_horaria_api
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate  # Windows
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    pip install pandas openpyxl python-constraint Flask-CORS # Garante que todas as dependências extras estejam instaladas
    ```
4.  **Execute o servidor Flask:**
    ```bash
    python src/main.py
    ```
    O backend estará rodando em `http://localhost:5000`.

### Frontend (`grade_horaria_ui/`)

1.  **Navegue até o diretório do frontend:**
    ```bash
    cd ../grade_horaria_ui
    ```
2.  **Instale as dependências:**
    ```bash
    pnpm install
    ```
3.  **Configure a URL da API:**
    *   Certifique-se de que o arquivo `.env.local` existe na raiz de `grade_horaria_ui/`.
    *   Ele deve conter a seguinte linha, apontando para o endereço onde o backend está rodando:
        ```
        NEXT_PUBLIC_API_URL=http://localhost:5000/api
        ```
4.  **Execute o servidor de desenvolvimento:**
    ```bash
    pnpm run dev
    ```
    O frontend estará acessível em `http://localhost:5173` (ou outra porta indicada pelo Vite).

## Uso da Aplicação

1.  Abra o frontend no seu navegador (`http://localhost:5173`).
2.  A aplicação criará automaticamente uma sessão com o backend.
3.  **Upload de Arquivos:**
    *   Faça o upload do **Catálogo de Disciplinas** (formato `.xlsx` ou `.csv`, seguindo a estrutura explicada nos requisitos ou usando `catalogo_teste.xlsx`).
    *   Faça o upload do **Histórico Escolar** e **Currículo do Curso** (atualmente, o processamento de PDF é um placeholder; use arquivos vazios ou de exemplo se não tiver CSV/Excel).
4.  **Preferências:**
    *   Defina os créditos mínimos e máximos desejados.
    *   Clique em "Salvar Preferências".
5.  **Gerar Grade:**
    *   Clique em "Gerar Grade Horária".
    *   Aguarde o processamento. As grades sugeridas serão exibidas.

## Arquivos de Documentação Incluídos

*   `requisitos_aplicacao.md`: Detalhes sobre os requisitos funcionais e não funcionais.
*   `stack_tecnologica.md`: Justificativa para a escolha das tecnologias.
*   `arquitetura_sistema.md`: Visão geral da arquitetura da aplicação.
*   `catalogo_teste.xlsx`: Arquivo de exemplo para o catálogo de disciplinas.

## Próximos Passos e Melhorias

*   Implementar processamento robusto de arquivos PDF para Histórico e Currículo.
*   Integrar a verificação automática de pré-requisitos com base no currículo.
*   Adicionar campos para preferências do usuário (interesses, horários preferenciais/indisponíveis) e integrá-los ao algoritmo de IA.
*   Melhorar a interface do usuário e a visualização das grades.
*   Adicionar testes unitários e de integração.
*   Resolver o problema de implantação do backend Flask no ambiente de produção.

