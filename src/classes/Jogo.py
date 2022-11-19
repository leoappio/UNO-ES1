from classes.Baralho import Baralho
from classes.Jogador import Jogador
from classes.Mesa import Mesa
import jsons


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

    def get_proximo_jogador_por_id(self, id)->Jogador:
        indice_jogador_atual = self.ordem_jogadores.index(id)

        proximo_id = 0
        if len(self.ordem_jogadores) == indice_jogador_atual-1:
            proximo_id = self.ordem_jogadores[0]
        else:
            proximo_id = self.ordem_jogadores[indice_jogador_atual+1]

        for jogador in self.jogadores:
            if jogador.id == proximo_id:
                return jogador

    
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


    def set_ordem_jogadores(self):
        self.ordem_jogadores = []
        for jogador in self.jogadores:
            self.ordem_jogadores.append(jogador.id)
    

    def set_jogador_local(self):
        for jogador in self.jogadores:
            if jogador.id == self.id_local:
                self.jogador_local = jogador
      
    
    def jogadores_list_para_objetos(self, jogadores_list):
        jogadores = []
        for jogador in jogadores_list:
            nome = jogador[0]
            id = jogador[1]
            jogadores.append(Jogador(id, nome))
        
        return jogadores


    def iniciar_jogo(self, jogadores: list, id_jogador_local: str):
        self.id_local = id_jogador_local
        self.jogadores = self.jogadores_list_para_objetos(jogadores)
        self.set_ordem_jogadores()
        self.baralho = Baralho()
        self.mesa = Mesa(self.baralho)
        self.baralho.criar_baralho()
        self.id_jogador_da_vez = self.jogadores[0].id

        for jogador in self.jogadores:
            self.mesa.baralho.embaralhar()
            mao = self.mesa.baralho.dar_cartas()
            jogador.set_mao(mao)

        self.mesa.pegar_carta_inicio()
        self.set_jogador_local()
    

    def get_dict_enviar_jogada(self, tipo_jogada):
        jogada = {}
        if tipo_jogada == '1':
            jogada['match_status'] = 'next'
            jogada['tipo_jogada'] = '1'
            jogada['jogador1'] = jsons.dumps(self.jogadores[0].__dict__)
            jogada['jogador2'] = jsons.dumps(self.jogadores[1].__dict__)
            jogada['jogador3'] = jsons.dumps(self.jogadores[2].__dict__)
            jogada['mesa'] = jsons.dumps(self.mesa.__dict__)
            jogada['id_jogador_da_vez'] = self.id_jogador_da_vez
        return jogada
            

    def adicionar_log(self, texto_log):
        self.log[2] = self.log[1]
        self.log[1] = self.log[0]
        self.log[0] = texto_log

    def validar_carta(self, indice):
        print(f'carta {self.jogador_local.mao[indice].codigo} clicada')
