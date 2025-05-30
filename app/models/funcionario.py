from app.database import mydb

class Funcionario:
    def __init___(self, id, nome, telefone, cpf, codigo, usuario, senha, id_cargo):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.codigo = codigo
        self.usuario = usuario
        self.senha = senha
        self.id_cargo = id_cargo

    @staticmethod
    def from_db_row(row):
        return Funcionario(id=row['id'], nome=row['nome'], telefone=row['telefone'], cpf=row['cpf'], codigo=row['codigo'], usuario=row['usuario'], senha=row['senha'], id_cargo=row['id_cargo'])
        
    def serialize(self):  
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'cpf': self.cpf,
            'codigo': self.codigo,
            'usuario': self.usuario,
            'senha': self.senha,
            'id_cargo': self.id_cargos
        }
    from app.database import mydb

class Funcionario:
    def __init__(self, id, id_cargo, nome, telefone, cpf, codigo, usuario, senha, nome_cargo, hierarquia):
        self.id = id
        self.id_cargo = id_cargo
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.codigo = codigo
        self.usuario = usuario
        self.senha = senha
        self.nome_cargo = nome_cargo
        self.hierarquia = hierarquia

    @staticmethod
    def from_db_row(row):
        return Funcionario(
            id=row['id'],
            id_cargo=row['id_cargo'],
            nome=row['nome'],
            telefone=row['telefone'],
            cpf=row['cpf'],
            codigo=row['codigo'],
            usuario=row['usuario'],
            senha=row['senha'],
            nome_cargo=row['nome_cargo'],
            hierarquia=row['hierarquia']
        )
        
    def serialize(self):  
        return {
            'id': self.id,
            'id_cargo': self.id_cargo,
            'nome': self.nome,
            'telefone': self.telefone,
            'cpf': self.cpf,
            'codigo': self.codigo,
            'usuario': self.usuario,
            'senha': self.senha,
            'nome_cargo': self.nome_cargo,
            'hierarquia': self.hierarquia
        }

