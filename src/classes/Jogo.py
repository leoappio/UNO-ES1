from classes.Baralho import Baralho
from classes.Jogador import Jogador
from classes.Mesa import Mesa


class Jogo:
    def __init__(self):
        self.jogadores = []
        self.jogador_local = None
        self.id_local = ''
        self.partida_em_andamento = False
        self.id_jogador_da_vez = ''
        self.ordem_jogadores = []
        self.jogador_atual = ''
        self.partida_abandonada = False
        self.log = [None, None, None]
        self.mesa = None

    def get_ordem_jogadores(self):
        return self.ordem_jogadores

    def get_jogadores(self):
        return self.jogadores

    def get_jogadores_remotos(self):
        jogadores_remotos = []
        for jogador in self.jogadores:
            if jogador.id != self.jogador_local:
                jogadores_remotos.append(jogador)
        return jogadores_remotos

    def set_ordem_jogadores(self, jogadores):
        for jogador in jogadores:
            self.ordem_jogadores.insert(int(jogador[2]), jogador[1])
        self.jogador_atual = self.ordem_jogadores[0]

    def iniciar_jogo(self, jogadores: list, id_jogador_local: str):
        self.id_local = id_jogador_local
        self.set_ordem_jogadores(jogadores)
        ordem_jogadores = self.get_ordem_jogadores()
        self.baralho = Baralho()
        self.mesa = Mesa(self.baralho)

        for jogador in jogadores:
            jog = Jogador(jogador[1], jogador[0])
            self.jogadores.append(jog)
            if jogador[1] == id_jogador_local:
                self.jogador_local = jog

        if ordem_jogadores[0] == id_jogador_local:
            lista_jogadores = self.get_jogadores()
            self.baralho.criar_baralho()
            for jogador in lista_jogadores:
                self.mesa.baralho.embaralhar()
                mao = self.mesa.baralho.dar_cartas()
                jogador.set_mao(mao)
            self.mesa.pegar_carta_inicio()

    def adicionar_log(self, texto_log):
        self.log[2] = self.log[1]
        self.log[1] = self.log[0]
        self.log[0] = texto_log

    def validar_carta(self, indice):
        print(f'carta {self.jogador_local.mao[indice].codigo} clicada')
