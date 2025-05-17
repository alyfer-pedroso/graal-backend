from flask import Blueprint, request, jsonify
from app.controllers.produtos_controller import (
    listar_produtos,
    obter_produto,
    criar_produto,
    atualizar_produto,
    deletar_produto
)
from app.models.mensagens import MensagemErro

produto_bp = Blueprint('produto_bp', __name__, url_prefix='/produto')

@produto_bp.route('/', methods=['GET'])
def listar_produtos():
    try:
        produto = listar_produtos()
        return jsonify(produto), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@produto_bp.route('/<int:id>', methods=['GET'])
def obter_produtos(id):
    try:
        produto= obter_produto(id)
        if produto is None:
            return jsonify(MensagemErro('Produto não encontrado', 404).serialize()), 404
        
        return jsonify(produto), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@produto_bp.route('/', methods=['POST'])
def add_produtos():
    try:
        data = request.get_json()
        if not data:
            return jsonify(MensagemErro('Dados não fornecidos', 400).serialize()), 400

        id = data.get('id')
        nome = data.get('nome')
        validade = data.get('validade')
        preco = data.get('preco')
        ean = data.get('ean')
        quantidade = data.get('quantidade')
        quantidade_min = data.get('quantidade_min')
        id_fornecedor = data.get('id_fornecedor')
        id_categorias = data.get('id_categorias')

        if not id or not nome or not validade or not preco or not ean or not quantidade or not quantidade_min or not id_fornecedor or not id_categorias:
            return jsonify(MensagemErro('Todos os campos são obrigatórios', 400).serialize()), 400
        
        novo_produto = criar_produto(id, nome, validade, preco, ean, quantidade, quantidade_min, id_fornecedor, id_categorias)
        return jsonify(novo_produto), 201
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@produto_bp.route('/<int:id>', methods=['PUT'])
def update_produtos(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify(MensagemErro('Dados não fornecidos', 400).serialize()), 400
        
        id = data.get('id')
        nome = data.get('nome')
        validade = data.get('validade')
        preco = data.get('preco')
        ean = data.get('ean')
        quantidade = data.get('quantidade')
        quantidade_min = data.get('quantidade_min')
        id_fornecedor = data.get('id_fornecedor')
        id_categorias = data.get('id_categorias')
        
        produto_atualizado = atualizar_produto(id, nome, validade, preco, ean, quantidade, quantidade_min, id_fornecedor, id_categorias)
        
        if not produto_atualizado:
            return jsonify(MensagemErro('Produto não encontrado', 404).serialize()), 404

        return jsonify(produto_atualizado), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@produto_bp.route('/<int:id>', methods=['DELETE'])
def delete_produtos(id):
    try:
        if deletar_produto(id):
            return jsonify({'message': 'Produto deletado com sucesso'}), 200
        
        return jsonify(MensagemErro('Produto não encontrado', 404).serialize()), 404
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

