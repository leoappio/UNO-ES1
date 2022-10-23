class Jogador:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome
        self.mao = []
        self.gritou_uno = False
        self.vencedor = False
        self.num_cartas = 0
        self.tem_carta_valida = False