from flask import Blueprint, request, jsonify
from app.controllers.fornecedores_controller import (
    listar_fornecedores,
    obter_fornecedor,
    criar_fornecedor,
    atualizar_fornecedor,
    deletar_fornecedor
)
from app.models.mensagens import MensagemErro

fornecedor_bp = Blueprint('fornecedor_bp', __name__, url_prefix='/fornecedor')

@fornecedor_bp.route('/', methods=['GET'])
def get_fornecedores():
    try:
        fornecedor = listar_fornecedores()
        return jsonify(fornecedor), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@fornecedor_bp.route('/<int:id>', methods=['GET'])
def get_fornecedor(id):
    try:
        fornecedor = obter_fornecedor(id)
        if fornecedor is None:
            return jsonify(MensagemErro('Fornecedor não encontrado', 404).serialize()), 404
        
        return jsonify(fornecedor), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@fornecedor_bp.route('/', methods=['POST'])
def add_fornecedor():
    try:
        data = request.get_json()
        if not data:
            return jsonify(MensagemErro('Dados não fornecidos', 400).serialize()), 400

        nome = data.get('nome')
        cnpj = data.get('cnpj')

        if not nome or not cnpj:
            return jsonify(MensagemErro('Todos os campos são obrigatórios', 400).serialize()), 400
        
        novo_fornecedor = criar_fornecedor(nome, cnpj)
        return jsonify(novo_fornecedor), 201
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@fornecedor_bp.route('/<int:id>', methods=['PUT'])
def update_fornecedor(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify(MensagemErro('Dados não fornecidos', 400).serialize()), 400
        
        nome = data.get('nome')
        cnpj = data.get('cnpj')
        
        fornecedor_atualizado = atualizar_fornecedor(id, nome, cnpj)
        
        if not fornecedor_atualizado:   
            return jsonify(MensagemErro('Fornecedor não encontrado', 404).serialize()), 404

        return jsonify(fornecedor_atualizado), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@fornecedor_bp.route('/<int:id>', methods=['DELETE'])
def delete_fornecedor(id):
    try:
        if deletar_fornecedor(id):
            return jsonify({'message': 'Fornecedor deletado com sucesso'}), 200
        
        return jsonify(MensagemErro('Fornecedor não encontrado', 404).serialize()), 404
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

