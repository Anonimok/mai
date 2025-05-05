# Design da Interface do Usuário (UI) - Aplicativo Android Gerador de Grade

Este documento descreve a proposta de design da interface do usuário para a versão Android nativa da aplicação, seguindo as diretrizes do Material Design 3.

## 1. Princípios Gerais

*   **Consistência:** Manter um design consistente em todas as telas.
*   **Clareza:** Informações e ações devem ser claras e fáceis de entender.
*   **Eficiência:** O fluxo do usuário para completar a tarefa principal (gerar grade) deve ser o mais direto possível.
*   **Feedback:** Fornecer feedback visual claro para ações do usuário (uploads, salvamentos, carregamento).
*   **Material Design 3:** Utilizar componentes, cores, tipografia e elevação conforme as especificações do Material 3.

## 2. Estrutura de Navegação

*   **Navegação Principal:** Utilizar uma `BottomNavigationView` (Barra de Navegação Inferior) com três destinos principais:
    1.  **Upload:** Tela para carregar os arquivos necessários.
    2.  **Preferências:** Tela para definir os parâmetros da grade.
    3.  **Grade:** Tela para iniciar a geração e visualizar os resultados.
*   **Tela Inicial:** Ao abrir o app, uma tela de carregamento (Splash Screen) pode ser exibida brevemente enquanto a sessão com o backend é estabelecida. Após a criação da sessão, o usuário é direcionado para a aba "Upload" da `BottomNavigationView`.

## 3. Descrição das Telas

### 3.1. Tela de Carregamento (Splash Screen - Opcional)
*   **Componentes:**
    *   Logo da aplicação (simples).
    *   Indicador de progresso (ex: `CircularProgressIndicator`).
*   **Funcionalidade:** Exibida ao iniciar o app enquanto a comunicação inicial com o backend (`/api/session`) ocorre. Transiciona automaticamente para a Tela Principal.

### 3.2. Tela Principal (com BottomNavigationView)
*   **Layout:**
    *   `AppBar` no topo com o título da aplicação ("Gerador de Grade").
    *   Conteúdo da aba selecionada no centro.
    *   `BottomNavigationView` na parte inferior com ícones e rótulos para "Upload", "Preferências" e "Grade".

### 3.3. Aba/Tela de Upload
*   **Layout:** `LinearLayout` vertical ou `ConstraintLayout`.
*   **Componentes:**
    *   Seção para "Catálogo de Disciplinas":
        *   Texto descritivo.
        *   Botão (`MaterialButton`) "Selecionar Catálogo" (ícone de upload).
        *   Indicador de status (ex: `TextView` com "Nenhum arquivo" / "Arquivo: nome.xlsx" / "Erro no upload" e um ícone correspondente).
    *   Seção para "Histórico Escolar":
        *   Similar ao catálogo (Botão, Indicador de status).
    *   Seção para "Currículo do Curso":
        *   Similar ao catálogo (Botão, Indicador de status).
    *   Indicador de progresso global (`LinearProgressIndicator`) visível durante o upload.
*   **Funcionalidade:** Ao clicar nos botões, abre o seletor de arquivos do Android. Exibe feedback sobre o status do upload de cada arquivo.

### 3.4. Aba/Tela de Preferências
*   **Layout:** `LinearLayout` vertical ou `ConstraintLayout`.
*   **Componentes:**
    *   Campo de entrada (`TextInputLayout` com `TextInputEditText`) para "Créditos Mínimos":
        *   Tipo de entrada: numérico.
        *   Validação de entrada.
    *   Campo de entrada (`TextInputLayout` com `TextInputEditText`) para "Créditos Máximos":
        *   Tipo de entrada: numérico.
        *   Validação de entrada.
    *   Botão (`MaterialButton`) "Salvar Preferências".
    *   `Snackbar` ou `Toast` para feedback de sucesso/erro ao salvar.
*   **Funcionalidade:** Permite ao usuário inserir e salvar suas preferências de crédito. O botão "Salvar" envia os dados para o backend.

### 3.5. Aba/Tela de Grade
*   **Layout:** `LinearLayout` vertical ou `ConstraintLayout`.
*   **Componentes:**
    *   Botão (`MaterialButton`) "Gerar Grade Horária":
        *   Habilitado apenas se o catálogo foi carregado e as preferências foram salvas.
    *   Indicador de progresso (`CircularProgressIndicator` ou similar) exibido durante a geração.
    *   Área de Resultados:
        *   `TextView` para mensagens (ex: "Nenhuma grade encontrada", "Erro ao gerar grade").
        *   `RecyclerView` para exibir a lista de grades sugeridas.
            *   Cada item da lista (`ViewHolder`) representará uma grade sugerida.
            *   O item da grade pode usar `CardView` para agrupar as informações.
            *   Dentro do Card: `TextViews` para listar as disciplinas (Código, Nome, Horário Formatado - Dia, HH:MM - HH:MM), e um `TextView` para o total de créditos daquela grade.
*   **Funcionalidade:** Inicia a geração da grade ao clicar no botão. Exibe um indicador de carregamento. Mostra os resultados em uma lista rolável ou uma mensagem apropriada.

## 4. Componentes Chave (Material Design 3)

*   `BottomNavigationView`: Navegação principal.
*   `MaterialButton`: Para ações (upload, salvar, gerar).
*   `TextInputLayout` / `TextInputEditText`: Para entrada de preferências.
*   `CircularProgressIndicator` / `LinearProgressIndicator`: Feedback de carregamento/upload.
*   `RecyclerView`: Para exibir a lista de grades.
*   `CardView`: Para agrupar informações de cada grade sugerida.
*   `Snackbar` / `Toast`: Para mensagens de feedback curtas.
*   `TextView`: Para exibir textos, rótulos e status.

## 5. Fluxo do Usuário

1.  Abrir App -> (Splash Screen -> Criação de Sessão) -> Tela Principal (Aba Upload).
2.  **Upload:** Selecionar e carregar Catálogo, Histórico, Currículo.
3.  Navegar para Aba **Preferências**.
4.  **Preferências:** Inserir créditos min/max -> Salvar Preferências.
5.  Navegar para Aba **Grade**.
6.  **Grade:** Clicar em "Gerar Grade Horária" -> Aguardar (Indicador de Progresso) -> Visualizar Resultados na lista.

Este design inicial fornece uma estrutura clara e funcional. Detalhes específicos de layout, cores e ícones serão definidos durante a implementação usando temas e estilos do Material Design 3.
