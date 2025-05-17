from flask import Blueprint, request, jsonify
from app.controllers.funcionarios_controller import (
    listar_funcionarios,
    obter_funcionario,
    criar_funcionario,
    atualizar_funcionario,
    deletar_funcionario
)
from app.models.mensagens import MensagemErro

funcionario_bp = Blueprint('funcionario_bp', __name__, url_prefix='/funcionarios')

@funcionario_bp.route('/', methods=['GET'])
def get_funcionarios():
    try:
        funcionarios = listar_funcionarios()
        return jsonify(funcionarios), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@funcionario_bp.route('/<int:id>', methods=['GET'])
def get_funcionario(id):
    try:
        funcionario = obter_funcionario(id)
        if funcionario is None:
            return jsonify(MensagemErro('funcionario não encontrado', 404).serialize()), 404
        
        return jsonify(funcionario), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

@funcionario_bp.route('/', methods=['POST'])
def add_funcionario():
    try:
        data = request.get_json()
        if not data:
            return jsonify(MensagemErro('Dados não fornecidos', 400).serialize()), 400

        nome = data.get('nome')
        telefone = data.get('telefone')
        cpf = data.get('cpf')
        codigo = data.get('codigo')
        usuario = data.get('usuario')
        senha = data.get('senha')
        id_cargo = data.get('id_cargo')

        if not all([nome, telefone, cpf, codigo, usuario, senha, id_cargo]):
            return jsonify(MensagemErro('Todos os campos são obrigatórios', 400).serialize()), 400

        novo_funcionario = criar_funcionario(nome, telefone, cpf, codigo, usuario, senha, id_cargo)
        return jsonify(novo_funcionario), 201
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500


@funcionario_bp.route('/<int:id>', methods=['PUT'])
def update_funcionario(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify(MensagemErro('Dados não fornecidos', 400).serialize()), 400

        nome = data.get('nome')
        telefone = data.get('telefone')
        cpf = data.get('cpf')
        codigo = data.get('codigo')
        usuario = data.get('usuario')
        senha = data.get('senha')
        id_cargo = data.get('id_cargo')

        funcionario_atualizado = atualizar_funcionario(
            id,
            nome=nome,
            telefone=telefone,
            cpf=cpf,
            codigo=codigo,
            usuario=usuario,
            senha=senha,
            id_cargo=id_cargo
        )

        if not funcionario_atualizado:
            return jsonify(MensagemErro('Funcionário não encontrado', 404).serialize()), 404

        return jsonify(funcionario_atualizado), 200
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500


@funcionario_bp.route('/<int:id>', methods=['DELETE'])
def delete_funcionario(id):
    try:
        if deletar_funcionario(id):
            return jsonify({'message': 'funcionario deletado com sucesso'}), 200
        
        return jsonify(MensagemErro('funcionario não encontrado', 404).serialize()), 404
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500

