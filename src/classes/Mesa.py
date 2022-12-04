class Mesa:
    def __init__(self, baralho, carta_atual="", cor_atual=""):
        self.baralho = baralho
        self.carta_atual = carta_atual
        self.cor_atual = cor_atual

    def pegar_carta_inicio(self):
        carta = self.baralho.pegar_carta_inicial()
        self.carta_atual = carta
        self.cor_atual = self.carta_atual.cor
    
    def set_cor_atual(self, cor=None):
        if cor is None:
            self.cor_atual = self.carta_atual.cor
        else:
            self.cor_atual = cor
            
    def set_carta_atual(self, carta):
        self.carta_atual = carta

    def get_carta_atual(self):
        return self.carta_atual

    def get_baralho(self):
        return self.baralho