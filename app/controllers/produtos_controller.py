from app.database import mydb
from app.models import produto as cg, mensagens

def listar_produtos():
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Produto")
        
        produtos = cursor.fetchall()
        return [cg.Produto.from_db_row(produto).serialize() for produto in produtos]
    except Exception as e:
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def obter_produto(id):
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Produto WHERE id = %s", (id,))

        produto = cursor.fetchone()
        return cg.Produto.from_db_row(produto).serialize() if produto else None
    except Exception as e:
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def criar_produto(nome, validade, preco, ean, quantidade, quantidade_min, id_fornecedor, id_categorias):
    try:
        cursor = mydb.cursor()
        cursor.execute(
            "INSERT INTO Produto (nome, validade, preco, ean, quantidade, quantidade_min, id_fornecedor, id_categorias) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (nome, validade, preco, ean, quantidade, quantidade_min, id_fornecedor, id_categorias)
        )
        mydb.commit()
        return obter_produto(cursor.lastrowid)
    except Exception as e:
        mydb.rollback()
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def atualizar_produto(id, nome=None, validade=None, preco=None, ean=None, quantidade=None, quantidade_min=None, id_fornecedor=None, id_categorias=None):
    try:
        cursor = mydb.cursor()
        updates = []
        params = []

        if nome is not None:
            updates.append("nome = %s")
            params.append(nome)
        if validade is not None:
            updates.append("validade = %s")
            params.append(validade)
        if preco is not None:
            updates.append("preco = %s")
            params.append(preco)
        if ean is not None:
            updates.append("ean = %s")
            params.append(ean)
        if quantidade is not None:
            updates.append("quantidade = %s")
            params.append(quantidade)
        if quantidade_min is not None:
            updates.append("quantidade_min = %s")
            params.append(quantidade_min)
        if id_fornecedor is not None:
            updates.append("id_fornecedor = %s")
            params.append(id_fornecedor)
        if id_categorias is not None:
            updates.append("id_categorias = %s")
            params.append(id_categorias)

        if not updates:
            return mensagens.MensagemErro("Nenhum dado para atualizar", 400).serialize()

        query = "UPDATE Produto SET " + ", ".join(updates) + " WHERE id = %s"
        params.append(id)
        cursor.execute(query, tuple(params))

        mydb.commit()
        return obter_produto(id)
    except Exception as e:
        mydb.rollback()
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()


def deletar_produto(id):
    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM Produto WHERE id = %s", (id,))

        mydb.commit()
        return cursor.rowcount == 1
    except Exception as e:
        mydb.rollback()
        return False
    finally:
        cursor.close()

