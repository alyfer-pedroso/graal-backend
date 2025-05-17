from flask import Blueprint, request, jsonify
from app.controllers.itens_controller import (
    listar_itens,
    obter_itens,
    criar_itens,
    atualizar_itens,
    deletar_itens
)
from app.models.mensagens import MensagemErro

item_bp = Blueprint('item_bp', __name__, url_prefix='/itens')

@item_bp.route('/', methods=['GET'])
def get_itens():
    try:
        itens = listar_itens()
        return jsonify(itens), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@item_bp.route('/<int:id>', methods=['GET'])
def get_itens(id):
    try:
        itens = obter_itens(id)
        if itens is None:
            return jsonify(MensagemErro('Item não encontrado', 404).serialize()), 404
        
        return jsonify(itens), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@item_bp.route('/', methods=['POST'])
def add_itens():
    try:
        data = request.get_json()
        if not data:
            return jsonify(MensagemErro('Dados não fornecidos', 400).serialize()), 400

        id = data.get('id')
        quantidade = data.get('quantidade')
        id_venda = data.get('id_venda')
        id_produto = data.get('id_produto')

        if not id or not quantidade or not id_venda or not id_produto:
            return jsonify(MensagemErro('Todos os campos são obrigatórios', 400).serialize()), 400
        
        novo_item = criar_itens(id, quantidade, id_venda, id_produto)
        return jsonify(novo_item), 201
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@item_bp.route('/<int:id>', methods=['PUT'])
def update_itens(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify(MensagemErro('Dados não fornecidos', 400).serialize()), 400
        
        id = data.get('id')
        quantidade = data.get('quantidade')
        id_venda = data.get('id_venda')
        id_produto = data.get('id_produto')
        
        item_atualizado = atualizar_itens(id, quantidade, id_venda, id_produto)
        
        if not item_atualizado:
            return jsonify(MensagemErro('Item não encontrado', 404).serialize()), 404

        return jsonify(item_atualizado), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@item_bp.route('/<int:id>', methods=['DELETE'])
def delete_itens(id):
    try:
        if deletar_itens(id):
            return jsonify({'message': 'Item deletado com sucesso'}), 200
        
        return jsonify(MensagemErro('Item não encontrado', 404).serialize()), 404
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

