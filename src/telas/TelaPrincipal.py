from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
from AtorJogador import AtorJogador
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./arquivosTelaPrincipal")

class TelaPrincipal(AtorJogador):
    def __init__(self, jogo, quantidade_de_jogadores):
        super().__init__()
        self.window = Tk()
        self.window.title("UNO")
        self.window.geometry("1600x900")
        self.window.configure(bg = "#FFFFFF")
        self.window.resizable(False, False)
        self.jogo = jogo
        self.quantidade_de_jogadores = quantidade_de_jogadores


    @staticmethod
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    
    def receber_jogada(self):
        meu_id = self.dog_server_interface.meu_id
        self.jogo = self.jogo.receber_jogada(meu_id)
        self.atualizar_interface()
        self.dog_server_interface.send_move(self.jogo)


    def atualizar_interface(self, jogo):
        ...

    def abrir(self):
        canvas = Canvas(
            self.window,
            bg = "#FFFFFF",
            height = 900,
            width = 1600,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)

        background_image = PhotoImage(
            file=self.relative_to_assets("background.png"))

        canvas_bg_image = canvas.create_image(
            800.0,
            450.0,
            image=background_image
        )

        uno_back_image = PhotoImage(
            file=self.relative_to_assets("uno_back.png"))

        deck_of_cards_button = Button(
            image=uno_back_image,
            command=lambda: print("botão baralho clicado"),
        )

        deck_of_cards_button.place(
            x=659.0,
            y=354.0,
            width=135.0,
            height=192.0
        )

        table_image = PhotoImage(
            file=self.relative_to_assets(f'./baralho/{self.jogo.mesa.carta_atual.codigo}.png'))

        canvas_tb_image = canvas.create_image(
            873.0,
            450.0,
            image=table_image
        )
        
        cartas_jogador_local = []
        for i, carta in enumerate(self.jogo.jogador_local.mao): 
            carta_imagem = PhotoImage(
                            file=self.relative_to_assets(f'./baralho/{carta.codigo}.png'))

            cartas_jogador_local.append(carta_imagem)
                
            carta_botao = Button(
                image=cartas_jogador_local[i],
                command=lambda i=i: self.jogo.validar_carta(i)
            )

            carta_botao.place(
                x=(593.0 + i*52),
                y=698.0,
                width=103.0,
                height=147.0
            )

        canvas.create_text(
            756.0,
            640.0,
            anchor="nw",
            text="Fulano",
            fill="#000000",
            font=("Poppins Regular", 24 * -1)
        )

        if self.quantidade_de_jogadores == 4:
            canvas.create_text(
                1109.0,
                432.0,
                anchor="nw",
                text="Fulaninho",
                fill="#000000",
                font=("Poppins Regular", 24 * -1)
            )

            jogador_remoto_direita = []
            for i in range(len(self.jogo.jogadores_remotos[0].mao)):
                jogador_remoto_direita_imagem = PhotoImage(
                    file=self.relative_to_assets("jogador_remoto_direita.png"))
                jogador_remoto_direita.append(jogador_remoto_direita_imagem)
                quarto_jogador_remoto = canvas.create_image(
                    1335.0,
                    (294.0+i*52),
                    image=jogador_remoto_direita[i]
                )

    
        if self.quantidade_de_jogadores >= 3:
            canvas.create_text(
                293.0,
                432.0,
                anchor="nw",
                text="Beltrano",
                fill="#000000",
                font=("Poppins Regular", 24 * -1)
            )
            
            jogador_remoto_esquerda = []
            for i in range(len(self.jogo.jogadores_remotos[1].mao)):
                jogador_remoto_esquerda_imagem = PhotoImage(
                    file=self.relative_to_assets("jogador_remoto_esquerda.png"))
                jogador_remoto_esquerda.append(jogador_remoto_esquerda_imagem)
                segundo_jogador_remoto = canvas.create_image(
                    188.0,
                    (294.0+i*52),
                    image=jogador_remoto_esquerda[i]
                )

        botao_uno_image = PhotoImage(
            file=self.relative_to_assets("botao_uno.png"))
        botao_uno = Button(
            image=botao_uno_image,
            command=lambda: print("Fulano gritou uno"),
        )
        botao_uno.place(
            x=1103.0,
            y=732.0,
            width=160.0,
            height=80.0
        )

        jogador_remoto_cima = []
        for i in range(len(self.jogo.jogadores_remotos[2].mao)):
            jogador_remoto_cima_imagem = PhotoImage(
                file=self.relative_to_assets("jogador_remoto_cima.png"))
            jogador_remoto_cima.append(jogador_remoto_cima_imagem)
            terceiro_jogador_remoto = canvas.create_image(
                (643.0+i*52),
                129.0,
                image=jogador_remoto_cima[i]
            )

        canvas.create_text(
            755.0,
            217.0,
            anchor="nw",
            text="Ciclano",
            fill="#000000",
            font=("Poppins Regular", 24 * -1)
        )

        botao_sair_do_jogo_imagem = PhotoImage(
            file=self.relative_to_assets("botao_sair_do_jogo.png"))
        botao_sair_do_jogo = Button(
            image=botao_sair_do_jogo_imagem,
            command=lambda: print("botao sair do jogo clicado"),
        )
        botao_sair_do_jogo.place(
            x=1482.0,
            y=57.0,
            width=54.0,
            height=54.0
        )

        canvas.create_text(
            115.0,
            82.0,
            anchor="nw",
            text="Vez de Fulano\nCor da rodada: vermelho",
            fill="#000000",
            font=("Poppins Regular", 24 * -1)
        )

        self.window.mainloop()
