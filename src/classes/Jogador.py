class Jogador:
    def __init__(self, id, nome, mao =[], gritou_uno = False, vencedor = False):
        self.id = id
        self.nome = nome
        self.mao = mao
        self.gritou_uno = gritou_uno
        self.vencedor = vencedor

    def set_mao(self, mao):
        self.mao = mao
    
    def set_gritou_uno(self, bool):
        self.gritou_uno = bool

    def get_mao(self):
        return self.mao

    def get_mao_size(self):
        return len(self.mao)

    def get_gritou_uno(self):
        return self.gritou_uno
    
    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome
        
    def get_carta_by_indice(self, indice):
        return self.mao[indice]
        
    def baixar_uma_carta(self, indice_na_mao):
        self.mao.pop(indice_na_mao)

    def adicionar_cartas_na_mao(self, cartas):
        for carta in cartas:
            self.mao.append(carta)

    