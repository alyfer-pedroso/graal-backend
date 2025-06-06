from app.database import mydb

class Venda:
    def __init__(self, id, total, data_venda, id_funcionario):
        self.id = id
        self.total = total
        self.data_venda = data_venda
        self.id_funcionario = id_funcionario

    @staticmethod
    def from_db_row(row):
        return Venda(id=row['id'], total=row['total'], data_venda=row['data_venda'], id_funcionario=row['id_funcionario'])

    def serialize(self):
        return {
            'id': self.id,
            'total': self.total,
            'data_venda': self.data_venda,
            'id_funcionario': self.id_funcionario,
        }
