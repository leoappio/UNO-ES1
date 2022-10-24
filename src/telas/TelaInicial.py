from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, Button, messagebox, simpledialog
from PIL import Image, ImageTk
from telas.TelaSelecionarJogadores import TelaSelecionarJogadores
from AtorJogador import AtorJogador
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./arquivosTelaInicial")

class TelaInicial(AtorJogador):
    def __init__(self) -> None:
        super().__init__()
        self.window = Tk()
        self.window.title("UNO")
        self.window.geometry("1600x900")
        self.window.configure(bg = "#FFFFFF")
        self.window.resizable(False, False)


    @staticmethod
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


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
        
        backgroud_image = PhotoImage(
            file=TelaInicial.relative_to_assets("image_1.png"))  

        canvas_bg_image = canvas.create_image(
            800.0,
            450.0,
            image=backgroud_image
        )

        imagem_logo = PhotoImage(
            file=self.relative_to_assets("image_2.png"))
        logo = canvas.create_image(
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
            command=lambda: self.open_select_players_screen(),
            relief="flat"
        )
        button_1.place(
            x=616.0,
            y=651.0,
            width=369.0,
            height=112.0
        )
        
        player_name = simpledialog.askstring(title="Player Identification", prompt="Qual é o seu nome?")
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)
        self.window.mainloop()
    

    def open_select_players_screen(self):
        self.window.destroy()
        tela_selecionar_jogadores = TelaSelecionarJogadores()
        tela_selecionar_jogadores.abrir()
