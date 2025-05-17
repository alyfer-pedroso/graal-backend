from app.database import mydb
from app.models import venda as cg, mensagens

def listar_vendas():
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Venda")
        
        vendas = cursor.fetchall()
        return [cg.Venda.from_db_row(venda).serialize() for venda in vendas]
    except Exception as e:
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def obter_venda(id):
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Venda WHERE id = %s", (id,))

        venda = cursor.fetchone()
        return cg.Venda.from_db_row(venda).serialize() if venda else None
    except Exception as e:
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def criar_venda(total, data_venda, id_funcionario):
    try:
        cursor = mydb.cursor()
        cursor.execute(
            "INSERT INTO Venda (total, data_venda, id_funcionario) VALUES (%s, %s, %s)",
            (total, data_venda, id_funcionario)
        )
        mydb.commit()
        return obter_venda(cursor.lastrowid)
    except Exception as e:
        mydb.rollback()
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def atualizar_venda(id, total=None, data_venda=None, id_funcionario=None):
    try:
        cursor = mydb.cursor()
        updates = []
        params = []

        if total:
            updates.append("total = %s")
            params.append(total)
        if data_venda:
            updates.append("data_venda = %s")
            params.append(data_venda)
        if id_funcionario:
            updates.append("id_funcionario = %s")
            params.append(id_funcionario)

        if not updates:
            return mensagens.MensagemErro("Nenhum dado para atualizar", 400).serialize()

        query = "UPDATE Funcionario SET " + ", ".join(updates) + " WHERE id = %s"
        params.append(id)
        cursor.execute(query, tuple(params))

        mydb.commit()
        return obter_venda(id)
    except Exception as e:
        mydb.rollback()
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()


def deletar_venda(id):
    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM Venda WHERE id = %s", (id,))

        mydb.commit()
        return cursor.rowcount == 1
    except Exception as e:
        mydb.rollback()
        return False
    finally:
        cursor.close()

