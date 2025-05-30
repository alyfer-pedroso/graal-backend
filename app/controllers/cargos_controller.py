from app.database import mydb
from app.models import cargo as cg, mensagens

def listar_cargos():
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Cargo")
        
        cargos = cursor.fetchall()
        return [cg.Cargo.from_db_row(cargo).serialize() for cargo in cargos]
    except Exception as e:
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def obter_cargo(id):
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Cargo WHERE id = %s", (id,))

        cargo = cursor.fetchone()
        return cg.Cargo.from_db_row(cargo).serialize() if cargo else None
    except Exception as e:
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def criar_cargo(nome, hierarquia):
    try:
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO Cargo (nome, hierarquia) VALUES (%s, %s)", (nome, hierarquia))

        mydb.commit()
        return obter_cargo(cursor.lastrowid)
    except Exception as e:
        mydb.rollback()
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def atualizar_cargo(id, nome=None, hierarquia=None):
    try:
        cursor = mydb.cursor()
        updates = []

        if nome:
            updates.append("nome = %s")
        if hierarquia:
            updates.append("hierarquia = %s")
        if not updates:
            return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
        
        query = "UPDATE Cargo SET " + ", ".join(updates) + " WHERE id = %s"
        params = tuple([nome, hierarquia][i] for i, _ in enumerate(updates)) + (id,)
        cursor.execute(query, params)

        mydb.commit()
        return obter_cargo(id)
    except Exception as e:
        mydb.rollback()
        return mensagens.MensagemErro(e.args[1], e.args[0]).serialize()
    finally:
        cursor.close()

def deletar_cargo(id):
    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM Cargo WHERE id = %s", (id,))

        mydb.commit()
        return cursor.rowcount == 1
    except Exception as e:
        mydb.rollback()
        return False
    finally:
        cursor.close()

