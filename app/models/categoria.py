from app.database import mydb

class Categoria:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome
        
    @staticmethod
    def from_db_row(row):
        return Categoria(id=row['id'], nome=row['nome'])

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
        }
