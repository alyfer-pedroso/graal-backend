class MensagemErro:
    def __init__(self, mensagem, status):
        self.mensagem = mensagem
        self.status = status
        self.erro = True

    def serialize(self):
        return {
            'mensagem': self.mensagem,
            'status': self.status,
            'erro': self.erro
        }

