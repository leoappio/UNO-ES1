from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, Button, messagebox
from classes.Jogo import Jogo
from telas.TelaPrincipal import TelaPrincipal
from AtorJogador import AtorJogador


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./arquivosSelecionarJogadores")


class TelaSelecionarJogadores(AtorJogador):
    def __init__(self) -> None:
        super().__init__()
        self.window = Tk()
        self.window.title("UNO - Selecione os Jogadores")
        self.window.geometry("1600x900")
        self.window.configure(bg="#FFFFFF")
        self.window.resizable(False, False)

    @staticmethod
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def abrir(self):
        canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=900,
            width=1600,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)

        image_image_1 = PhotoImage(
            file=TelaSelecionarJogadores.relative_to_assets("image_1.png"))

        image_1 = canvas.create_image(
            800.0,
            450.0,
            image=image_image_1
        )

        canvas.create_text(
            410.0,
            182.0,
            anchor="nw",
            text="Selecione o número de jogadores",
            fill="#FFFFFF",
            font=("Poppins SemiBold", 48 * -1)
        )

        button_image_1 = PhotoImage(
            file=TelaSelecionarJogadores.relative_to_assets("button_1.png"))

        button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.iniciar_partida(2),
            relief="flat"
        )
        button_1.place(
            x=340.0,
            y=327.0,
            width=240.0,
            height=240.0
        )

        button_image_2 = PhotoImage(
            file=TelaSelecionarJogadores.relative_to_assets("button_2.png"))

        button_2 = Button(
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.iniciar_partida(3),
            relief="flat"
        )
        button_2.place(
            x=675.0,
            y=327.0,
            width=240.0,
            height=240.0
        )

        button_image_3 = PhotoImage(
            file=TelaSelecionarJogadores.relative_to_assets("button_3.png"))

        button_3 = Button(
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.iniciar_partida(4),
            relief="flat"
        )
        button_3.place(
            x=1010.0,
            y=327.0,
            width=240.0,
            height=240.0
        )

        self.window.mainloop()

    def iniciar_partida(self, quantidade_de_jogadores):
        start_status = self.dog_server_interface.start_match(
            quantidade_de_jogadores)
        message = start_status.get_message()
        messagebox.showinfo(message=message)
        codigo = start_status.get_code()
        print('codigo: ', codigo)

        if codigo == '2':
            print('iniciar_jogo')
            jogadores = start_status.get_players()
            id_jogador_local = start_status.get_local_id()
            jogo = Jogo()
            jogo.iniciar_jogo(jogadores, id_jogador_local)
            ordem_jogadores = jogo.get_ordem_jogadores()
            print('ordem jogadores: ', ordem_jogadores)
            if ordem_jogadores[0] == id_jogador_local:
                pass  # enviar jogada
            self.window.destroy()
            tela_principal = TelaPrincipal(jogo, quantidade_de_jogadores)
            tela_principal.abrir()

    def receber_inicio(self, start_status):
        jogadores = start_status.get_players()
        id_jogador_local = start_status.get_local_id()
        jogo = Jogo()
        jogo.iniciar_jogo(jogadores, id_jogador_local)
        print(jogo.get_jogadores)
        tela_principal = TelaPrincipal(jogo, len(jogadores))
        tela_principal.abrir()
