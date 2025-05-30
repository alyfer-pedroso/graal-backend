from flask import Blueprint, request, jsonify
from app.controllers.funcionarios_controller import (
    listar_funcionarios,
    obter_funcionario,
    criar_funcionario,
    atualizar_funcionario,
    deletar_funcionario,
    login_funcionario,
    validar_codigo
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
            return jsonify(MensagemErro('Funcionário nao encontrado', 404).serialize()), 404
        
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
        usuario = data.get('usuario')
        senha = data.get('senha')
        id_cargo = data.get('id_cargo')
        codigo_validacao = data.get('codigo_validacao')

        if not all([nome, telefone, cpf, usuario, senha, id_cargo, codigo_validacao]):
            return jsonify(MensagemErro('Todos os campos são obrigatórios', 400).serialize()), 400
        
        if not validar_codigo(codigo_validacao):
            return jsonify(MensagemErro('Código de validação inválido', 400).serialize()), 400

        novo_funcionario = criar_funcionario(nome, telefone, cpf, usuario, senha, id_cargo)
        return jsonify(novo_funcionario), 201
    except Exception as e:
        return jsonify(MensagemErro(e.args[1], e.args[0]).serialize()), 500
    
@funcionario_bp.route('/login', methods=['POST'])
def autenticar_funcionario():
    try:
        data = request.get_json()
        if not data:
            return jsonify(MensagemErro('Dados não fornecidos', 400).serialize()), 400

        usuario = data.get('usuario')
        senha = data.get('senha')

        if not all([usuario, senha]):
            return jsonify(MensagemErro('Todos os campos são obrigatórios', 400).serialize()), 400

        funcionario_logado = login_funcionario(usuario, senha)

        if not funcionario_logado:
            return jsonify(MensagemErro('Funcionário nao encontrado', 404).serialize()), 404
        
        return jsonify(funcionario_logado), 200
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

