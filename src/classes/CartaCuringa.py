from classes.Carta import Carta

class CartaCuringa(Carta):
    def __init__(self, mais_quatro):
        super().__init__()
        self.mais_quatro = mais_quatro
        self.cor_escolhida = ""
        self.codigo = f'mais_quatro_{mais_quatro}'
