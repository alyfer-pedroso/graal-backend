from app.database import mydb
from app.models import venda as cg, mensagens
import json

def listar_todas_vendas():
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                v.id as venda_id,
                (SELECT nome FROM Funcionario WHERE id = v.id_funcionario) as nome_funcionario,
                v.total,
                v.data_venda,
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'nome', p.nome,
                        'quantidade_comprada', i.quantidade,
                        'preco_unidade', p.preco
                    )
                ) as items
            FROM Venda v
            LEFT JOIN Item i ON v.id = i.id_venda
            LEFT JOIN Produto p ON i.id_produto = p.id
            GROUP BY v.id, v.id_funcionario, v.total, v.data_venda
            ORDER BY v.id
        """)
        
        vendas = cursor.fetchall()
        for venda in vendas:
            venda['items'] = json.loads(venda['items'])
        return vendas
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

def criar_venda(total, id_funcionario):
    try:
        cursor = mydb.cursor()
        cursor.execute(
            "INSERT INTO Venda (total, id_funcionario) VALUES (%s, %s)",
            (total, id_funcionario)
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

