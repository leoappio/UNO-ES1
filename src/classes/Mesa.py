class Mesa:
    def __init__(self, baralho, carta_atual=""):
        self.baralho = baralho
        self.carta_atual = carta_atual

    def pegar_carta_inicio(self):
        carta = self.baralho.pegar_carta_aleatoria()
        self.carta_atual = carta