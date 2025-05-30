from app.database import mydb
from app.models import fornecedor as cg, mensagens

def listar_fornecedores():
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Fornecedor")
        
        fornecedores = cursor.fetchall()
        return [cg.Fornecedor.from_db_row(fornecedor).serialize() for fornecedor in fornecedores]
    except Exception as e:
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def obter_fornecedor(id):
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Fornecedor WHERE id = %s", (id,))

        fornecedor = cursor.fetchone()
        return cg.Fornecedor.from_db_row(fornecedor).serialize() if fornecedor else None
    except Exception as e:
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def criar_fornecedor(nome, cnpj):
    try:
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO Fornecedor (nome, cnpj) VALUES (%s, %s)", (nome, cnpj))

        mydb.commit()
        return obter_fornecedor(cursor.lastrowid)
    except Exception as e:
        mydb.rollback()
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def atualizar_fornecedor(id, nome=None, cnpj=None):
    try:
        cursor = mydb.cursor()
        updates = []
        params = []

        if nome is not None:
            updates.append("nome = %s")
            params.append(nome)
        if cnpj is not None:
            updates.append("cnpj = %s")
            params.append(cnpj)

        if not updates:
            return mensagens.MensagemErro("Nenhum dado para atualizar", 400).serialize()
        
        query = "UPDATE Fornecedor SET " + ", ".join(updates) + " WHERE id = %s"
        params.append(id)
        cursor.execute(query, tuple(params))

        mydb.commit()
        return obter_fornecedor(id)
    except Exception as e:
        mydb.rollback()
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def deletar_fornecedor(id):
    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM Fornecedor WHERE id = %s", (id,))

        mydb.commit()
        return cursor.rowcount == 1
    except Exception as e:
        mydb.rollback()
        return False
    finally:
        cursor.close()

