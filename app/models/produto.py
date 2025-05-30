from babel.numbers import format_currency

class Produto:
    def __init__(self, id, nome, validade, preco, EAN, quantidade, quantidade_min, id_fornecedor, id_categoria, categoria, fornecedor):
        self.id = id
        self.nome = nome
        self.validade = validade
        self.preco = preco
        self.EAN = EAN
        self.quantidade = quantidade
        self.quantidade_min = quantidade_min
        self.id_fornecedor = id_fornecedor
        self.id_categoria = id_categoria
        self.categoria = categoria
        self.fornecedor = fornecedor

    @staticmethod
    def from_db_row(row):
        return Produto(id=row['id'],
        nome=row['nome'],
        validade=row['validade'],
        preco=row['preco'],
         EAN=row['EAN'],
         quantidade=row['quantidade'],
         quantidade_min=row['quantidade_min'],
         id_fornecedor=row['id_fornecedor'],
         id_categoria=row['id_categoria'],
         categoria=row['categoria'],
         fornecedor=row['fornecedor']
         )

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'validade': self.validade,
            'preco': format_currency(self.preco, 'BRL', locale='pt_BR'),
            'EAN': self.EAN,
            'quantidade': self.quantidade,
            'id_fornecedor': self.id_fornecedor,
            'id_categoria': self.id_categoria,
            'categoria': self.categoria,
            'fornecedor': self.fornecedor,
            'quantidade_min': self.quantidade_min
        }
