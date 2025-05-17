from app.database import mydb
from app.models import item as cg, mensagens

def listar_itens():
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Item")
        
        itens = cursor.fetchall()
        return [cg.Item.from_db_row(item).serialize() for item in itens]
    except Exception as e:
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def obter_item(id):
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Item WHERE id = %s", (id,))

        item = cursor.fetchone()
        return cg.Item.from_db_row(item).serialize() if item else None
    except Exception as e:
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def criar_item(quantidade, id_venda, id_produto):
    try:
        cursor = mydb.cursor()
        cursor.execute(
            "INSERT INTO Item (quantidade, id_venda, id_produto) VALUES (%s, %s, %s)",
            (quantidade, id_venda, id_produto)
        )
        mydb.commit()
        return obter_item(cursor.lastrowid)
    except Exception as e:
        mydb.rollback()
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def atualizar_item(id, quantidade=None, id_venda=None, id_produto=None):
    try:
        cursor = mydb.cursor()
        updates = []
        params = []

        if quantidade is not None:
            updates.append("quantidade = %s")
            params.append(quantidade)
        if id_venda is not None:
            updates.append("id_venda = %s")
            params.append(id_venda)
        if id_produto is not None:
            updates.append("id_produto = %s")
            params.append(id_produto)

        if not updates:
            return mensagens.MensagemErro("Nenhum dado para atualizar", 400).serialize()

        query = "UPDATE Item SET " + ", ".join(updates) + " WHERE id = %s"
        params.append(id)
        cursor.execute(query, tuple(params))

        mydb.commit()
        return obter_item(id)
    except Exception as e:
        mydb.rollback()
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()


def deletar_item(id):
    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM Item WHERE id = %s", (id,))

        mydb.commit()
        return cursor.rowcount == 1
    except Exception as e:
        mydb.rollback()
        return False
    finally:
        cursor.close()

