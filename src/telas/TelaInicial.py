from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, Button, Toplevel, messagebox, simpledialog
from dog.dog_interface import DogPlayerInterface
from classes.CartaCuringa import CartaCuringa
from dog.dog_actor import DogActor
from classes.Jogo import Jogo
# from PIL import Image, ImageTk
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./arquivos")

class TelaInicial(DogPlayerInterface):
    def __init__(self) -> None:
        super().__init__()
        self.window = Tk()
        self.window.title("UNO")
        self.window.geometry("1600x900")
        self.window.configure(bg="#FFFFFF")
        self.window.resizable(False, False)
        self.canvas = None
        self.jogo = None
        self.images_mao = {}
        self.botoes_mao = {}
        self.window_mao = {}
        self.images_mao_cima = {}
        self.window_mao_cima = {}
        self.images_mao_direita = {}
        self.window_mao_direita = {}

    @staticmethod
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def abrir_tela_inicial(self):
        self.canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=900,
            width=1600,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)

        backgroud_image = PhotoImage(
            file=TelaInicial.relative_to_assets("image_1.png"))

        canvas_bg_image = self.canvas.create_image(
            800.0,
            450.0,
            image=backgroud_image
        )

        # Tela inicial
        imagem_logo = PhotoImage(
            file=self.relative_to_assets("image_2.png"))

        # Criação do logo
        self.logo = self.logo = self.canvas.create_image(
            800.0,
            361.0,
            image=imagem_logo
        )
        
        self.canvas.itemconfigure(self.logo, state='normal')

        # Criação do Botão Jogar
        button_image_1 = PhotoImage(
            master=self.canvas,
            file=self.relative_to_assets("button_1.png"))

        button_1 = Button(
            master=self.canvas,
            image=button_image_1,
            command=lambda: self.iniciar_partida(),
        )
        self.botaoJogar = self.canvas.create_window(616.0, 651.0, width=359.0, height=112.0, anchor='nw', window=button_1)
        # self.button_1.place(
        #     x=616.0,
        #     y=651.0,
        #     width=369.0,
        #     height=112.0
        # )

        #self.canvas.itemconfigure(botaoJogar, 'normal')
        
        # Criação do simpledialog que pergunda o nome
        player_name = simpledialog.askstring(
            title="Player Identification", prompt="Qual é o seu nome?")
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)
        
        # Tela principal
        
        # Criação do baralho
        uno_back_image = PhotoImage(
            master=self.canvas,
            file=self.relative_to_assets("uno_back.png"))

        botao_baralho_cartas = Button(
            master=self.canvas,
            image=uno_back_image,
            command=lambda: self.comprar_uma_carta(),
        )
        
        self.baralho = self.canvas.create_window(659.0, 354.0, width=135.0, height=192.0, anchor='nw', state='hidden', window=botao_baralho_cartas)

        # Criação da carta atual
        table_image = PhotoImage(
            master=self.window,
            file=self.relative_to_assets(f'./baralho/0_amarelo.png'))

        self.table = self.canvas.create_image(
            873.0,
            450.0,
            image=table_image
        )

        self.canvas.itemconfigure(self.table, state='hidden')
        
        # POSICIONANDO JOGADOR LOCAL
        for i in range(7):
            self.images_mao[i] = PhotoImage(
                master=self.window,
                file=self.relative_to_assets(f'./baralho/0_amarelo.png'))

            self.botoes_mao[i] = Button(
                    master=self.window,
                    image=self.images_mao[i],
                    command=lambda i=i: self.abaixar_carta(i)
                )
            
            self.window_mao[i] = self.canvas.create_window((593.0 + i*52), 640.0, width=103.0, height=147.0, anchor='nw', state='hidden', window=self.botoes_mao[i])
            
        for i in range(7, 14):
            self.images_mao[i] = PhotoImage(
                master=self.window,
                file=self.relative_to_assets(f'./baralho/0_amarelo.png'))

            self.botoes_mao[i] = Button(
                    master=self.window,
                    image=self.images_mao[i],
                    command=lambda i=i: self.abaixar_carta(i)
                )
            
            self.window_mao[i] = self.canvas.create_window((593.0 + (i-7)*52), 740.0, width=103.0, height=147.0, anchor='nw', state='hidden', window=self.botoes_mao[i])
        
        self.label_jogador_local = self.canvas.create_text(
            756.0,
            600.0,
            anchor="nw",
            text= "None",
            fill="#000000",
            font=("Poppins Regular", 24 * -1)
        )
        
        self.canvas.itemconfigure(self.label_jogador_local, state='hidden')

        #POSICIONANDO QUEM JOGA DEPOIS DE MIM (EM CIMA)
        for i in range(7):
            self.images_mao_cima[i] = PhotoImage(
                master=self.window,
                file=self.relative_to_assets(f'./jogador_remoto_cima.png'))
            
            self.window_mao_cima[i] = self.canvas.create_image(
                (643.0+i*52),
                180.0,
                image=self.images_mao_cima[i]
            )
            
            self.canvas.itemconfigure(self.window_mao_cima[i], state='hidden')
            
        for i in range(7, 14):
            self.images_mao_cima[i] = PhotoImage(
                master=self.window,
                file=self.relative_to_assets(f'./jogador_remoto_cima.png'))

            self.window_mao_cima[i] = self.canvas.create_image(
                (643.0+(i-7)*52),
                90.0,
                image=self.images_mao_cima[i]
            )
            
            self.canvas.itemconfigure(self.window_mao_cima[i], state='hidden')

        self.label_jogador_cima = self.canvas.create_text(
            755.0,
            260.0,
            anchor="nw",
            text="None",
            fill="#000000",
            font=("Poppins Regular", 24 * -1)
        )
        
        self.canvas.itemconfigure(self.label_jogador_cima, state='hidden')
        
        # #POSICIONANDO QUEM JOGA ANTES DE MIM(DIREITA)
        
        for i in range(7):
            self.images_mao_direita[i] = PhotoImage(
                master=self.window,
                file=self.relative_to_assets(f'./jogador_remoto_direita.png'))
            
            self.window_mao_direita[i] = self.canvas.create_image(
                1287.0,
                (294.0+i*52),
                image=self.images_mao_direita[i]
            )
            
            self.canvas.itemconfigure(self.window_mao_direita[i], state='hidden')
            
        for i in range(7, 14):
            self.images_mao_direita[i] = PhotoImage(
                master=self.window,
                file=self.relative_to_assets(f'./jogador_remoto_direita.png'))

            self.window_mao_direita[i] = self.canvas.create_image(
                1387.0,
                (294.0+(i-7)*52),
                image=self.images_mao_direita[i]
            )
            
            self.canvas.itemconfigure(self.window_mao_direita[i], state='hidden')

        self.label_jogador_direita = self.canvas.create_text(
            1100.0,
            432.0,
            anchor="nw",
            text="None",
            fill="#000000",
            font=("Poppins Regular", 24 * -1)
        )
        
        self.canvas.itemconfigure(self.label_jogador_direita, state='hidden')
        
        botao_uno_image = PhotoImage(
                master=self.window,
                file=self.relative_to_assets("botao_uno.png"))

        botao_uno = Button(
            master=self.window,
            image=botao_uno_image,
            command=lambda: self.gritar_uno(),
        )

        self.botao_uno = self.canvas.create_window(1103.0, 732.0, width=160.0, height=80.0, anchor='nw', state='hidden', window=botao_uno)

        self.infos_turno = self.canvas.create_text(
            115.0,
            82.0,
            anchor="nw",
            text="None",
            fill="#000000",
            font=("Poppins Regular", 24 * -1)
        )
        
        self.canvas.itemconfigure(self.infos_turno, state='hidden')
        
        self.window.mainloop()


    def receive_move(self, a_move):
        print('receive move chamado')
        print(a_move['tipo_jogada'])
        self.jogo.receber_jogada(a_move['tipo_jogada'], a_move)
        if a_move['tipo_jogada'] == 'jogada_inicial':
            print('oi')
            self.abrir_tela_partida()
        else:
            self.atualizar_interface()
    

    def atualizar_interface(self):
        print('atualizar interface')
        self.abrir_tela_partida()


    def receive_start(self, start_status):
        print('receive start chamado')
        id_jogador_local = start_status.get_local_id()
        self.jogo = Jogo()
        self.jogo.id_local = id_jogador_local      
    

    def iniciar_partida(self):
        start_status = self.dog_server_interface.start_match(3)
        message = start_status.get_message()
        messagebox.showinfo(message=message)
        codigo = start_status.get_code()
        print(start_status.get_players())

        if codigo == '2':
            jogadores = start_status.get_players()
            id_jogador_local = start_status.get_local_id()
            self.jogo = Jogo()
            self.jogo.iniciar_jogo(jogadores, id_jogador_local)
            dict_jogada = self.jogo.get_dict_enviar_jogada('jogada_inicial')
            self.dog_server_interface.send_move(dict_jogada)
            self.abrir_tela_partida()


    def abaixar_carta(self, indice_carta):
        print(f'o indice eh {indice_carta}')
        if self.jogo.id_jogador_da_vez == self.jogo.id_local:
            if self.jogo.validar_carta(indice_carta):
                jogador = self.jogo.get_jogador_local()
                if isinstance(jogador.mao[indice_carta], CartaCuringa):
                    cor = self.escolher_uma_cor()
                    self.jogo.baixar_uma_carta(self.jogo.id_local, indice_carta, jogador.gritou_uno, cor)
                else:   
                    self.jogo.baixar_uma_carta(self.jogo.id_local, indice_carta, jogador.gritou_uno)
                dict_jogada = self.jogo.get_dict_enviar_jogada('baixar_uma_carta', jogador)
                self.dog_server_interface.send_move(dict_jogada)
                self.atualizar_interface()
    

    def gritar_uno(self):
        if self.jogo.id_jogador_da_vez == self.jogo.id_local:
            jogador = self.jogo.get_jogador_local()
            self.jogo.validar_gritou_uno(True, jogador)
    
    
    def comprar_uma_carta(self):
        jogador = self.jogo.get_jogador_local()
        if self.jogo.id_jogador_da_vez == self.jogo.id_local:
            if len(jogador.mao) < 20:
                finalizou_turno = self.jogo.tem_carta_valida()
                self.jogo.comprar_uma_carta(self.jogo.id_local, jogador.gritou_uno, finalizou_turno)
                self.atualizar_interface()
                tem_carta_valida = self.jogo.tem_carta_valida()
                dict_jogada = self.jogo.get_dict_enviar_jogada('comprar_uma_carta', jogador, finalizou_turno=tem_carta_valida)
                self.dog_server_interface.send_move(dict_jogada)

    def escolher_uma_cor(self):
        cor_escolhida = simpledialog.askinteger(
        title="Carta curinga", prompt="Digite 1 para vermelho, 2 para amarelo, 3 para verde e 4 para azul")
        messagebox.showinfo(message="ok")
        if cor_escolhida == 1:
            self.carta_atual.cor_escolhida = 'vermelho'
        elif cor_escolhida == 2:
            self.carta_atual.cor_escolhida = 'amarelo'
        elif cor_escolhida == 3:
            self.carta_atual.cor_escolhida = 'verde'
        elif cor_escolhida == 4:
            self.carta_atual.cor_escolhida = 'azul'
        else:
            self.escolher_uma_cor()

    def abrir_tela_partida(self):
        print('cheguei aqui')
        
        self.carta_atual = PhotoImage(
            master=self.window,
            file=self.relative_to_assets(f'./baralho/{self.jogo.mesa.carta_atual.codigo}.png'))
        
        self.canvas.itemconfigure(self.logo, state='hidden')
        self.canvas.itemconfigure(self.botaoJogar, state='hidden')
        
        self.canvas.itemconfigure(self.table, image=self.carta_atual, state='normal')
        self.canvas.itemconfigure(self.baralho, state='normal')
        
        for i in range(len(self.jogo.jogador_local.mao)):
            carta = PhotoImage(
                master=self.window,
                file=self.relative_to_assets(f'./baralho/{self.jogo.jogador_local.mao[i].codigo}.png'))
            self.images_mao[i] = carta
        
            self.botoes_mao[i].config(image=self.images_mao[i])
            self.canvas.itemconfigure(self.window_mao[i], state='normal')
            
        self.canvas.itemconfig(self.label_jogador_local, text=self.jogo.jogador_local.nome, state='normal')
        
        jogador_cima = self.jogo.get_proximo_jogador_por_id(self.jogo.id_local)
        
        for i in range(len(jogador_cima.mao)):
            self.canvas.itemconfigure(self.window_mao_cima[i], state='normal')
                        
        self.canvas.itemconfigure(self.label_jogador_cima, text=jogador_cima.nome, state='normal')
        
        jogador_direita = self.jogo.get_proximo_jogador_por_id(jogador_cima.id)
        
        for i in range(len(jogador_direita.mao)):
            self.canvas.itemconfigure(self.window_mao_direita[i], state='normal')
                        
        self.canvas.itemconfigure(self.label_jogador_direita, text=jogador_direita.nome, state='normal')
        
        self.canvas.itemconfigure(self.botao_uno, state='normal')
        
        jogador_da_vez = self.jogo.get_jogador_por_id(self.jogo.id_jogador_da_vez)
        
        if isinstance(self.jogo.mesa.carta_atual, CartaCuringa):
            cor = self.jogo.mesa.carta_atual.cor_escolhida
        else:
            cor = self.jogo.mesa.carta_atual.cor
        self.canvas.itemconfigure(self.infos_turno, text=f"Vez de {jogador_da_vez.nome}\nCor da rodada: {cor}", state='normal')