# -*- coding: utf-8 -*-
"""Módulo para gerenciar o armazenamento temporário dos dados processados."""

import uuid
import logging

logger = logging.getLogger(__name__)

# Usaremos um dicionário em memória para simplicidade.
# Em produção, isso poderia ser substituído por Redis, um banco de dados,
# ou um sistema de cache mais robusto para lidar com múltiplas sessões.
_data_store = {}

def create_session():
    """Cria uma nova sessão e retorna seu ID."""
    session_id = str(uuid.uuid4())
    _data_store[session_id] = {
        'catalog': None,
        'history': None,
        'curriculum': None,
        'preferences': None
    }
    logger.info(f"Nova sessão criada: {session_id}")
    return session_id

def store_data(session_id, data_type, data):
    """Armazena dados processados para uma sessão específica."""
    if session_id not in _data_store:
        logger.error(f"Tentativa de armazenar dados para sessão inexistente: {session_id}")
        return False
    if data_type not in _data_store[session_id]:
        # Corrigido: Removido \r e garantido aspas simples corretas
        logger.error(f"Tipo de dado inválido '{data_type}' para sessão {session_id}")
        return False

    _data_store[session_id][data_type] = data
    # Corrigido: Removido \r e garantido aspas simples corretas
    logger.info(f"Dados do tipo '{data_type}' armazenados para sessão {session_id}")
    return True

def get_data(session_id, data_type):
    """Recupera dados processados para uma sessão específica."""
    if session_id not in _data_store:
        logger.error(f"Tentativa de recuperar dados de sessão inexistente: {session_id}")
        return None
    if data_type not in _data_store[session_id]:
        # Corrigido: Removido \r e garantido aspas simples corretas
        logger.error(f"Tipo de dado inválido '{data_type}' solicitado para sessão {session_id}")
        return None

    return _data_store[session_id].get(data_type)

def get_all_data(session_id):
    """Recupera todos os dados de uma sessão."""
    if session_id not in _data_store:
        logger.error(f"Tentativa de recuperar todos os dados de sessão inexistente: {session_id}")
        return None
    return _data_store[session_id]

def clear_session(session_id):
    """Remove os dados de uma sessão."""
    if session_id in _data_store:
        del _data_store[session_id]
        logger.info(f"Sessão removida: {session_id}")
        return True
    logger.warning(f"Tentativa de remover sessão inexistente: {session_id}")
    return False

