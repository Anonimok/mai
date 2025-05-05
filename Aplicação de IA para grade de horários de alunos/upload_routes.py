# -*- coding: utf-8 -*-
"""Rotas da API para upload de arquivos."""

import os
import logging
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from src.modules import data_parser, data_manager

# Configuração do diretório de uploads temporários
UPLOAD_FOLDER = '/tmp/grade_uploads'
ALLOWED_EXTENSIONS = {"xlsx", "csv", "pdf"} # Adicionado PDF, embora o parser não esteja completo

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

upload_bp = Blueprint('upload_bp', __name__)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload/<data_type>', methods=['POST'])
def upload_file(data_type):
    """Recebe upload de arquivo (catalog, history, curriculum)."""
    session_id = request.form.get('session_id')
    if not session_id:
        return jsonify({"error": "ID da sessão não fornecido."}), 400

    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nome de arquivo vazio."}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, f"{session_id}_{data_type}_{filename}")

        try:
            file.save(file_path)
            logger.info(f"Arquivo {filename} salvo em {file_path} para sessão {session_id}")

            # Processar o arquivo
            processed_data = None
            if data_type == 'catalog':
                processed_data = data_parser.parse_catalog(file_path)
                if processed_data is None:
                     return jsonify({"error": "Falha ao processar o arquivo do catálogo."}), 500
                 # Converter DataFrame para dict para armazenamento JSON compatível
                processed_data = processed_data.to_dict(orient='records')
            elif data_type == 'history':
                # A função parse_history atualmente retorna um placeholder
                processed_data = data_parser.parse_history(file_path)
            elif data_type == 'curriculum':
                # A função parse_curriculum atualmente retorna um placeholder
                processed_data = data_parser.parse_curriculum(file_path)
            else:
                os.remove(file_path) # Remove arquivo não processado
                return jsonify({"error": "Tipo de dado inválido."}), 400

            # Armazenar dados processados na sessão
            if not data_manager.store_data(session_id, data_type, processed_data):
                # Tenta remover o arquivo se o armazenamento falhar
                try:
                    os.remove(file_path)
                except OSError as e:
                    logger.error(f"Erro ao remover arquivo temporário {file_path}: {e}")
                return jsonify({"error": "Falha ao armazenar dados na sessão."}), 500

            # Limpeza opcional do arquivo após processamento bem-sucedido
            # Deixe comentado se precisar do arquivo original para depuração
            # try:
            #     os.remove(file_path)
            # except OSError as e:
            #     logger.warning(f"Não foi possível remover o arquivo temporário {file_path}: {e}")

            return jsonify({"message": f"Arquivo {data_type} recebido e processado com sucesso.", "session_id": session_id}), 200

        except Exception as e:
            logger.error(f"Erro ao salvar ou processar o arquivo {filename} para sessão {session_id}: {e}", exc_info=True)
            # Tenta remover o arquivo em caso de erro
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError as os_err:
                    logger.error(f"Erro ao remover arquivo temporário {file_path} após falha: {os_err}")
            return jsonify({"error": "Ocorreu um erro interno no servidor."}), 500
    else:
        return jsonify({"error": "Tipo de arquivo não permitido."}), 400

@upload_bp.route('/session', methods=['POST'])
def create_new_session():
    """Cria uma nova sessão de usuário."""
    session_id = data_manager.create_session()
    if session_id:
        return jsonify({"session_id": session_id}), 201
    else:
        return jsonify({"error": "Falha ao criar sessão."}), 500

