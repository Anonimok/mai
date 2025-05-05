# -*- coding: utf-8 -*-
import os
import sys
import logging
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS # Import CORS

# Importar os novos blueprints
from src.routes.upload_routes import upload_bp
from src.routes.schedule_routes import schedule_bp

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder=None) # Remover static_folder daqui, será tratado separadamente
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev_secret_key_change_me') # Usar variável de ambiente ou default seguro

# Habilitar CORS para todas as origens em todas as rotas
# Em produção, restrinja a origem ao domínio do seu frontend: CORS(app, origins=["http://localhost:3000", "https://seu-dominio.com"])
CORS(app)

# Registrar os blueprints
app.register_blueprint(upload_bp, url_prefix='/api')
app.register_blueprint(schedule_bp, url_prefix='/api/schedule')

# Remover configuração de banco de dados e rotas estáticas padrão do template
# A rota estática será tratada pelo servidor de frontend (React) ou um servidor web como Nginx em produção.
# A rota raiz pode ser usada para um simples health check.

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint simples para verificar se a API está rodando."""
    logger.info("Health check solicitado.")
    return jsonify({"status": "ok"}), 200

# Remover a rota serve(path) padrão, pois o frontend React cuidará disso.

if __name__ == '__main__':
    # O host 0.0.0.0 é necessário para acessibilidade externa (inclusive do frontend rodando localmente)
    # O debug=True é útil para desenvolvimento, mas deve ser False em produção.
    logger.info("Iniciando servidor Flask...")
    app.run(host='0.0.0.0', port=5000, debug=True)

