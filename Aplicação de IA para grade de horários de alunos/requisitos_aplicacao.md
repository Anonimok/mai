# Requisitos da Aplicação de Grade Horária com IA

## 1. Objetivo Principal

Desenvolver uma aplicação web que utilize inteligência artificial para gerar grades horárias personalizadas e otimizadas para estudantes universitários, levando em consideração múltiplos fatores acadêmicos e pessoais.

## 2. Requisitos Funcionais

### 2.1. Entradas de Dados (Inputs)

A aplicação deverá ser capaz de processar as seguintes informações:

*   **Catálogo de Disciplinas:** Importação de arquivos (Excel/CSV, como `CADASTRO_TURMAS_20251`, `Merged file.csv`) contendo detalhes das disciplinas ofertadas, incluindo: código da disciplina, nome, horários (no formato original "D.HHMM-C"), créditos, vagas totais ofertadas e saldo de vagas atualizado.
*   **Histórico Acadêmico do Aluno:** Importação de arquivo específico do aluno (ex: `HISTORICO_ESCOLAR_KAUÊ_DOS_SANTOS.pdf` ou formato similar) detalhando as disciplinas já cursadas, notas obtidas e pré-requisitos já cumpridos.
*   **Currículo do Curso:** Importação de arquivo (ex: `CURRICULO_ADMINISTRAÇÃO_(NOTURNO)_20231.pdf` ou formato similar) que define a estrutura curricular, a sequência recomendada de disciplinas, regras de pré-requisitos e possíveis equivalências entre disciplinas.
*   **Perfil e Preferências do Aluno:** Interface para o aluno cadastrar e atualizar suas informações e preferências, incluindo:
    *   Interesses temáticos (áreas de maior afinidade dentro do curso).
    *   Horários preferenciais e horários indisponíveis (trabalho, outras atividades).
    *   Experiências anteriores relevantes (estágios, projetos) que podem influenciar a escolha de disciplinas.
    *   Meta de conclusão do curso (em quantos semestres/anos pretende finalizar).
    *   Carga horária desejada por período (mínima e máxima).

### 2.2. Processamento e Lógica de IA

O núcleo da aplicação consistirá em:

*   **Pré-processamento de Dados:** Conversão e padronização dos dados importados, especialmente a transformação do formato de horário "D.HHMM-C" para um formato padrão (dia da semana, hora de início, hora de fim) que facilite a detecção de conflitos.
*   **Modelagem de Restrições:** Definição formal das regras e restrições que a grade horária deve seguir:
    *   **Não-conflito de Horários:** Nenhuma disciplina selecionada pode ter horários sobrepostos.
    *   **Pré-requisitos:** Todas as disciplinas selecionadas devem ter seus pré-requisitos cumpridos (com base no histórico e currículo).
    *   **Equivalências:** Considerar disciplinas equivalentes ao verificar pré-requisitos e disciplinas já cursadas.
    *   **Disponibilidade de Vagas:** Priorizar disciplinas com saldo de vagas positivo, potencialmente excluindo ou penalizando disciplinas sem vagas.
    *   **Carga Horária:** Respeitar os limites de carga horária mínima e máxima definidos pelo aluno ou pelo curso.
    *   **Restrições de Horário do Aluno:** Evitar alocar disciplinas nos horários marcados como indisponíveis pelo aluno.
*   **Algoritmo de Otimização (IA):** Implementação de um algoritmo capaz de explorar o espaço de combinações possíveis de disciplinas e selecionar a melhor grade horária com base em múltiplos critérios ponderados:
    *   **Adequação às Preferências:** Maximizar o alinhamento com os interesses temáticos e horários preferenciais do aluno.
    *   **Progresso no Curso:** Priorizar disciplinas que contribuam para a conclusão do curso dentro da meta estabelecida.
    *   **Equilíbrio da Grade:** Buscar uma distribuição equilibrada da carga horária e dificuldade ao longo da semana.
    *   **Viabilidade:** Considerar a disponibilidade de vagas e a probabilidade de conseguir a matrícula.
    *   **Técnicas Sugeridas:** Programação por Restrição (CSP) ou Programação Linear Inteira (PLI), utilizando bibliotecas como `python-constraint`, `ortools` (Google), ou `PuLP`.
    *   **Ponderação e Descarte:** O algoritmo deve ser capaz de ponderar a importância relativa de cada critério e descartar combinações consideradas inviáveis ou extremamente improváveis (ex: disciplinas sem vagas, conflitos insolúveis com preferências essenciais).
*   **Aprendizado (Opcional/Futuro):** Capacidade de aprender com o feedback do usuário sobre as grades geradas para refinar as ponderações e melhorar futuras sugestões.

### 2.3. Saídas e Interação (Outputs)

A aplicação deverá fornecer:

*   **Visualização da Grade:** Apresentação clara da grade horária recomendada, preferencialmente em formato de tabela ou calendário (dias da semana x horários), mostrando as disciplinas alocadas.
*   **Múltiplas Opções (Opcional):** Apresentar algumas das melhores opções de grade encontradas, permitindo ao aluno escolher.
*   **Interface de Ajustes:** Permitir que o aluno faça ajustes manuais na grade sugerida (ex: trocar uma disciplina por outra compatível).
*   **Feedback:** Mecanismo para o aluno fornecer feedback sobre a qualidade da grade gerada, que pode ser usado para recalibrar o algoritmo.

## 3. Requisitos Não-Funcionais

*   **Plataforma:** Aplicação Web acessível por navegador.
*   **Interface:** Intuitiva, fácil de usar e responsiva (adaptável a diferentes tamanhos de tela, como desktop e mobile).
*   **Performance:** Tempo de resposta aceitável para o processamento e geração da grade, mesmo com catálogos de disciplinas e currículos complexos.
*   **Integração de Dados:** Foco inicial na importação de arquivos (Excel, CSV, PDF). A integração direta com sistemas acadêmicos via API pode ser considerada como uma evolução futura.
*   **Modularidade:** Arquitetura que facilite a manutenção, a atualização das regras de negócio (currículos, critérios de ponderação) e a adição de novas funcionalidades.
*   **Tecnologia:** A ser definida na próxima fase, mas deve suportar os algoritmos de IA e a interface web (ex: Python com Flask/Django para backend, React/Vue/Next.js para frontend).
*   **Segurança:** Garantir a privacidade dos dados dos alunos.
*   **Escalabilidade:** Capacidade de lidar com um número crescente de usuários e dados no futuro.
