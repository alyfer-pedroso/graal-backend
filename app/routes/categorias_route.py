from flask import Blueprint, request, jsonify
from app.controllers.categorias_controller import (
    listar_categorias,
    obter_categorias,
    criar_categoria,
    atualizar_categoria,
    deletar_categoria
)
from app.models.mensagens import MensagemErro

categoria_bp = Blueprint('categoria_bp', __name__, url_prefix='/categorias')

@categoria_bp.route('/', methods=['GET'])
def listar_todas_categorias():
    try:
        categorias = listar_categorias()
        return jsonify(categorias), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@categoria_bp.route('/<int:id>', methods=['GET'])
def obter_categoria_por_id(id):
    try:
        categoria = obter_categorias(id)
        if categoria is None:
            return jsonify(MensagemErro('Categoria não encontrada', 404).serialize()), 404
        
        return jsonify(categoria), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@categoria_bp.route('/', methods=['POST'])
def add_categorias():
    try:
        data = request.get_json()
        if not data:
            return jsonify(MensagemErro('Dados não fornecidos', 400).serialize()), 400

        id = data.get('id')
        nome = data.get('nome')

        if not id or not nome:
            return jsonify(MensagemErro('Todos os campos são obrigatórios', 400).serialize()), 400
        
        nova_categoria = criar_categoria(id, nome)
        return jsonify(nova_categoria), 201
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@categoria_bp.route('/<int:id>', methods=['PUT'])
def update_categorias(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify(MensagemErro('Dados não fornecidos', 400).serialize()), 400
        
        id = data.get('id')
        nome = data.get('nome')
        
        categoria_atualizado = atualizar_categoria(id, nome)
        
        if not categoria_atualizado:
            return jsonify(MensagemErro('Categoria não encontrado', 404).serialize()), 404

        return jsonify(categoria_atualizado), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@categoria_bp.route('/<int:id>', methods=['DELETE'])
def delete_categoria(id):
    try:
        if deletar_categoria(id):
            return jsonify({'message': 'Categoria deletada com sucesso'}), 200
        
        return jsonify(MensagemErro('Categoria não encontrada', 404).serialize()), 404
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

