from classes.CartaNumerada import CartaNumerada
from classes.CartaEspecial import CartaEspecial
from classes.CartaCuringa import CartaCuringa

import random

class Baralho:
    def __init__(self):
        self.cartas = []

    def criar_baralho(self):
        cores = ["vermelho", "amarelo", "verde", "azul"]
        tipos = ["bloqueio", "mais_dois", "inverte"]

        for _ in range(0, 2):
            for i in range(0, 10):
                for c in cores:
                    self.cartas.append(CartaNumerada(c, "numerica", i))
            
            for i in tipos:
                for c in cores:
                    self.cartas.append(CartaEspecial(c, i))

            for i in range(0, 2):
                self.cartas.append(CartaCuringa(True))
                self.cartas.append(CartaCuringa(False))

    def embaralhar(self):
        random.shuffle(self.cartas)

    def dar_cartas(self):
        mao_aux = []
        for i in range(0, 7):
            carta = self.cartas.pop()
            mao_aux.append(carta)

        return mao_aux

    def pegar_carta_aleatoria(self):
        carta = self.cartas.pop()
        return carta