from app.database import mydb
from app.models import categoria as cg, mensagens

def listar_categorias():
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Categoria")
        
        categorias = cursor.fetchall()
        return [cg.Categoria.from_db_row(categoria).serialize() for categoria in categorias]
    except Exception as e:
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def obter_categoria(id):
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Categoria WHERE id = %s", (id,))

        categoria = cursor.fetchone()
        return cg.Categoria.from_db_row(categoria).serialize() if categoria else None
    except Exception as e:
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def criar_categoria(nome):
    try:
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO Categoria (nome) VALUES (%s)", (nome,))

        mydb.commit()
        return obter_categoria(cursor.lastrowid)
    except Exception as e:
        mydb.rollback()
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def atualizar_categoria(id, nome=None):
    try:
        cursor = mydb.cursor()
        updates = []
        params = []

        if nome is not None:
            updates.append("nome = %s")
            params.append(nome)

        if not updates:
            return mensagens.MensagemErro("Nenhum dado para atualizar", 400).serialize()
        
        query = "UPDATE Categoria SET " + ", ".join(updates) + " WHERE id = %s"
        params.append(id)
        cursor.execute(query, tuple(params))

        mydb.commit()
        return obter_categoria(id)
    except Exception as e:
        mydb.rollback()
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def deletar_categoria(id):
    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM Categoria WHERE id = %s", (id,))

        mydb.commit()
        return cursor.rowcount == 1
    except Exception as e:
        mydb.rollback()
        return False
    finally:
        cursor.close()

