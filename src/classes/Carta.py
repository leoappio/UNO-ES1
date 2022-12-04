from abc import ABC

class Carta(ABC):
    def __init__(self):
        self.codigo = ""
        
    def get_codigo(self):
        return self.codigo
        
    def get_mais_quatro(self):
        pass
    
    def set_cor_escolhida(self):
        pass
    
    def get_tipo(self):
        pass