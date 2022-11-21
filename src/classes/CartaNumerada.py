import Carta as Carta
from CartaColorida import CartaColorida

class CartaNumerada(CartaColorida):
    def __init__(self, cor, tipo, numero):
        super().__init__(cor, tipo)
        self.numero = numero
        self.codigo = f'{numero}_{cor}'