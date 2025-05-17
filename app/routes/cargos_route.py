from flask import Blueprint, request, jsonify
from app.controllers.cargos_controller import (
    listar_cargos,
    obter_cargo,
    criar_cargo,
    atualizar_cargo,
    deletar_cargo
)
from app.models.mensagens import MensagemErro

cargo_bp = Blueprint('cargo_bp', __name__, url_prefix='/cargos')

@cargo_bp.route('/', methods=['GET'])
def get_cargos():
    try:
        cargos = listar_cargos()
        return jsonify(cargos), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@cargo_bp.route('/<int:id>', methods=['GET'])
def get_cargo(id):
    try:
        cargo = obter_cargo(id)
        if cargo is None:
            return jsonify(MensagemErro('Cargo não encontrado', 404).serialize()), 404
        
        return jsonify(cargo), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@cargo_bp.route('/', methods=['POST'])
def add_cargo():
    try:
        data = request.get_json()
        if not data:
            return jsonify(MensagemErro('Dados não fornecidos', 400).serialize()), 400

        nome = data.get('nome')
        hierarquia = data.get('hierarquia')

        if not nome or not hierarquia:
            return jsonify(MensagemErro('Todos os campos são obrigatórios', 400).serialize()), 400
        
        novo_cargo = criar_cargo(nome, hierarquia)
        return jsonify(novo_cargo), 201
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@cargo_bp.route('/<int:id>', methods=['PUT'])
def update_cargo(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify(MensagemErro('Dados não fornecidos', 400).serialize()), 400
        
        nome = data.get('nome')
        hierarquia = data.get('hierarquia')
        
        cargo_atualizado = atualizar_cargo(id, nome, hierarquia)
        
        if not cargo_atualizado:
            return jsonify(MensagemErro('Cargo não encontrado', 404).serialize()), 404

        return jsonify(cargo_atualizado), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@cargo_bp.route('/<int:id>', methods=['DELETE'])
def delete_cargo(id):
    try:
        if deletar_cargo(id):
            return jsonify({'message': 'Cargo deletado com sucesso'}), 200
        
        return jsonify(MensagemErro('Cargo não encontrado', 404).serialize()), 404
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

