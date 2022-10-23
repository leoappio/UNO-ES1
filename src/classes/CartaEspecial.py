from classes.CartaColorida import CartaColorida

class CartaEspecial(CartaColorida):
    def __init__(self, cor, tipo):
        super().__init__(cor, tipo)
        self.codigo = f'{tipo}_{cor}'