import json
from Baralho import Baralho
from Jogador import Jogador
from Mesa import Mesa
#import jsons
from CartaCuringa import CartaCuringa
from CartaEspecial import CartaEspecial
from CartaNumerada import CartaNumerada
from CartaColorida import CartaColorida

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


    def receber_jogada(self, tipo_jogada, dict_jogada):
        if tipo_jogada == 'jogada_inicial':
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
            carta_atual = self.converter_dict_cartas_para_objetos([dict_mesa['carta_atual']])[0]
            cor_atual = dict_mesa['cor_atual']
            self.mesa = Mesa(baralho, carta_atual, cor_atual)
            self.id_jogador_da_vez = dict_jogada['id_jogador_da_vez']
            self.set_ordem_jogadores()
            self.set_jogador_local()

        #abaixar uma carta sempre encerra o turno
        elif tipo_jogada == 'abaixar_uma_carta':
            jogador = self.get_jogador_por_id(dict_jogada['id_jogador'])
            jogador.baixar_uma_carta(int(dict_jogada['indice_carta_baixada']))
            carta_baixada = self.converter_dict_cartas_para_objetos([dict_jogada['carta']])[0]
            self.mesa.carta_atual = carta_baixada

            self.validar_gritou_uno(dict_jogada, jogador)

            if isinstance(carta_baixada, CartaCuringa):
                if carta_baixada.mais_quatro:
                    #pega o proximo jogador e adiciona 4 cartas na mao dele
                    #atualiza o proximo jogador, pulando o que comprou
                    prox_jogador = self.get_proximo_jogador_por_id(jogador.id)
                    cartas = self.baralho.comprar_x_cartas(4)
                    prox_jogador.mao.append(cartas)
                    self.set_id_jogador_da_vez(jogador.id, pular_dois=True)
                    self.adicionar_log(f'{prox_jogador.nome} comprou 4 cartas!')

                self.mesa.cor_atual = carta_baixada.cor_escolhida
                self.adicionar_log(f'{jogador.nome} escolheu a cor {carta_baixada.cor_escolhida}!')

            elif isinstance(carta_baixada, CartaEspecial):
                if carta_baixada.tipo == 'bloqueio':
                    #pula 1 jogador
                    self.set_id_jogador_da_vez(jogador.id, pular_dois=True)                 
                    prox_jogador = self.get_proximo_jogador_por_id(jogador.id)

                    self.adicionar_log(f'{prox_jogador.nome} foi bloqueado!')
                elif carta_baixada.tipo == 'mais_dois':
                    #pega o proximo jogador e adiciona 2 cartas na mao dele
                    #atualiza o proximo jogador, pulando o que comprou
                    prox_jogador = self.get_proximo_jogador_por_id(jogador.id)
                    cartas = self.baralho.comprar_x_cartas(2)
                    prox_jogador.mao.append(cartas)
                    self.set_id_jogador_da_vez(jogador.id, pular_dois=True)

                    self.adicionar_log(f'{prox_jogador.nome} comprou 2 cartas!')
                elif carta_baixada.tipo == 'inverte':
                    #inverte ordem da lista e seta o proximo baseado no id
                    self.inverter_ordem_jogadores()
                    self.set_id_jogador_da_vez(jogador.id)
                    self.adicionar_log(f'{jogador.nome} inverteu o sentido do jogo!')
            else:
                self.mesa.set_cor_atual()

        elif tipo_jogada == 'comprar_uma_carta':
            jogador = self.get_jogador_por_id(dict_jogada['id_jogador'])
            jogador.gritou_uno = False
            self.validar_gritou_uno(dict_jogada, jogador)
            carta_comprada = self.baralho.pegar_carta()
            jogador.mao.append(carta_comprada)
            if bool(dict_jogada['finalizou_turno']):
                self.set_id_jogador_da_vez(jogador.id)
        

    def validar_gritou_uno(self, dict_jogada, jogador):
        if bool(dict_jogada['gritou_uno']):
            jogador.gritou_uno = True
            for jog in self.jogadores:
                if len(jog.mao) == 1 and not jog.gritou_uno:
                    carta_comprada = self.baralho.pegar_carta()
                    jog.mao.append(carta_comprada)
                    self.adicionar_log(f'{jog.nome} foi denunciado e comprou uma carta!')


    def inverter_ordem_jogadores(self):
        self.ordem_jogadores.reverse()


    def set_id_jogador_da_vez(self, id_jogador, pular_dois=False):
        if pular_dois:
            jogador_pulado = self.get_proximo_jogador_por_id(id_jogador)
            prox_jogador = self.get_proximo_jogador_por_id(jogador_pulado)
            self.id_jogador_da_vez = prox_jogador
        else:
            prox_jogador = self.get_proximo_jogador_por_id(id_jogador)
            self.id_jogador_da_vez = prox_jogador



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
            jogada['tipo_jogada'] = '1'
            #jogada['jogador1'] = jsons.dumps(self.jogadores[0].__dict__)
            #jogada['jogador2'] = jsons.dumps(self.jogadores[1].__dict__)
            #jogada['jogador3'] = jsons.dumps(self.jogadores[2].__dict__)
            #jogada['mesa'] = jsons.dumps(self.mesa.__dict__)
            jogada['id_jogador_da_vez'] = self.id_jogador_da_vez
        elif tipo_jogada == 'abaixar_uma_carta':
            jogada['id_jogador'] = jogador.id
            jogada['carta'] = self.mesa.carta_atual
            jogada['indice_carta_baixada'] = indice_carta_baixada
            jogada['gritou_uno'] = jogador.gritou_uno
            jogada['venceu_partida'] = len(jogador.mao) == 0
        elif tipo_jogada == 'comprar_uma_carta':
            jogada['id_jogador'] = jogador.id
            jogada['gritou_uno'] = jogador.gritou_uno
            jogada['finalizou_turno'] = finalizou_turno

        return jogada
            

    def adicionar_log(self, texto_log):
        self.log[2] = self.log[1]
        self.log[1] = self.log[0]
        self.log[0] = texto_log


    def get_jogador_local(self)->Jogador:
        for jogador in self.jogadores:
            if jogador.id == self.id_local:
                return jogador


    def tem_carta_valida(self):
        mao = self.get_jogador_local().get_mao()
        tem_carta_valida = False

        for i in range(len(mao)):
            eh_valida = self.validar_carta(i)
            if eh_valida:
                tem_carta_valida = True
        
        return tem_carta_valida


    def validar_carta(self, indice):
        carta = self.get_jogador_local().mao[indice]

        eh_colorida = isinstance(carta, CartaColorida)
        if not eh_colorida: 
            return True
        else:
            cor_carta = carta.cor
            carta_atual = self.mesa.carta_atual
            atual_eh_colorida = isinstance(carta_atual, CartaColorida)

            cor_atual = ""
            if atual_eh_colorida:
                cor_atual = self.mesa.carta_atual.cor
            else:
                cor_atual = self.mesa.carta_atual.cor_escolhida
            
            if cor_atual == cor_carta:
                return True
            else:
                if isinstance(carta_atual, CartaCuringa):
                    return False
                else:
                    tipo_carta = carta.tipo
                    tipo_atual = carta_atual.tipo
                    if tipo_atual == tipo_carta:
                        return True
                    else:
                        numero_atual = carta_atual.numero
                        numero_carta = carta.numero
                        if numero_atual == numero_carta:
                            return True
                        else:
                            return False
    
    def validar_carta_teste(self, carta_jogada, carta_atual):
        carta = carta_jogada

        eh_colorida = isinstance(carta, CartaColorida)
        if not eh_colorida:  
            return True
        else:
            cor_carta = carta.cor
            atual_eh_colorida = isinstance(carta_atual, CartaColorida)

            cor_atual = ""
            if atual_eh_colorida:
                cor_atual = carta_atual.cor
            else:
                cor_atual = carta_atual.cor_escolhida
            
            if cor_atual == cor_carta:
                return True
            else:
                if isinstance(carta_atual, CartaCuringa):
                    return False
                numero_atual = carta_atual.numero
                numero_carta = carta.numero
                if numero_atual == numero_carta:
                    return True
                else:
                    tipo_carta = carta.tipo
                    tipo_atual = carta_atual.tipo
                    if tipo_atual == tipo_carta:
                        return True
        
        return False


carta_atual = CartaNumerada("vermelho","numerica", 7)
carta_jogada = CartaNumerada("verde", "numerica", 5)

jogo = Jogo()

print(jogo.validar_carta_teste(carta_jogada, carta_atual))
    
