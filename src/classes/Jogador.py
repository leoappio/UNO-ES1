class Jogador:
    def __init__(self, id, nome, mao =[], gritou_uno = False):
        self.id = id
        self.nome = nome
        self.mao = mao
        self.gritou_uno = gritou_uno

    def set_mao(self, mao):
        self.mao = mao
    
    def set_gritou_uno(self, bool):
        self.gritou_uno = bool

    def get_mao(self):
        return self.mao

    def get_gritou_uno(self):
        return self.gritou_uno
    
    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome
        
    def baixar_uma_carta(self, indice_na_mao):
        self.mao.pop(indice_na_mao)

    