from app.database import mydb

class Produto:
    def __init__(self, id, nome, validade, preco, ean, quantidade, quantidade_min, id_fornecedor, id_categorias):
        self.id = id
        self.nome = nome
        self.validade = validade
        self.preco = preco
        self.ean = ean
        self.quantidade = quantidade
        self.quantidade_min = quantidade_min
        self.id_fornecedor = id_fornecedor
        self.id_categorias = id_categorias

    @staticmethod
    def from_db_row(row):
        return Produto(id=row['id'], nome=row['nome'], validade=row['validade'], preco=row['preco'],
         ean=row['validade'], quantidade=row['quantidade'], quantidade_min=row['quantidade_min'], id_fornecedor=row['id_fornecedor'], id_categorias=row['id_categorias'])

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'validade': self.validade,
            'preco': self.preco,
            'ean': self.ean,
            'quantidade': self.quantidade,
            'id_fornecedor': self.id_fornecedor,
            'id_categorias': self.id_categorias
        }
