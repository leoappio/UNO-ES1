import json
from classes.Baralho import Baralho
from classes.Jogador import Jogador
from classes.Mesa import Mesa
import jsons
from classes.CartaCuringa import CartaCuringa
from classes.CartaEspecial import CartaEspecial
from classes.CartaNumerada import CartaNumerada

class Jogo:
    def __init__(self):
        self.jogadores = [None, None, None]
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
        print('indice jogador atual = ', indice_jogador_atual)
        print('len ordem jogadores', len(self.ordem_jogadores))

        proximo_id = 0
        if len(self.ordem_jogadores) -1 == indice_jogador_atual:
            proximo_id = self.ordem_jogadores[0]
        else:
            proximo_id = self.ordem_jogadores[indice_jogador_atual+1]

        for jogador in self.jogadores:
            if jogador.id == proximo_id:
                return jogador

    
    def get_jogador_por_id(self, id)->Jogador:
        for jogador in self.jogadores:
            if jogador.id == id:
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


    def atualizar_propriedades(self, tipo_jogada, dict_jogada):
        if tipo_jogada == '1':
            #convertendo jogadores
            for i in range(3):
                dict_jogador = json.loads(dict_jogada[f'jogador{i+1}'])
                id = dict_jogador["id"]
                nome = dict_jogador["nome"]
                mao = self.converter_dict_cartas_para_objetos(dict_jogador['mao'])
                gritou_uno = dict_jogador['gritou_uno']
                vencedor = dict_jogador['vencedor']
                num_cartas = dict_jogador['num_cartas']
                tem_carta_valida = dict_jogador['tem_carta_valida']
                self.jogadores[i] = Jogador(id, nome, mao, gritou_uno, vencedor, num_cartas, tem_carta_valida)

            dict_mesa = json.loads(dict_jogada['mesa'])
            cartas_baralho = self.converter_dict_cartas_para_objetos(dict_mesa['baralho']['cartas'])
            baralho = Baralho(cartas_baralho)
            print('carta atual:',dict_mesa['carta_atual'])
            carta_atual = self.converter_dict_cartas_para_objetos([dict_mesa['carta_atual']])[0]
            self.mesa = Mesa(baralho, carta_atual)

            self.id_jogador_da_vez = dict_jogada['id_jogador_da_vez']
        
        self.set_ordem_jogadores()
        self.set_jogador_local()


    def converter_dict_cartas_para_objetos(self, cartas):
        cartas_obj = []
        for carta in cartas:
            if 'mais_quatro' in carta:
                mais_quatro = carta['mais_quatro']
                cor_escolhida = carta['cor_escolhida']
                cartas_obj.append(CartaCuringa(mais_quatro, cor_escolhida))
            elif 'numero' in carta:
                cor = carta['cor']
                tipo = carta['tipo']
                numero = carta['numero']
                cartas_obj.append(CartaNumerada(cor, tipo, numero))
            else:
                cor = carta['cor']
                tipo = carta['tipo']
                cartas_obj.append(CartaEspecial(cor, tipo))
        
        return cartas_obj


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
