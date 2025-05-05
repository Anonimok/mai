# -*- coding: utf-8 -*-
"""Rotas da API para gerenciar preferências e gerar a grade horária."""

import logging
import pandas as pd
from flask import Blueprint, request, jsonify
from src.modules import data_manager, scheduler_ai

schedule_bp = Blueprint("schedule_bp", __name__)
logger = logging.getLogger(__name__)

@schedule_bp.route("/preferences", methods=["POST"])
def update_preferences():
    """Recebe e armazena as preferências do usuário para uma sessão."""
    session_id = request.json.get("session_id")
    preferences = request.json.get("preferences")

    if not session_id:
        return jsonify({"error": "ID da sessão não fornecido."}), 400
    if not preferences or not isinstance(preferences, dict):
        return jsonify({"error": "Preferências inválidas ou não fornecidas."}), 400

    # Validação básica das preferências (pode ser expandida)
    required_prefs = ["min_creditos", "max_creditos"]
    if not all(key in preferences for key in required_prefs):
        return jsonify({"error": f"Preferências obrigatórias ausentes: {required_prefs}"}), 400

    if data_manager.store_data(session_id, "preferences", preferences):
        logger.info(f"Preferências armazenadas para sessão {session_id}")
        return jsonify({"message": "Preferências atualizadas com sucesso.", "session_id": session_id}), 200
    else:
        return jsonify({"error": "Falha ao armazenar preferências na sessão."}), 500

@schedule_bp.route("/generate", methods=["POST"])
def generate_schedule_route():
    """Gera a grade horária com base nos dados e preferências da sessão."""
    session_id = request.json.get("session_id")
    if not session_id:
        return jsonify({"error": "ID da sessão não fornecido."}), 400

    # Recuperar todos os dados da sessão
    session_data = data_manager.get_all_data(session_id)
    if not session_data:
        return jsonify({"error": "Sessão não encontrada ou vazia."}), 404

    catalog_data = session_data.get("catalog")
    history_data = session_data.get("history")
    curriculum_data = session_data.get("curriculum")
    preferences = session_data.get("preferences")

    # Verificar se todos os dados necessários estão presentes
    if not catalog_data:
        return jsonify({"error": "Dados do catálogo não encontrados na sessão."}), 400
    if not history_data:
        # Usar dados padrão se não houver histórico (parser ainda é placeholder)
        history_data = {"disciplinas_cursadas": [], "pre_requisitos_cumpridos": []}
        logger.warning(f"Dados de histórico não encontrados para sessão {session_id}, usando padrão.")
    if not curriculum_data:
        # Usar dados padrão se não houver currículo (parser ainda é placeholder)
        curriculum_data = {"estrutura": {}, "pre_requisitos": {}, "equivalencias": {}}
        logger.warning(f"Dados de currículo não encontrados para sessão {session_id}, usando padrão.")
    if not preferences:
        return jsonify({"error": "Preferências do usuário não encontradas na sessão."}), 400

    try:
        # Converter catálogo de volta para DataFrame se foi armazenado como dict
        if isinstance(catalog_data, list):
            catalog_df = pd.DataFrame(catalog_data)
        elif isinstance(catalog_data, pd.DataFrame):
            catalog_df = catalog_data
        else:
             return jsonify({"error": "Formato de dados do catálogo inválido na sessão."}), 500

        logger.info(f"Iniciando geração de grade para sessão {session_id}...")
        solutions = scheduler_ai.generate_schedule(
            catalog_df=catalog_df,
            history_data=history_data,
            curriculum_data=curriculum_data,
            preferences=preferences
        )
        logger.info(f"Geração concluída para sessão {session_id}. Encontradas {len(solutions)} soluções.")

        if solutions is None: # Indica erro interno no gerador
             return jsonify({"error": "Falha interna ao gerar a grade horária."}), 500

        # Retorna as soluções encontradas (o gerador já retorna as top N)
        return jsonify({"solutions": solutions, "session_id": session_id}), 200

    except Exception as e:
        logger.error(f"Erro ao gerar grade para sessão {session_id}: {e}", exc_info=True)
        return jsonify({"error": "Ocorreu um erro interno no servidor durante a geração da grade."}), 500

