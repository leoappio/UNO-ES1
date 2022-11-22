from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, Button, Toplevel, messagebox, simpledialog
from dog.dog_interface import DogPlayerInterface
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

        imagem_logo = PhotoImage(
            file=self.relative_to_assets("image_2.png"))

        logo = self.canvas.create_image(
            800.0,
            361.0,
            image=imagem_logo
        )

        button_image_1 = PhotoImage(
            file=TelaInicial.relative_to_assets("button_1.png"))

        button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.iniciar_partida(),
            relief="flat"
        )
        button_1.place(
            x=616.0,
            y=651.0,
            width=369.0,
            height=112.0
        )

        player_name = simpledialog.askstring(
            title="Player Identification", prompt="Qual é o seu nome?")
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)

        self.window.mainloop()


    def receive_move(self, a_move):
        print('receive move chamado')
        self.jogo.receber_jogada(a_move['tipo_jogada'], a_move)
        if a_move['tipo_jogada'] == 'jogada_inicial':
            print('oi')
            self.abrir_tela_partida()
        else:
            self.atualizar_interface()
    

    def atualizar_interface(self):
        ...


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
        if self.jogo.id_jogador_da_vez == self.jogo.id_local:
            if self.jogo.validar_carta(indice_carta):
                jogador = self.jogo.get_jogador_local()
                self.jogo.baixar_uma_carta(self.jogo.id_local, indice_carta, jogador.gritou_uno)
                self.atualizar_interface()
                dict_jogada = self.jogo.get_dict_enviar_jogada("baixar_uma_carta", jogador)
                self.dog_server_interface.send_move(dict_jogada)
    

    def gritar_uno(self):
        if self.jogo.id_jogador_da_vez == self.jogo.id_local:
            jogador = self.jogo.get_jogador_local()
            jogador.gritou_uno = True
    
    
    def comprar_uma_carta(self):
        if self.jogo.id_jogador_da_vez == self.jogo.id_local:
            if len(jogador.mao) < 20:
                jogador = self.jogo.get_jogador_local()
                finalizou_turno = self.jogo.tem_carta_valida()
                self.jogo.comprar_uma_carta(self.jogo.id_local, jogador.gritou_uno, finalizou_turno)
                self.atualizar_interface()
                tem_carta_valida = self.jogo.tem_carta_valida()
                dict_jogada = self.jogo.get_dict_enviar_jogada('comprar_uma_carta', jogador, finalizou_turno=tem_carta_valida)
                self.dog_server_interface.send_move(dict_jogada)


    def abrir_tela_partida(self):
        nova_tela = Toplevel(self.window)
        local_id = self.jogo.id_local
        self.canvas_jogo = Canvas(
            nova_tela,
            bg="#FFFFFF",
            height=900,
            width=1600,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas_jogo.place(x=0, y=0)

        background_image = PhotoImage(
            master=nova_tela,
            file=self.relative_to_assets("background.png"))

        self.canvas_jogo.create_image(
            800.0,
            450.0,
            image=background_image
        )

        uno_back_image = PhotoImage(
            master=nova_tela,
            file=self.relative_to_assets("uno_back.png"))

        botao_baralho_cartas = Button(
            master=nova_tela,
            image=uno_back_image,
            command=lambda: print("botão baralho clicado"),
        )

        botao_baralho_cartas.place(
            x=659.0,
            y=354.0,
            width=135.0,
            height=192.0
        )

        table_image = PhotoImage(
            master=nova_tela,
            file=self.relative_to_assets(f'./baralho/{self.jogo.mesa.carta_atual.codigo}.png'))

        self.canvas_jogo.create_image(
            873.0,
            450.0,
            image=table_image
        )

        # POSICIONANDO JOGADOR LOCAL
        cartas_jogador_local = []
        print('tamanho mao local', len(self.jogo.jogador_local.mao))
        for i, carta in enumerate(self.jogo.jogador_local.mao):
            carta_imagem = PhotoImage(
                master=nova_tela,
                file=self.relative_to_assets(f'./baralho/{carta.codigo}.png'))

            cartas_jogador_local.append(carta_imagem)

            carta_botao = Button(
                master=nova_tela,
                image=cartas_jogador_local[i],
                command=lambda i=i: self.jogo.validar_carta(i)
            )

            carta_botao.place(
                x=(593.0 + i*52),
                y=698.0,
                width=103.0,
                height=147.0
            )

        self.canvas_jogo.create_text(
            756.0,
            640.0,
            anchor="nw",
            text= self.jogo.jogador_local.nome,
            fill="#000000",
            font=("Poppins Regular", 24 * -1)
        )

        #POSICIONANDO QUEM JOGA DEPOIS DE MIM (EM CIMA)
        jogador_remoto_cima = []
        jogador_cima = self.jogo.get_proximo_jogador_por_id(local_id)
        print('tamanho mao cima', len(jogador_cima.mao))
        for i in range(len(jogador_cima.mao)):
            jogador_remoto_cima_imagem = PhotoImage(
                master=nova_tela,
                file=self.relative_to_assets("jogador_remoto_cima.png"))
            jogador_remoto_cima.append(jogador_remoto_cima_imagem)
            self.canvas_jogo.create_image(
                (643.0+i*52),
                129.0,
                image=jogador_remoto_cima[i]
            )

        self.canvas_jogo.create_text(
            755.0,
            217.0,
            anchor="nw",
            text=jogador_cima.nome,
            fill="#000000",
            font=("Poppins Regular", 24 * -1)
        )

        #POSICIONANDO QUEM JOGA ANTES DE MIM(DIREITA)
        jogador_direita = self.jogo.get_proximo_jogador_por_id(jogador_cima.id)
        self.canvas_jogo.create_text(
            1109.0,
            432.0,
            anchor="nw",
            text=jogador_direita.nome,
            fill="#000000",
            font=("Poppins Regular", 24 * -1)
        )

        jogador_remoto_direita = []
        for i in range(len(jogador_direita.mao)):
            jogador_remoto_direita_imagem = PhotoImage(
                master=nova_tela,
                file=self.relative_to_assets("jogador_remoto_direita.png"))
            jogador_remoto_direita.append(jogador_remoto_direita_imagem)
            self.canvas_jogo.create_image(
                1335.0,
                (294.0+i*52),
                image=jogador_remoto_direita[i]
            )

        botao_uno_image = PhotoImage(
            master=nova_tela,
            file=self.relative_to_assets("botao_uno.png"))

        botao_uno = Button(
            master=nova_tela,
            image=botao_uno_image,
            command=lambda: print("Fulano gritou uno"),
        )
        botao_uno.place(
            x=1103.0,
            y=732.0,
            width=160.0,
            height=80.0
        )

        jogador_da_vez = self.jogo.get_jogador_por_id(self.jogo.id_jogador_da_vez)

        self.canvas_jogo.create_text(
            115.0,
            82.0,
            anchor="nw",
            text=f"Vez de {jogador_da_vez.nome}\nCor da rodada: vermelho",
            fill="#000000",
            font=("Poppins Regular", 24 * -1)
        )

        #nova_tela.mainloop()
