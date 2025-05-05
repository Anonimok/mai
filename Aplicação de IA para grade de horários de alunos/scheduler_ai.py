# -*- coding: utf-8 -*-
"""Módulo principal da IA para geração de grade horária usando Programação por Restrição."""

from constraint import Problem, AllDifferentConstraint
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Funções Auxiliares para Restrições ---

def time_conflict_checker(schedule1, schedule2):
    """Verifica se dois horários (listas de dicts) de disciplinas conflitam."""
    for slot1 in schedule1:
        for slot2 in schedule2:
            # Verifica sobreposição no mesmo dia
            if slot1["dia_semana"] == slot2["dia_semana"]:
                # Conflito se: inicio1 < fim2 E inicio2 < fim1
                if slot1["inicio_min"] < slot2["fim_min"] and slot2["inicio_min"] < slot1["fim_min"]:
                    return True # Há conflito
    return False # Não há conflito

class NoTimeConflictConstraint:
    """Restrição customizada para verificar conflitos de horário entre múltiplas disciplinas."""
    def __init__(self, courses_data):
        # courses_data: dicionário {codigo_disciplina: {turma: horarios_processados, ...}}
        self.courses_data = courses_data

    def __call__(self, variables, domains, assignments, forwardcheck=False):
        # variables: lista de códigos de disciplina selecionados para esta verificação
        # assignments: dicionário {codigo_disciplina: turma_selecionada}

        selected_schedules = []
        for course_code in variables:
            if course_code in assignments:
                selected_turma = assignments[course_code]
                # Ignora se a disciplina não foi selecionada (turma = None ou similar)
                if selected_turma is None or selected_turma == "NAO_CURSAR":
                    continue
                # Busca os horários processados para a turma selecionada
                schedule = self.courses_data.get(course_code, {}).get(selected_turma, {}).get("horarios_processados")
                if schedule:
                    selected_schedules.append(schedule)
                else:
                     # Se não encontrar o horário, assume que a atribuição é inválida
                     # logger.warning(f"Horário não encontrado para {course_code} - {selected_turma}")
                     return False # Inviável

        # Compara cada par de horários selecionados
        for i in range(len(selected_schedules)):
            for j in range(i + 1, len(selected_schedules)):
                if time_conflict_checker(selected_schedules[i], selected_schedules[j]):
                    return False # Encontrou conflito

        return True # Nenhum conflito encontrado

# --- Função Principal de Geração --- #

def generate_schedule(catalog_df, history_data, curriculum_data, preferences):
    """Gera a grade horária usando CSP."""

    if catalog_df is None or catalog_df.empty:
        logger.error("Catálogo de disciplinas vazio ou inválido.")
        return None

    problem = Problem()

    # --- Processamento Inicial --- #
    # Agrupar turmas por código de disciplina
    courses = {}
    for index, row in catalog_df.iterrows():
        code = row["codigo_disciplina"]
        turma_id = row.get("turma", f"T{index}") # Usa a coluna turma ou um ID único
        if code not in courses:
            courses[code] = {}
        courses[code][turma_id] = {
            "nome": row["nome_disciplina"],
            "horarios_processados": row["horarios_processados"],
            "vagas_disponiveis": row["vagas_disponiveis"],
            "creditos": row.get("creditos", 0) # Assume 0 se não houver
        }

    # --- Definição de Variáveis e Domínios --- #
    # Variáveis: Códigos das disciplinas potenciais a serem cursadas.
    # Domínio: Turmas disponíveis para cada disciplina + opção de não cursar.
    potential_courses = list(courses.keys()) # Inicialmente, todas as disciplinas do catálogo

    # TODO: Filtrar `potential_courses` com base no histórico e currículo
    # - Remover disciplinas já cursadas (do history_data["disciplinas_cursadas"])
    # - Priorizar/Selecionar disciplinas obrigatórias do período (do curriculum_data)
    # - Verificar pré-requisitos (comparar curriculum_data["pre_requisitos"] com history_data)

    disciplinas_cursadas = history_data.get("disciplinas_cursadas", [])
    potential_courses = [c for c in potential_courses if c not in disciplinas_cursadas]

    logger.info(f"Disciplinas consideradas após filtro inicial: {len(potential_courses)}")

    for course_code in potential_courses:
        available_turmas = list(courses[course_code].keys())
        # Filtrar turmas sem vagas
        available_turmas = [t for t in available_turmas if courses[course_code][t]["vagas_disponiveis"] > 0]

        domain = available_turmas
        if not domain: # Se não há turmas com vagas, não adiciona a variável
             logger.warning(f"Disciplina {course_code} sem turmas com vagas disponíveis.")
             continue

        # Adiciona a opção de não cursar a disciplina
        domain.append("NAO_CURSAR")
        problem.addVariable(course_code, domain)

    # --- Definição de Restrições --- #

    # 1. Sem Conflitos de Horário
    # Passa todos os dados de cursos para a restrição poder consultar os horários
    no_conflict_constraint = NoTimeConflictConstraint(courses)
    # Aplica a restrição a todas as variáveis (disciplinas)
    problem.addConstraint(no_conflict_constraint, potential_courses)

    # 2. Carga Horária (Exemplo)
    min_credits = preferences.get("min_creditos", 12)
    max_credits = preferences.get("max_creditos", 24)

    def credit_constraint(*turmas_selecionadas):
        # turmas_selecionadas é uma tupla com as turmas escolhidas para cada variável na ordem
        current_credits = 0
        variable_codes = potential_courses # Ordem das variáveis como adicionadas
        for i, turma in enumerate(turmas_selecionadas):
            if turma != "NAO_CURSAR":
                course_code = variable_codes[i]
                # Verifica se a disciplina ainda está sendo considerada (pode ter sido removida se não tinha vagas)
                if course_code in courses:
                     current_credits += courses[course_code][turma].get("creditos", 0)

        return min_credits <= current_credits <= max_credits

    # Garante que só adiciona a restrição se houver variáveis no problema
    if potential_courses:
         # Obter a lista atual de variáveis do problema, pois algumas podem ter sido puladas
         actual_variables = problem.getVariables()
         if actual_variables:
              problem.addConstraint(credit_constraint, actual_variables)
         else:
              logger.warning("Nenhuma variável adicionada ao problema, pulando restrição de crédito.")
    else:
        logger.warning("Nenhuma disciplina potencial encontrada, pulando restrição de crédito.")


    # TODO: Adicionar mais restrições:
    # - Pré-requisitos (requer dados de currículo e histórico)
    # - Preferências de horário do aluno (não alocar em horários indisponíveis)
    # - Interesses temáticos (priorizar disciplinas de interesse - pode ser feito pós-processamento)
    # - Disciplinas obrigatórias

    # --- Resolução --- #
    logger.info("Iniciando a busca por soluções...")
    solutions = problem.getSolutions()
    logger.info(f"Encontradas {len(solutions)} soluções.")

    # --- Pós-processamento (Seleção da Melhor Solução) --- #
    if not solutions:
        return [] # Retorna lista vazia se não houver solução

    # Critérios de seleção (exemplo simples: maximizar créditos, priorizar vagas)
    # Pode-se adicionar critérios mais complexos como alinhamento com interesses.
    best_solution = None
    max_score = -1

    processed_solutions = []

    for solution in solutions:
        current_credits = 0
        current_vagas_score = 0 # Soma das vagas disponíveis (maior é melhor?)
        schedule_details = [] # Lista para armazenar detalhes da grade

        selected_courses_count = 0
        for course_code, turma in solution.items():
            if turma != "NAO_CURSAR":
                selected_courses_count += 1
                details = courses[course_code][turma]
                current_credits += details.get("creditos", 0)
                current_vagas_score += details.get("vagas_disponiveis", 0)
                schedule_details.append({
                    "codigo": course_code,
                    "nome": details["nome"],
                    "turma": turma,
                    "horarios": details["horarios_processados"],
                    "creditos": details.get("creditos", 0)
                })

        # Pontuação simples: prioriza mais créditos, depois mais vagas
        # Adiciona um pequeno bônus por ter mais disciplinas (evita soluções vazias se o min_credits for 0)
        score = current_credits * 1000 + current_vagas_score + selected_courses_count

        processed_solutions.append({
            "score": score,
            "creditos": current_credits,
            "disciplinas": schedule_details
        })

    # Ordena as soluções pela pontuação (maior primeiro)
    processed_solutions.sort(key=lambda x: x["score"], reverse=True)

    # Retorna as N melhores soluções (ex: top 5)
    return processed_solutions[:5]

