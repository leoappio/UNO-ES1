class Jogo:
    def __init__(self, mesa, jogadores_remotos, jogador_local):
        self.mesa = mesa
        self.jogadores_remotos = jogadores_remotos
        self.jogador_local = jogador_local
        self.partida_em_andamento = False
        self.jogada_em_andamento = False
        self.ordem_jogadores = []
        self.log = [None, None, None]

    def iniciar_jogo(self):
        for jogador in self.jogadores_remotos:
            self.mesa.baralho.embaralhar()
            mao = self.mesa.baralho.dar_cartas()
            jogador.mao = mao
        mao = self.mesa.baralho.dar_cartas()
        self.jogador_local.mao = mao
        self.mesa.pegar_carta_inicio()
    
    
    def adicionar_log(self, texto_log):
        self.log[2] = self.log[1]
        self.log[1] = self.log[0]
        self.log[0] = texto_log
                
            

    def validar_carta(self, indice):
        print(f'carta {self.jogador_local.mao[indice].codigo} clicada')
