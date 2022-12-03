import json
from classes.Baralho import Baralho
from classes.Jogador import Jogador
from classes.Mesa import Mesa
import jsons
from classes.CartaCuringa import CartaCuringa
from classes.CartaEspecial import CartaEspecial
from classes.CartaNumerada import CartaNumerada
from classes.CartaColorida import CartaColorida

class Jogo:
    def __init__(self):
        self.jogadores = [None, None, None]
        self.jogador_local = None
        self.id_local = ''
        self.partida_em_andamento = True
        self.id_jogador_da_vez = ''
        self.ordem_jogadores = []
        self.log = [None, None, None]
        self.mesa = None
        self.vencedor = ""

    def get_proximo_jogador_por_id(self, id)->Jogador:
        indice_jogador_atual = self.ordem_jogadores.index(id)
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

    def get_id_local(self):
        return self.id_local

    def get_id_jogador_da_vez(self):
        return self.id_jogador_da_vez

    def set_ordem_jogadores(self):
        self.ordem_jogadores = []
        for jogador in self.jogadores:
            self.ordem_jogadores.append(jogador.id)
    

    def set_jogador_local(self):
        for jogador in self.jogadores:
            if jogador.id == self.id_local:
                self.jogador_local = jogador


    def set_id_local(self, id):
        self.id_local = id

    def set_id_jogador_da_vez(self, id):
        self.id_jogador_da_vez = id

    def set_partida_em_andamento(self, bool):
        self.partida_em_andamento = bool
      
    
    def jogadores_list_para_objetos(self, jogadores_list):
        jogadores = []
        for jogador in jogadores_list:
            nome = jogador[0]
            id = jogador[1]
            jog = Jogador(id, nome)
            jogadores.append(jog)
        
        return jogadores


    def iniciar_jogo(self, jogadores: list, id_jogador_local: str):
        self.set_id_local(id_jogador_local)
        self.jogadores = self.jogadores_list_para_objetos(jogadores)
        self.set_ordem_jogadores()
        baralho = Baralho()
        self.mesa = Mesa(baralho)
        baralho.criar_baralho()
        ordem = self.get_ordem_jogadores()
        self.set_id_jogador_da_vez(ordem[0])
        self.set_partida_em_andamento(True)

        for jogador in self.jogadores:
            self.mesa.baralho.embaralhar()
            mao = self.mesa.baralho.dar_cartas()
            jogador.set_mao(mao)

        self.mesa.pegar_carta_inicio()
        self.set_jogador_local()


    def receber_jogada(self, tipo_jogada, dict_jogada):
        if tipo_jogada == 'jogada_inicial':
            for i in range(3):
                dict_jogador = json.loads(dict_jogada[f'jogador{i+1}'])
                id = dict_jogador["id"]
                nome = dict_jogador["nome"]
                mao = self.converter_dict_cartas_para_objetos(dict_jogador['mao'])
                gritou_uno = dict_jogador['gritou_uno']
                self.jogadores[i] = Jogador(id, nome, mao, gritou_uno)

            dict_mesa = json.loads(dict_jogada['mesa'])
            cartas_baralho = self.converter_dict_cartas_para_objetos(dict_mesa['baralho']['cartas'])
            baralho = Baralho(cartas_baralho)
            carta_atual = self.converter_dict_cartas_para_objetos([dict_mesa['carta_atual']])[0]
            cor_atual = dict_mesa['cor_atual']
            self.mesa = Mesa(baralho, carta_atual, cor_atual)
            self.id_jogador_da_vez = dict_jogada['id_jogador_da_vez']
            self.set_ordem_jogadores()
            self.set_jogador_local()

        elif tipo_jogada == 'baixar_uma_carta':
            self.partida_em_andamento = bool(dict_jogada['partida_em_andamento'])
            jogador = self.get_jogador_por_id(dict_jogada['id_jogador'])
            carta_baixada = jogador.mao[dict_jogada['indice_carta_baixada']]

            if not self.partida_em_andamento:
                self.vencedor = dict_jogada['vencedor']

            if isinstance(carta_baixada, CartaCuringa):
                cor_escolhida = dict_jogada['cor_escolhida']
                self.baixar_uma_carta(dict_jogada['id_jogador'], dict_jogada['indice_carta_baixada'], dict_jogada['gritou_uno'], cor=cor_escolhida)
            else:
                self.baixar_uma_carta(dict_jogada['id_jogador'], dict_jogada['indice_carta_baixada'], dict_jogada['gritou_uno'])

        elif tipo_jogada == 'comprar_uma_carta':
            self.comprar_uma_carta(dict_jogada['id_jogador'], dict_jogada['gritou_uno'], dict_jogada['finalizou_turno'], False)


    def validar_gritou_uno(self, gritou_uno, jogador):
        if bool(gritou_uno):
            jogador.gritou_uno = True
            tem_jogador_denunciavel = False
            for jog in self.jogadores:
                if len(jog.mao) == 1 and not jog.gritou_uno:
                    tem_jogador_denunciavel = True
                    carta_comprada = self.mesa.baralho.pegar_carta()
                    jog.mao.append(carta_comprada)
                    self.adicionar_log(f'{jog.nome} foi denunciado e comprou uma carta!')
            
            if tem_jogador_denunciavel or (len(jogador.mao) == 1):
                self.adicionar_log(f'{jogador.nome} gritou UNO!')
            else:
                jogador.gritou_uno = False
            


    def comprar_uma_carta(self, id_jogador, gritou_uno, finalizou_turno=False, eh_local = False):
        if eh_local:
            jogador = self.get_jogador_local()
        else:
            jogador = self.get_jogador_por_id(id_jogador)

        jogador.gritou_uno = False
        self.validar_gritou_uno(gritou_uno, jogador)
        carta_comprada = self.mesa.baralho.pegar_carta()
        jogador.mao.append(carta_comprada)

        if eh_local and not self.tem_carta_valida():
            self.set_id_jogador_da_vez(jogador.id)
        elif bool(finalizou_turno):
            self.set_id_jogador_da_vez(jogador.id)
            

    def baixar_uma_carta(self, id_jogador, indice, gritou_uno, cor=""):
        jogador = self.get_jogador_por_id(id_jogador)
        self.adicionar_log(f'{jogador.nome} baixou a carta {jogador.mao[indice].codigo}')
        carta_baixada = jogador.mao[indice]
        jogador.baixar_uma_carta(int(indice))
        self.mesa.carta_atual = carta_baixada

        self.validar_gritou_uno(gritou_uno, jogador)

        if len(jogador.get_mao()) == 0:
            self.partida_em_andamento = False
            self.vencedor = jogador.nome

        if isinstance(carta_baixada, CartaCuringa):
            self.mesa.carta_atual.cor_escolhida = cor
            if carta_baixada.mais_quatro:
                prox_jogador = self.get_proximo_jogador_por_id(jogador.id)
                cartas = self.mesa.baralho.comprar_x_cartas(4)
                prox_jogador.set_mao(prox_jogador.mao + cartas)
                self.set_id_jogador_da_vez(jogador.id, pular_dois=True)
                self.adicionar_log(f'{prox_jogador.nome} comprou 4 cartas!')
            else:
                self.set_id_jogador_da_vez(jogador.id, pular_dois=False)

            self.mesa.cor_atual = carta_baixada.cor_escolhida
            self.adicionar_log(f'{jogador.nome} escolheu a cor {carta_baixada.cor_escolhida}!')

        elif isinstance(carta_baixada, CartaEspecial):
            if carta_baixada.tipo == 'bloqueio':
                self.set_id_jogador_da_vez(jogador.id, pular_dois=True)                 
                prox_jogador = self.get_proximo_jogador_por_id(jogador.id)
                self.adicionar_log(f'{prox_jogador.nome} foi bloqueado!')

            elif carta_baixada.tipo == 'mais_dois':
                prox_jogador = self.get_proximo_jogador_por_id(jogador.id)
                cartas = self.mesa.baralho.comprar_x_cartas(2)
                prox_jogador.mao = prox_jogador.mao + cartas
                self.set_id_jogador_da_vez(jogador.id, pular_dois=True)
                self.adicionar_log(f'{prox_jogador.nome} comprou 2 cartas!')

            elif carta_baixada.tipo == 'inverte':
                self.inverter_ordem_jogadores()
                self.set_id_jogador_da_vez(jogador.id)
                self.adicionar_log(f'{jogador.nome} inverteu o sentido do jogo!')
        else:
            self.set_id_jogador_da_vez(jogador.id)
            self.mesa.set_cor_atual()


    def inverter_ordem_jogadores(self):
        self.ordem_jogadores.reverse()


    def set_id_jogador_da_vez(self, id_jogador, pular_dois=False):
        if pular_dois:
            jogador_pulado = self.get_proximo_jogador_por_id(id_jogador)
            prox_jogador = self.get_proximo_jogador_por_id(jogador_pulado.id)
            self.id_jogador_da_vez = prox_jogador.id
        else:
            prox_jogador = self.get_proximo_jogador_por_id(id_jogador)
            self.id_jogador_da_vez = prox_jogador.id



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


    def get_dict_enviar_jogada(self, tipo_jogada, jogador=None,
     finalizou_turno=False, indice_carta_baixada=0):
        jogada = {}
        if tipo_jogada == 'jogada_inicial':
            jogada['match_status'] = 'next'
            jogada['tipo_jogada'] = 'jogada_inicial'
            jogada['jogador1'] = jsons.dumps(self.jogadores[0].__dict__)
            jogada['jogador2'] = jsons.dumps(self.jogadores[1].__dict__)
            jogada['jogador3'] = jsons.dumps(self.jogadores[2].__dict__)
            jogada['mesa'] = jsons.dumps(self.mesa.__dict__)
            jogada['id_jogador_da_vez'] = self.id_jogador_da_vez
        elif tipo_jogada == 'baixar_uma_carta':
            jogada['tipo_jogada'] = 'baixar_uma_carta'
            jogada['match_status'] = 'next'
            jogada['id_jogador'] = jogador.get_id()
            jogada['indice_carta_baixada'] = indice_carta_baixada
            eh_curinga = isinstance(self.mesa.get_carta_atual(), CartaCuringa)
            if eh_curinga:
                jogada['cor_escolhida'] = self.mesa.get_carta_atual().get_cor_escolhida()
            jogada['gritou_uno'] = jogador.get_gritou_uno()
            jogada['finalizou_turno'] = finalizou_turno
            jogada['partida_em_andamento'] = self.partida_em_andamento
            if not self.partida_em_andamento:
                jogada['vencedor'] = self.get_jogador_local().get_nome()
        elif tipo_jogada == 'comprar_uma_carta':
            jogada['tipo_jogada'] = 'comprar_uma_carta'
            jogada['match_status'] = 'next'
            jogada['id_jogador'] = jogador.get_id()
            jogada['gritou_uno'] = jogador.get_gritou_uno()
            jogada['finalizou_turno'] = finalizou_turno

        return jogada
            

    def adicionar_log(self, texto_log):
        self.log[2] = self.log[1]
        self.log[1] = self.log[0]
        self.log[0] = self.limpar_texto_log(texto_log)


    def get_jogador_local(self)->Jogador:
        for jogador in self.jogadores:
            if jogador.id == self.id_local:
                return jogador

    
    def limpar_texto_log(self, texto_log) -> str:
        if 'mais_quatro_False' in texto_log:
            texto_log = texto_log.replace('mais_quatro_False', 'Curinga')
        elif 'mais_quatro_True' in texto_log:
            texto_log = texto_log.replace('mais_quatro_True', 'Mais Quatro')
        else:
            texto_log = texto_log.replace('_', ' ')
        
        return texto_log


    def tem_carta_valida(self):
        mao = self.get_jogador_local().get_mao()
        tem_carta_valida = False

        for i in range(len(mao)):
            eh_valida = self.validar_carta(i)
            if eh_valida:
                tem_carta_valida = True
        
        return tem_carta_valida


    def validar_carta(self, indice):
        carta = self.jogador_local.mao[indice]

        eh_colorida = isinstance(carta, CartaColorida)
        if not eh_colorida:  
            return True
        else:
            cor_carta = carta.cor
            carta_atual = self.mesa.carta_atual
            atual_eh_colorida = isinstance(carta_atual, CartaColorida)

            cor_atual = ""
            if atual_eh_colorida:
                cor_atual = carta_atual.cor
            else:
                cor_atual = carta_atual.cor_escolhida           
            if cor_atual == cor_carta:
                return True

            if not isinstance(carta_atual, CartaCuringa):
                if carta_atual.tipo == "numerica" and carta.tipo == "numerica":
                    if carta_atual.numero == carta.numero:
                        return True
                elif carta_atual.tipo == carta.tipo:
                        return True
        
        return False


    def gritar_uno(self):
        jogador = self.get_jogador_local()
        jogador.set_gritou_uno(True)