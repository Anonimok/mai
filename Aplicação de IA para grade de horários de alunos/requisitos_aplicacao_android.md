# Requisitos da Aplicação Android - Gerador de Grade Horária

Este documento descreve os requisitos funcionais e não funcionais para a versão Android nativa da aplicação de geração de grade horária.

## 1. Visão Geral

A aplicação Android permitirá que estudantes universitários gerem sugestões de grade horária utilizando um backend Flask existente. O aplicativo fornecerá uma interface nativa para upload de arquivos, definição de preferências e visualização das grades geradas pela IA.

## 2. Requisitos Funcionais

### 2.1. Gerenciamento de Sessão
*   **RF01:** Ao iniciar, o aplicativo deve se comunicar com o endpoint `/api/session` do backend para criar uma nova sessão e obter um `session_id`.
*   **RF02:** O `session_id` deve ser armazenado localmente no dispositivo e enviado em todas as requisições subsequentes ao backend.
*   **RF03:** O aplicativo deve lidar com possíveis falhas na criação da sessão (ex: backend indisponível) e informar o usuário.

### 2.2. Upload de Arquivos
*   **RF04:** O aplicativo deve fornecer uma interface para o usuário selecionar e fazer upload de três tipos de arquivos:
    *   Catálogo de Disciplinas
    *   Histórico Escolar
    *   Currículo do Curso
*   **RF05:** O aplicativo deve utilizar o seletor de arquivos nativo do Android.
*   **RF06:** Os formatos de arquivo suportados para upload devem ser `.xlsx`, `.csv` e `.pdf` (embora o processamento de PDF no backend seja limitado).
*   **RF07:** O upload deve ser feito para os endpoints correspondentes do backend (`/api/upload/catalog`, `/api/upload/history`, `/api/upload/curriculum`), incluindo o `session_id`.
*   **RF08:** O aplicativo deve exibir o progresso do upload (se possível) e indicar sucesso ou falha para cada arquivo.
*   **RF09:** O aplicativo deve impedir o prosseguimento para as próximas etapas se o upload do Catálogo de Disciplinas falhar.

### 2.3. Definição de Preferências
*   **RF10:** O aplicativo deve apresentar uma tela onde o usuário possa definir suas preferências:
    *   Número mínimo de créditos.
    *   Número máximo de créditos.
*   **RF11:** O aplicativo deve validar as entradas do usuário (ex: mínimo <= máximo, valores numéricos válidos).
*   **RF12:** As preferências devem ser enviadas para o endpoint `/api/schedule/preferences` do backend, incluindo o `session_id`.
*   **RF13:** O aplicativo deve indicar sucesso ou falha ao salvar as preferências.

### 2.4. Geração de Grade Horária
*   **RF14:** O aplicativo deve ter um botão ou ação para iniciar o processo de geração de grade.
*   **RF15:** A ação só deve ser habilitada após o upload bem-sucedido do catálogo e o salvamento das preferências.
*   **RF16:** Ao ser acionado, o aplicativo deve enviar uma requisição para o endpoint `/api/schedule/generate` do backend, incluindo o `session_id`.
*   **RF17:** O aplicativo deve exibir um indicador de carregamento enquanto aguarda a resposta do backend.

### 2.5. Visualização da Grade Horária
*   **RF18:** Após receber as sugestões de grade do backend, o aplicativo deve exibi-las de forma clara e organizada, adequada para telas de dispositivos móveis.
*   **RF19:** Cada opção de grade deve mostrar as disciplinas, seus horários (dia, início, fim) e o total de créditos.
*   **RF20:** Se nenhuma grade for encontrada, o aplicativo deve informar o usuário.

### 2.6. Tratamento de Erros
*   **RF21:** O aplicativo deve capturar e exibir mensagens de erro de forma clara para o usuário em caso de falhas de comunicação com o backend, erros de validação ou outros problemas.

## 3. Requisitos Não Funcionais

*   **RNF01:** **Plataforma:** Android (versão mínima a ser definida, ex: Android 8.0 Oreo).
*   **RNF02:** **Linguagem:** Kotlin (preferencialmente) ou Java.
*   **RNF03:** **Arquitetura:** Seguir padrões de arquitetura Android recomendados (ex: MVVM - Model-View-ViewModel).
*   **RNF04:** **Interface do Usuário:** Seguir as diretrizes de design do Material Design 3.
*   **RNF05:** **Performance:** O aplicativo deve ser responsivo e não bloquear a thread principal durante operações de rede ou processamento.
*   **RNF06:** **Comunicação:** Utilizar bibliotecas de rede Android padrão (ex: Retrofit, Volley) para comunicação com a API Flask.
*   **RNF07:** **Persistência:** Armazenar o `session_id` de forma segura (ex: SharedPreferences).

## 4. Funcionalidades Futuras (Opcional)

*   Notificações push quando a geração da grade estiver concluída (se a geração for movida para background no backend).
*   Interface para adicionar preferências mais detalhadas (interesses, horários indisponíveis).
*   Visualização de grade mais interativa (ex: calendário).
*   Funcionalidade offline básica (cache de última grade gerada).

