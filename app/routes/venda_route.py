from flask import Blueprint, request, jsonify
from app.controllers.vendas_controller import (
    listar_vendas,
    obter_venda,
    criar_venda,
    atualizar_venda,
    deletar_venda
)
from app.controllers.itens_controller import (criar_item)
from app.models.mensagens import MensagemErro

venda_bp = Blueprint('venda_bp', __name__, url_prefix='/venda')

@venda_bp.route('/', methods=['GET'])
def listar_vendas():
    try:
        vendas = listar_vendas()
        return jsonify(vendas), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@venda_bp.route('/<int:id>', methods=['GET'])
def obter_vendas(id):
    try:
        vendas = obter_venda(id)
        if vendas is None:
            return jsonify(MensagemErro('Venda não encontrada', 404).serialize()), 404
        
        return jsonify(vendas), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@venda_bp.route('/', methods=['POST'])
def add_vendas():
    try:
        data = request.get_json()
        if not data:
            return jsonify(MensagemErro('Dados não fornecidos', 400).serialize()), 400

        total = data.get('total')
        id_funcionario = data.get('id_funcionario')
        produtos = data.get('produtos')

        if  not total or not id_funcionario or not produtos:
            return jsonify(MensagemErro('Todos os campos são obrigatórios', 400).serialize()), 400
        
        nova_venda = criar_venda(total, id_funcionario)
        
        if not nova_venda:
            return jsonify(MensagemErro('Erro ao criar venda', 500).serialize()), 500
        
        for produto in produtos:
            id_produto = produto.get('id_produto')
            quantidade = produto.get('quantidade')

            if not id_produto or not quantidade:
                return jsonify(MensagemErro('Todos os campos são obrigatórios', 400).serialize()), 400
            
            criar_item(quantidade, nova_venda['id'], id_produto, )
        
        return jsonify(nova_venda), 201
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@venda_bp.route('/<int:id>', methods=['PUT'])
def update_vendas(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify(MensagemErro('Dados não fornecidos', 400).serialize()), 400
        
        id = data.get('id')
        total = data.get('total')
        data_venda = data.get('data_venda')
        id_funcionario = data.get('id_funcionario')
        
        venda_atualizada = atualizar_venda(id, total, data_venda, id_funcionario)
        
        if not venda_atualizada:
            return jsonify(MensagemErro('Venda não encontrada', 404).serialize()), 404

        return jsonify(venda_atualizada), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@venda_bp.route('/<int:id>', methods=['DELETE'])
def delete_vendas(id):
    try:
        if deletar_venda(id):
            return jsonify({'message': 'Venda deletada com sucesso'}), 200
        
        return jsonify(MensagemErro('Venda não encontrada', 404).serialize()), 404
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

