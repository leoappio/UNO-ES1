from classes.Carta import Carta

class CartaCuringa(Carta):
    def __init__(self, mais_quatro, cor_escolhida =""):
        super().__init__()
        self.mais_quatro = mais_quatro
        self.cor_escolhida = cor_escolhida
        self.codigo = f'mais_quatro_{mais_quatro}'

    def get_cor_escolhida(self):
        return self.cor_escolhida
    
    def get_mais_quatro(self):
        return self.mais_quatro
    
    def set_cor_escolhida(self, nova_cor):
        self.cor_escolhida = nova_cor
