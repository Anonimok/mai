# Stack Tecnológica - Aplicação de Grade Horária com IA

Com base nos requisitos funcionais e não-funcionais definidos para a aplicação de geração de grades horárias personalizadas, a seguinte stack tecnológica foi selecionada:

## 1. Backend

*   **Linguagem:** Python (versão 3.10+)
    *   **Justificativa:** Ecossistema robusto para ciência de dados, IA e manipulação de arquivos. Ampla disponibilidade de bibliotecas para otimização e processamento de dados.
*   **Framework Web:** Flask
    *   **Justificativa:** Leve, flexível e adequado para construir APIs RESTful para comunicação com o frontend. O template `create_flask_app` disponível facilita a estruturação inicial do projeto e a integração com banco de dados (MySQL), se necessário no futuro.
*   **Bibliotecas Principais (Python):**
    *   `pandas`: Para leitura, manipulação e pré-processamento de dados de arquivos Excel e CSV (catálogo de disciplinas, histórico parcial).
    *   `openpyxl`, `xlrd`: Dependências do pandas para leitura de arquivos Excel.
    *   `python-constraint` ou `google-ortools`: Para implementação do algoritmo de otimização baseado em Programação por Restrição (CSP) ou Programação Linear Inteira (PLI).
A escolha final entre eles dependerá da complexidade e da melhor adequação ao modelo de restrições.
    *   `PyPDF2` ou ferramenta externa (via `shell`): Para extração de texto de arquivos PDF (histórico escolar, currículo), caso necessário e viável. A extração de dados estruturados de PDFs pode ser complexa e exigir abordagens adicionais.
    *   `Flask`, `Flask-CORS`: Para a criação do servidor web e API, e para permitir requisições do frontend.
*   **Banco de Dados (Opcional/Futuro):** MySQL
    *   **Justificativa:** O template Flask (`create_flask_app`) já prevê a integração com MySQL, facilitando a persistência de dados processados, perfis de usuário e preferências, caso a aplicação evolua para além da importação de arquivos a cada uso.

## 2. Frontend

*   **Linguagem:** JavaScript (com TypeScript opcionalmente, para maior robustez)
*   **Framework/Biblioteca:** React
    *   **Justificativa:** Amplamente utilizado, com vasta comunidade e ecossistema. Permite a criação de interfaces de usuário interativas e componentizadas. O template `create_react_app` oferece uma base sólida com ferramentas modernas (Tailwind CSS, shadcn/ui, Recharts) para acelerar o desenvolvimento da UI.
*   **Gerenciador de Pacotes:** pnpm (conforme template `create_react_app`)
*   **Estilização:** Tailwind CSS (incluído no template)
    *   **Justificativa:** Framework CSS utility-first que permite rápida prototipagem e desenvolvimento de interfaces responsivas.
*   **Componentes UI:** shadcn/ui (incluído no template)
    *   **Justificativa:** Coleção de componentes React bem projetados e acessíveis, baseados no Radix UI e Tailwind CSS.
*   **Visualização de Dados (Opcional):** Recharts (incluído no template)
    *   **Justificativa:** Biblioteca de gráficos para React, útil para visualizações alternativas da grade ou estatísticas do curso.

## 3. Comunicação

*   **API:** RESTful API
    *   **Justificativa:** Padrão de comunicação entre o backend Flask e o frontend React, utilizando JSON como formato de dados.

## 4. Ambiente de Desenvolvimento e Implantação

*   **Controle de Versão:** Git
*   **Ambiente Backend:** Ambiente virtual Python (`venv`)
*   **Implantação:**
    *   Backend Flask: Pode ser implantado usando a ferramenta `deploy_apply_deployment` com o tipo `flask`.
    *   Frontend React: Build estático gerado pelo React, que pode ser implantado como `static` usando `deploy_apply_deployment` ou servido junto com o Flask (menos comum para esta stack).

Esta stack combina a força do Python para o processamento de dados e IA no backend com a flexibilidade e riqueza do React para a criação de uma interface de usuário moderna e interativa no frontend.
