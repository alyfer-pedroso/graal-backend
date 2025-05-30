from app.database import mydb

class Item:
    def __init__(self, id, quantidade, id_venda, id_produto):
        self.id = id
        self.quantidade = quantidade
        self.id_venda = id_venda
        self.id_produto = id_produto

    @staticmethod
    def from_db_row(row):
        return Item(id=row['id'], quantidade=row['quantidade'], id_venda=row['id_venda'], id_produto=row['id_produto'])

    def serialize(self):
        return {
            'id': self.id,
            'quantidade': self.quantidade,
            'id_venda': self.id_venda,
            'id_produto': self.id_produto
        }
