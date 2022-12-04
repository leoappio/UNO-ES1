from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, Button, messagebox, simpledialog
from dog.dog_interface import DogPlayerInterface
from classes.CartaCuringa import CartaCuringa
from dog.dog_actor import DogActor
from classes.Jogo import Jogo

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./arquivos")

class TelaInicial(DogPlayerInterface):
    def __init__(self) -> None:
        super().__init__()
        # Configurações da janela
        self.window = Tk()
        self.window.title("UNO")
        self.window.geometry("1600x900")
        self.window.configure(bg="#FFFFFF")
        self.window.resizable(False, False)
        self.canvas = None
        self.jogo = None
        # Auxiliares para o carregamento das cartas dos jogadores
        self.cartas_local_imgs = {}
        self.cartas_local_btns = {}
        self.cartas_local_widgets = {}
        self.cartas_cima_imgs = {}
        self.cartas_cima_widgets = {}
        self.cartas_direita_imgs = {}
        self.cartas_direita_widgets = {}
        # Lista com os widgets de log
        self.log_widgets = []


    @staticmethod
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)
    
    def get_indice_carta_curinga(self):
        return self.indice_carta_curinga

    def set_indice_carta_curinga(self, indice):
        self.indice_carta_curinga = indice
        
    def set_canvas(self, canvas):
        self.canvas = canvas
        
    def set_carta_atual_image(self, nova_imagem):
        self.carta_atual_image = nova_imagem

    def abrir_tela_inicial(self):
        canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=900,
            width=1600,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.set_canvas(canvas)
        self.canvas.place(x=0, y=0)
        
        backgroud_image = PhotoImage(
            file=self.relative_to_assets("background.png"))
        background = self.canvas.create_image(
            800.0,
            450.0,
            image=backgroud_image
        )

        ##### Instancia os widgets da tela inicial
        # Logotipo
        imagem_logo = PhotoImage(
            file=self.relative_to_assets("logo.png"))
        self.logo = self.canvas.create_image(
            800.0,
            361.0,
            image=imagem_logo,
        )

        # Botão jogar
        botao_jogar_image = PhotoImage(
            file=self.relative_to_assets("botao_jogar.png"))
        botao_jogar = Button(
            image=botao_jogar_image,
            command=lambda: self.iniciar_partida(),
        )
        self.botaoJogar = self.canvas.create_window(616.0, 651.0, width=359.0, height=112.0, anchor='nw', window=botao_jogar)
    
        # Criação do modal para coletar o nome do jogador
        player_name = simpledialog.askstring(
            title="Player Identification", prompt="Qual é o seu nome?")
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)
        
        ##### Instancia os widgets da tela de partida
        # Monte de compra/baralho
        uno_back_image = PhotoImage(
            file=self.relative_to_assets("uno_back.png"))
        botao_baralho_cartas = Button(
            image=uno_back_image,
            command=lambda: self.comprar_uma_carta(),
        )
        self.baralho = self.canvas.create_window(659.0, 354.0, width=135.0, height=192.0, anchor='nw', state='hidden', window=botao_baralho_cartas)

        # Carta atual/mesa
        table_image = PhotoImage(
            file=self.relative_to_assets(f'./baralho/0_amarelo.png'))
        self.table = self.canvas.create_image(
            873.0,
            450.0,
            image=table_image,
            state='hidden'
        )
        
        # Nome e mão do jogador local
        for i in range(7):
            self.cartas_local_imgs[i] = PhotoImage(
                file=self.relative_to_assets(f'./baralho/0_amarelo.png'))
            self.cartas_local_btns[i] = Button(
                    image=self.cartas_local_imgs[i],
                    command=lambda i=i: self.abaixar_carta(i)
                )
            self.cartas_local_widgets[i] = self.canvas.create_window((593.0 + i*52), 640.0, width=103.0, height=147.0, anchor='nw', state='hidden', window=self.cartas_local_btns[i])
            
        for i in range(7, 14):
            self.cartas_local_imgs[i] = PhotoImage(
                file=self.relative_to_assets(f'./baralho/0_amarelo.png'))
            self.cartas_local_btns[i] = Button(
                    image=self.cartas_local_imgs[i],
                    command=lambda i=i: self.abaixar_carta(i)
                )
            self.cartas_local_widgets[i] = self.canvas.create_window((593.0 + (i-7)*52), 740.0, width=103.0, height=147.0, anchor='nw', state='hidden', window=self.cartas_local_btns[i])
        
        self.label_jogador_local = self.canvas.create_text(
            755.0,
            600.0,
            anchor="nw",
            text= "None",
            fill="#000000",
            font=("Poppins Regular", 24 * -1),
            state='hidden'
        )

        # Nome e cartas do jogador de cima
        for i in range(7):
            self.cartas_cima_imgs[i] = PhotoImage(
                file=self.relative_to_assets(f'./jogador_remoto_cima.png'))
            self.cartas_cima_widgets[i] = self.canvas.create_image(
                (643.0+i*52),
                185.0,
                image=self.cartas_cima_imgs[i],
                state='hidden'
            )
   
        for i in range(7, 14):
            self.cartas_cima_imgs[i] = PhotoImage(
                file=self.relative_to_assets(f'./jogador_remoto_cima.png'))
            self.cartas_cima_widgets[i] = self.canvas.create_image(
                (643.0+(i-7)*52),
                85.0,
                image=self.cartas_cima_imgs[i], 
                state='hidden'
            )
            
        self.label_jogador_cima = self.canvas.create_text(
            755.0,
            265.0,
            anchor="nw",
            text="Player3",
            fill="#000000",
            font=("Poppins Regular", 24 * -1),
            state='hidden'
        )
        
        # Nome e cartas do jogador a direita
        for i in range(7):
            self.cartas_direita_imgs[i] = PhotoImage(
                file=self.relative_to_assets(f'./jogador_remoto_direita.png'))
            self.cartas_direita_widgets[i] = self.canvas.create_image(
                1413.0,
                (294.0+i*52),
                image=self.cartas_direita_imgs[i],
                state='hidden'
            )
            
        for i in range(7, 14):
            self.cartas_direita_imgs[i] = PhotoImage(
                file=self.relative_to_assets(f'./jogador_remoto_direita.png'))
            self.cartas_direita_widgets[i] = self.canvas.create_image(
                1513.0,
                (294.0+(i-7)*52),
                image=self.cartas_direita_imgs[i],
                state='hidden'
            )

        self.label_jogador_direita = self.canvas.create_text(
            1226.0,
            432.0,
            anchor="nw",
            text="Player2",
            fill="#000000",
            font=("Poppins Regular", 24 * -1),
            state='hidden'
        )
        
        # Botão gritar UNO
        botao_uno_image = PhotoImage(
                file=self.relative_to_assets("botao_uno.png"))
        botao_uno = Button(
            image=botao_uno_image,
            command=lambda: self.gritar_uno(),
        )
        self.botao_uno = self.canvas.create_window(1103.0, 732.0, width=160.0, height=80.0, anchor='nw', state='hidden', window=botao_uno)

        # Texto lateral com as informações sobre o turno: Jogador da vez e cor atual
        self.infos_turno = self.canvas.create_text(
            115.0,
            82.0,
            anchor="nw",
            text="None",
            fill="#000000",
            font=("Poppins Regular", 24 * -1),
            state='hidden'
        )
        
        # Botões para escolha da cor da rodada
        botao_amarelo_image = PhotoImage(
            file=self.relative_to_assets("botao_amarelo.png"))
        botao_amarelo = Button(
            image=botao_amarelo_image,
            command=lambda: self.escolher_uma_cor('amarelo'),
        )
        self.botao_amarelo = self.canvas.create_window(145.0, 734.0, width=70.0, height=70.0, anchor='nw', state='hidden', window=botao_amarelo)

        botao_vermelho_image = PhotoImage(
            file=self.relative_to_assets("botao_vermelho.png"))
        botao_vermelho = Button(
            image=botao_vermelho_image,
            command=lambda: self.escolher_uma_cor('vermelho'),
        )
        self.botao_vermelho = self.canvas.create_window(218.0, 734.0, width=70.0, height=70.0, anchor='nw', state='hidden', window=botao_vermelho)

        botao_azul_image = PhotoImage(
            file=self.relative_to_assets("botao_azul.png"))
        botao_azul = Button(
            image=botao_azul_image,
            command=lambda: self.escolher_uma_cor('azul'),
        )
        self.botao_azul = self.canvas.create_window(218.0, 661.0, width=70.0, height=70.0, anchor='nw', state='hidden', window=botao_azul)

        botao_verde_image = PhotoImage(
            file=self.relative_to_assets("botao_verde.png"))
        botao_verde = Button(
            image=botao_verde_image,
            command=lambda: self.escolher_uma_cor('verde'),
        )
        self.botao_verde = self.canvas.create_window(145.0, 661.0, width=70.0, height=70.0, anchor='nw', state='hidden', window=botao_verde)
        
        # Log da partida
        for i in range(3):
            log = self.canvas.create_text(
                1101.0,
                (80.0 + 40*i),
                anchor="nw",
                text="",
                fill="#000000",
                font=("Poppins Regular", 21 * -1),
                state="hidden"
            )
            self.log_widgets.append(log)

        ##### Instancia os widgets da tela de encerramento
        vitoria_image = PhotoImage(
            file=self.relative_to_assets("vitoria.png"))
        self.background_vitoria = self.canvas.create_image(
            800.0,
            450.0,
            image=vitoria_image,
            state='hidden'
        )
        

        self.vitoria_text = self.canvas.create_text(
            174.0,
            367.0,
            anchor="nw",
            text="O vencedor é\n",
            fill="#000000",
            font=("Poppins Bold", 64 * -1),
            state='hidden'
        )
        
        self.window.mainloop()


    def receive_move(self, a_move):
        self.jogo.receber_jogada(a_move['tipo_jogada'], a_move)
        if a_move['tipo_jogada'] == 'jogada_inicial':
            self.abrir_tela_partida()
        else:
            self.atualizar_interface()


    def receive_start(self, start_status):
        id_jogador_local = start_status.get_local_id()
        self.jogo = Jogo()
        self.jogo.set_id_local(id_jogador_local)
    

    def receive_withdrawal_notification(self):
        self.jogo.set_partida_em_andamento(False)
        messagebox.showinfo(message="Partida encerrada! Algum jogador foi desconectado.")
        self.window.destroy()


    def iniciar_partida(self):
        start_status = self.dog_server_interface.start_match(3)
        message = start_status.get_message()
        messagebox.showinfo(message=message)
        codigo = start_status.get_code()

        if codigo == '2':
            jogadores = start_status.get_players()
            id_jogador_local = start_status.get_local_id()
            self.jogo = Jogo()
            self.jogo.iniciar_jogo(jogadores, id_jogador_local)
            dict_jogada = self.jogo.get_dict_enviar_jogada('jogada_inicial')
            self.dog_server_interface.send_move(dict_jogada)
            self.abrir_tela_partida()


    def abaixar_carta(self, indice):
        partida_em_andamento = self.jogo.get_partida_em_andamento()
        vez_do_jogador = self.jogo.get_vez_do_jogador()
        if partida_em_andamento and vez_do_jogador:
            tem_carta_valida = self.jogo.tem_carta_valida()
            if tem_carta_valida:
                eh_carta_valida = self.jogo.validar_carta(indice)
                if eh_carta_valida:
                    jogador = self.jogo.get_jogador_local()
                    eh_carta_curinga = isinstance(jogador.mao[indice], CartaCuringa)
                    if eh_carta_curinga:
                        self.liberar_escolha_de_cor()
                        self.set_indice_carta_curinga(indice)
                    else:
                        id_local = jogador.get_id()
                        gritou_uno = jogador.get_gritou_uno()
                        self.jogo.baixar_uma_carta(id_local, indice, gritou_uno)
                        dict_jogada = self.jogo.get_dict_enviar_jogada('baixar_uma_carta', jogador, True, indice)
                        self.dog_server_interface.send_move(dict_jogada)
                        self.atualizar_interface()
    

    def gritar_uno(self):
        id_atual = self.jogo.get_id_jogador_da_vez()
        id_local = self.jogo.get_id_local()
        if id_atual == id_local:
            self.jogo.gritar_uno()
    
    
    def comprar_uma_carta(self):
        jogador = self.jogo.get_jogador_local()
        if self.jogo.id_jogador_da_vez == self.jogo.id_local:
            if len(jogador.mao) < 20:
                self.jogo.comprar_uma_carta(self.jogo.id_local, jogador.gritou_uno, eh_local=True)
                tem_carta_valida = self.jogo.tem_carta_valida()
                dict_jogada = self.jogo.get_dict_enviar_jogada('comprar_uma_carta', jogador, finalizou_turno=not tem_carta_valida)
                self.dog_server_interface.send_move(dict_jogada)
                self.atualizar_interface()


    def liberar_escolha_de_cor(self):
        self.canvas.itemconfigure(self.botao_verde, state='normal')
        self.canvas.itemconfigure(self.botao_amarelo, state='normal')
        self.canvas.itemconfigure(self.botao_azul, state='normal')
        self.canvas.itemconfigure(self.botao_vermelho, state='normal')


    def escolher_uma_cor(self, cor):
        jogador = self.jogo.get_jogador_local()
        jogador.mao[self.indice_carta_curinga].cor_escolhida = cor
        self.jogo.mesa.carta_atual.cor_escolhida = cor
        self.jogo.baixar_uma_carta(self.jogo.id_local, self.indice_carta_curinga, jogador.gritou_uno, cor=cor)
        dict_jogada = self.jogo.get_dict_enviar_jogada('baixar_uma_carta', jogador, finalizou_turno=True, indice_carta_baixada=self.indice_carta_curinga)
        self.dog_server_interface.send_move(dict_jogada)
        
        self.canvas.itemconfigure(self.botao_verde, state='hidden')
        self.canvas.itemconfigure(self.botao_amarelo, state='hidden')
        self.canvas.itemconfigure(self.botao_azul, state='hidden')
        self.canvas.itemconfigure(self.botao_vermelho, state='hidden')
        
        self.atualizar_interface()


    def atualizar_interface(self):
        partida_em_andamento = self.jogo.get_partida_em_andamento()
        if partida_em_andamento:
            # Atualiza carta atual/mesa
            nova_imagem = PhotoImage(
                file=self.relative_to_assets(f'./baralho/{self.jogo.mesa.carta_atual.codigo}.png'))
            self.set_carta_atual_image(nova_imagem)
            self.canvas.itemconfigure(self.table, image=self.carta_atual_image, state='normal')
            
            jogador_local = self.jogo.get_jogador_local()
            jogador_cima = self.jogo.get_proximo_jogador_por_id(self.jogo.id_local)
            jogador_direita = self.jogo.get_proximo_jogador_por_id(jogador_cima.id)
            
            # Atualiza cartas do jogador local
            for i in range(14):
                if i < jogador_local.get_mao_size():
                    carta = PhotoImage(
                        file=self.relative_to_assets(f'./baralho/{self.jogo.jogador_local.mao[i].codigo}.png'))
                    self.cartas_local_imgs[i] = carta
                    self.cartas_local_btns[i].config(image=self.cartas_local_imgs[i])
                    self.canvas.itemconfigure(self.cartas_local_widgets[i], state='normal')
                else:
                    self.canvas.itemconfigure(self.cartas_local_widgets[i], state='hidden')
            
            # Atualiza cartas do jogador de cima
                if i < jogador_cima.get_mao_size():
                    self.canvas.itemconfigure(self.cartas_cima_widgets[i], state='normal')
                else:
                    self.canvas.itemconfigure(self.cartas_cima_widgets[i], state='hidden')
            
            # Atualiza cartas do jogador a direita
                if i < jogador_direita.get_mao_size():
                    self.canvas.itemconfigure(self.cartas_direita_widgets[i], state='normal')
                else:
                    self.canvas.itemconfigure(self.cartas_direita_widgets[i], state='hidden')

            self.canvas.itemconfigure(self.label_jogador_direita, text=jogador_direita.nome, state='normal')
            self.canvas.itemconfig(self.label_jogador_local, text=self.jogo.jogador_local.nome, state='normal')
            self.canvas.itemconfigure(self.label_jogador_cima, text=jogador_cima.nome, state='normal')
            
            # Atualiza as informações da rodada
            jogador_da_vez = self.jogo.get_jogador_por_id(self.jogo.id_jogador_da_vez)
            if isinstance(self.jogo.mesa.carta_atual, CartaCuringa):
                cor_atual = self.jogo.mesa.carta_atual.cor_escolhida
            else:
                cor_atual = self.jogo.mesa.carta_atual.cor
            
            self.canvas.itemconfigure(self.infos_turno, text=f"Vez de {jogador_da_vez.nome}\nCor da rodada: {cor_atual}", state='normal')
            
            # Atualiza log
            self.atualizar_log()

        else:
            self.abrir_tela_vitoria()
        
        
    def atualizar_log(self):
        for i in range(3):
            self.canvas.itemconfigure(self.log_widgets[i], text=self.jogo.log[i], state='normal')
            
    def abrir_tela_vitoria(self):
        self.canvas.itemconfigure(self.background_vitoria, state='normal')
        self.canvas.itemconfigure(self.vitoria_text, text=f"O vencedor é \n{self.jogo.vencedor}", state='normal')
        self.canvas.itemconfigure(self.botao_uno, state='hidden')
        self.canvas.itemconfigure(self.baralho, state='hidden')
        self.canvas.itemconfigure(self.botao_verde, state='hidden')
        self.canvas.itemconfigure(self.botao_amarelo, state='hidden')
        self.canvas.itemconfigure(self.botao_azul, state='hidden')
        self.canvas.itemconfigure(self.botao_vermelho, state='hidden')

        for i in range(len(self.cartas_local_widgets)):
            self.canvas.itemconfigure(self.cartas_local_widgets[i], state='hidden')
            
    def abrir_tela_partida(self):
        # Esconde widgets da tela principal
        self.canvas.itemconfigure(self.logo, state='hidden')
        self.canvas.itemconfigure(self.botaoJogar, state='hidden')
   
        # Mostra o botões do jogo
        self.canvas.itemconfigure(self.botao_uno, state='normal')
        self.canvas.itemconfigure(self.baralho, state='normal')
    
        # Atualiza a interface com as informações carregadas
        self.atualizar_interface()
