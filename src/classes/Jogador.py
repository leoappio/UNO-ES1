class Jogador:
    def __init__(self, id, nome, mao =[], gritou_uno = False,
     vencedor = False, num_cartas = 0, tem_carta_valida = False):
        self.id = id
        self.nome = nome
        self.mao = mao
        self.gritou_uno = gritou_uno
        self.vencedor = vencedor
        self.num_cartas = num_cartas
        self.tem_carta_valida = tem_carta_valida

    def set_mao(self, mao):
        self.mao = mao

    def atualizar_tem_carta_valida(self):
        ...
    
    def baixar_uma_carta(self, indice_na_mao):
        self.mao.pop(indice_na_mao)