# -*- coding: utf-8 -*-
"""Módulo para processar os arquivos de entrada (catálogo, histórico, currículo)."""

import pandas as pd
import re
import logging
import sys # Import sys for potential future use (like installing chardet)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_schedule_string(schedule_str):
    """Converte a string de horário D.HHMM-C em uma lista de tuplas (dia, inicio_min, fim_min)."""
    if not isinstance(schedule_str, str):
        return []

    # Exemplo: "2.1830-2 4.1830-2" -> [("Seg", 1110, 1220), ("Qua", 1110, 1220)] (2 * 55 min = 110 min)
    # Exemplo: "6.1830-2" -> [("Sex", 1110, 1220)]
    # Exemplo: "3.2020-2 5.2020-2" -> [("Ter", 1220, 1330), ("Qui", 1220, 1330)]
    # Exemplo: "2.0820-1" -> [("Seg", 500, 555)] (1 * 55 min = 55 min)
    pattern = r"([2-7])\.(\d{4})-(\d+)"
    matches = re.findall(pattern, schedule_str)

    parsed_schedules = []
    credit_duration_minutes = 55 # Duração de cada crédito em minutos, conforme informado pelo usuário

    for day, time_str, credits_str in matches:
        try:
            hour = int(time_str[:2])
            minute = int(time_str[2:])
            start_time_minutes = hour * 60 + minute
            credits = int(credits_str)

            # Calcula a duração total em minutos
            duration_minutes = credits * credit_duration_minutes

            # Calcula o horário de término
            end_time_minutes = start_time_minutes + duration_minutes

            # Convertendo dia numérico para string (Seg=2, Ter=3, ..., Sab=7)
            day_map = {"2": "Seg", "3": "Ter", "4": "Qua", "5": "Qui", "6": "Sex", "7": "Sab"}
            day_str = day_map.get(day, "Inválido")

            if day_str != "Inválido":
                parsed_schedules.append({
                    "dia_semana": day_str,
                    "horario_inicio": f"{hour:02d}:{minute:02d}",
                    "horario_fim": f"{(end_time_minutes // 60):02d}:{(end_time_minutes % 60):02d}",
                    "inicio_min": start_time_minutes,
                    "fim_min": end_time_minutes
                })
            else:
                 # Corrigido: Removido \r e simplificado aspas
                 logger.warning(f"Dia da semana inválido '{day}' encontrado em '{schedule_str}'")

        except ValueError as e:
             # Corrigido: Removido \r e simplificado aspas
            logger.warning(f"Erro ao processar horário '{day}.{time_str}-{credits_str}': {e}")
            continue
        except Exception as e:
             # Corrigido: Removido \r e simplificado aspas
             logger.error(f"Erro inesperado ao processar parte do horário '{schedule_str}': {e}")
             continue

    return parsed_schedules

def parse_catalog(file_path):
    """Lê um arquivo de catálogo (Excel ou CSV) e retorna um DataFrame processado."""
    try:
        if file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        elif file_path.endswith(".csv"):
            try:
                df = pd.read_csv(file_path, sep=";")
                if df.shape[1] <= 1:
                    logger.info("CSV lido com ; resultou em poucas colunas, tentando com ,")
                    df = pd.read_csv(file_path, sep=",")
            except Exception as e_csv:
                 logger.error(f"Erro ao ler CSV {file_path} com ; ou ,: {e_csv}")
                 # Tentar detectar encoding
                 try:
                     # Tenta importar chardet. Se não estiver disponível, informa e prossegue sem ele.
                     import chardet
                     with open(file_path, 'rb') as f:
                         result = chardet.detect(f.read())
                     encoding = result['encoding']
                     logger.info(f"Detectado encoding {encoding} para {file_path}, tentando novamente.")
                     # Tenta detectar separador automaticamente com engine python
                     df = pd.read_csv(file_path, sep=None, engine='python', encoding=encoding)
                 except ImportError:
                     logger.warning("Biblioteca chardet não instalada, não foi possível detectar encoding. Tentando com utf-8 e detecção de separador.")
                     try:
                         df = pd.read_csv(file_path, sep=None, engine='python', encoding='utf-8')
                     except Exception as e_utf8:
                         logger.error(f"Falha ao ler CSV {file_path} com utf-8 e detecção de separador: {e_utf8}")
                         raise ValueError("Falha ao ler CSV. Verifique o separador e encoding.")
                 except Exception as e_enc:
                     logger.error(f"Erro ao ler CSV {file_path} mesmo após detectar encoding: {e_enc}")
                     raise ValueError("Falha ao ler CSV. Verifique o formato.")

        else:
            raise ValueError("Formato de arquivo não suportado para catálogo. Use .xlsx ou .csv")

        logger.info(f"Colunas encontradas no catálogo: {df.columns.tolist()}")

        # Mapeamento de colunas com base na explicação do usuário
        column_mapping = {
            "Disciplina": "codigo_disciplina", # Coluna 0
            # "Turma": "turma", # Coluna 1 - Ignorado conforme solicitado
            "Nome da Disciplina": "nome_disciplina", # Coluna 2
            "H.A.": "creditos", # Coluna 3 - Usando H.A como créditos
            "Vagas Ofertadas": "vagas_ofertadas", # Coluna 4
            # "Vagas Ocupadas": "vagas_ocupadas", # Coluna 5 - Ignorado
            # "Alunos Especiais": "alunos_especiais", # Coluna 6 - Ignorado
            "Saldo Vagas": "vagas_disponiveis", # Coluna 7
            # "Pedidos sem vaga": "pedidos_sem_vaga", # Coluna 8 - Ignorado
            "Horários/Locais": "horario_str", # Coluna 9
            # "Professores": "professores", # Coluna 10 - Ignorado
            "Curso": "curso_codigo" # Coluna 11
        }

        # Renomear colunas que existem no DataFrame
        # Converte nomes das colunas do DF para string para evitar erros de tipo misto
        df.columns = df.columns.astype(str)
        actual_mapping = {k: v for k, v in column_mapping.items() if k in df.columns}
        df.rename(columns=actual_mapping, inplace=True)

        # Verificar colunas essenciais após renomear
        required_cols = ["codigo_disciplina", "nome_disciplina", "horario_str", "vagas_disponiveis", "creditos"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            # Tenta mapeamentos alternativos comuns
            alt_mapping = {
                "Código": "codigo_disciplina",
                "Cod. Disciplina": "codigo_disciplina",
                "Nome": "nome_disciplina",
                "Horários": "horario_str",
                "Horário": "horario_str",
                "Créditos": "creditos",
                "Vagas": "vagas_ofertadas",
                "Saldo de Vagas": "vagas_disponiveis",
                "Vagas Disponíveis": "vagas_disponiveis"
            }
            alt_actual_mapping = {k: v for k, v in alt_mapping.items() if k in df.columns and v not in df.columns}
            if alt_actual_mapping:
                logger.warning(f"Usando mapeamentos alternativos: {alt_actual_mapping}")
                df.rename(columns=alt_actual_mapping, inplace=True)
                missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
             raise ValueError(f"Colunas essenciais não encontradas no catálogo após renomear: {missing_cols}. Colunas disponíveis: {df.columns.tolist()}")

        # Processar a string de horário (Coluna 9)
        # Extrai apenas a parte do horário, ignorando o local após " / "
        df["horario_str_parsed"] = df["horario_str"].astype(str).apply(lambda x: x.split(" / ")[0] if isinstance(x, str) and " / " in x else x)
        df["horarios_processados"] = df["horario_str_parsed"].apply(parse_schedule_string)

        # Filtrar linhas onde o horário não pôde ser processado ou está vazio
        df = df[df["horarios_processados"].apply(lambda x: isinstance(x, list) and len(x) > 0)]

        # Converter colunas numéricas, tratando erros
        numeric_cols = ["vagas_disponiveis", "creditos", "vagas_ofertadas"]
        for col in numeric_cols:
            if col in df.columns:
                # Tenta converter para numérico, forçando erros para NaN
                df[col] = pd.to_numeric(df[col], errors="coerce")
                # Remove linhas onde a conversão falhou (resultou em NaN)
                df.dropna(subset=[col], inplace=True)
                # Converte para inteiro APÓS remover NaNs
                df[col] = df[col].astype(int)

        # Adicionar coluna de turma se não existir (para compatibilidade com scheduler_ai)
        if "turma" not in df.columns:
             # Tenta usar a coluna original "Turma" se existir
             if "Turma" in df.columns:
                 df["turma"] = df["Turma"].astype(str)
             else:
                 # Cria um ID de turma baseado no índice se nenhuma coluna de turma for encontrada
                 logger.info("Coluna 'turma' não encontrada, criando ID de turma baseado no índice.")
                 df["turma"] = "T" + df.index.astype(str)

        logger.info(f"Catálogo processado com {len(df)} disciplinas/turmas válidas.")
        return df

    except FileNotFoundError:
        logger.error(f"Erro: Arquivo do catálogo não encontrado em {file_path}")
        return None
    except ValueError as ve:
        logger.error(f"Erro de valor ao processar o catálogo: {ve}")
        return None
    except Exception as e:
        logger.error(f"Erro inesperado ao processar o catálogo {file_path}: {e}", exc_info=True)
        return None

# --- Funções para Histórico e Currículo (Placeholders) ---

def parse_history(file_path):
    """Lê um arquivo de histórico e retorna dados relevantes (ex: disciplinas cursadas)."""
    logger.warning(f"Função parse_history é um placeholder. Extração de PDF/outros formatos não implementada. Recebeu: {file_path}")
    # Retorna uma estrutura vazia ou com dados mínimos esperados pelo scheduler
    return {"disciplinas_cursadas": [], "pre_requisitos_cumpridos": []}

def parse_curriculum(file_path):
    """Lê um arquivo de currículo e retorna a estrutura e pré-requisitos."""
    logger.warning(f"Função parse_curriculum é um placeholder. Extração de PDF/outros formatos não implementada. Recebeu: {file_path}")
    # Retorna uma estrutura vazia ou com dados mínimos esperados pelo scheduler
    return {"estrutura": {}, "pre_requisitos": {}, "equivalencias": {}}

