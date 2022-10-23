from classes.Carta import Carta
from abc import ABC

class CartaColorida(Carta, ABC):
    def __init__(self, cor, tipo):
        super().__init__()
        self.cor = cor
        self.tipo = tipo

