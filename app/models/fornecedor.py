from app.database import mydb

class Fornecedor:
    def __init__(self, id, nome, cnpj):
        self.id = id
        self.nome = nome
        self.cnpj = cnpj
        

    @staticmethod
    def from_db_row(row):
        return Fornecedor(id=row['id'], nome=row['nome'], cnpj=row['cnpj'])

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cnpj': self.cnpj
        }
