import random
from app.database import mydb
from app.models import funcionario as cg, mensagens

def listar_funcionarios():
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Funcionario")
        
        funcionarios = cursor.fetchall()
        return [cg.Funcionario.from_db_row(funcionario).serialize() for funcionario in funcionarios]
    except Exception as e:
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def obter_funcionario(id):
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Funcionario WHERE id = %s", (id,))

        funcionario = cursor.fetchone()
        return cg.Funcionario.from_db_row(funcionario).serialize() if funcionario else None
    except Exception as e:
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def criar_funcionario(nome, telefone, cpf, usuario, senha, id_cargo, codigo_validacao):
    try:
        cursor = mydb.cursor()

        if not validar_codigo(codigo_validacao):
            return mensagens.MensagemErro('Código de validação inválido', 400).serialize()

        codigo = gerar_codigo_funcionario()
        cursor.execute(
            "INSERT INTO Funcionario (nome, telefone, cpf, usuario, senha, codigo, id_cargo) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (nome, telefone, cpf, usuario, senha, codigo, id_cargo)
        )

        mydb.commit()
        return obter_funcionario(cursor.lastrowid)
    except Exception as e:
        mydb.rollback()
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def atualizar_funcionario(id, nome=None, telefone=None, cpf=None, usuario=None, senha=None, id_cargo=None):
    try:
        cursor = mydb.cursor()
        updates = []
        params = []

        if nome:
            updates.append("nome = %s")
            params.append(nome)
        if telefone:
            updates.append("telefone = %s")
            params.append(telefone)
        if cpf:
            updates.append("cpf = %s")
            params.append(cpf)
        if usuario:
            updates.append("usuario = %s")
            params.append(usuario)
        if senha:
            updates.append("senha = %s")
            params.append(senha)
        if id_cargo:
            updates.append("id_cargo = %s")
            params.append(id_cargo)

        if not updates:
            return mensagens.MensagemErro("Nenhum dado para atualizar", 400).serialize()

        query = "UPDATE Funcionario SET " + ", ".join(updates) + " WHERE id = %s"
        params.append(id)
        cursor.execute(query, tuple(params))

        mydb.commit()
        return obter_funcionario(id)
    except Exception as e:
        mydb.rollback()
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()


def deletar_funcionario(id):
    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM Funcionario WHERE id = %s", (id,))

        mydb.commit()
        return cursor.rowcount == 1
    except Exception as e:
        mydb.rollback()
        return False
    finally:
        cursor.close()

def login_funcionario(usuario, senha):
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Funcionario WHERE usuario = %s AND senha = %s", (usuario, senha))

        funcionario = cursor.fetchone()
        return cg.Funcionario.from_db_row(funcionario).serialize() if funcionario else None
    except Exception as e:
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def gerar_codigo_funcionario():
    cursor = mydb.cursor()

    try:
        min_11_digit = 10**10
        max_11_digit = 10**11 - 1

        while True:
            codigo = random.randint(min_11_digit, max_11_digit)
            cursor.execute("SELECT id FROM Funcionario WHERE codigo = %s", (codigo,))
            
            if cursor.fetchone() is None:
                return codigo
    finally:
        cursor.close()

def validar_codigo(codigo):
    cursor = mydb.cursor()

    try:
        cursor.execute("""
            SELECT c.hierarquia 
            FROM Funcionario f 
            JOIN Cargo c ON f.id_cargo = c.id 
            WHERE f.codigo = %s
        """, (codigo,))

        result = cursor.fetchone()
        return result[0] > 1 if result else False
    finally:
        cursor.close()
