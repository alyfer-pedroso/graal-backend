from app.database import mydb

class Cargo:
    def __init__(self, id, nome, hierarquia):
        self.id = id
        self.nome = nome
        self.hierarquia = hierarquia

    @staticmethod
    def from_db_row(row):
        return Cargo(id=row['id'], nome=row['nome'], hierarquia=row['hierarquia'])

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'hierarquia': self.hierarquia
        }

