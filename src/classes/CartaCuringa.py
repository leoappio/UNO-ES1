from classes.Carta import Carta

class CartaCuringa(Carta):
    def __init__(self, mais_quatro, cor_escolhida =""):
        super().__init__()
        self.mais_quatro = mais_quatro
        self.cor_escolhida = cor_escolhida
        self.codigo = f'mais_quatro_{mais_quatro}'
