from dog.dog_actor import DogActor
from dog.dog_interface import DogPlayerInterface
from tkinter import Tk


class AtorJogador(DogPlayerInterface):
    def __init__(self) -> None:
        self.dog_server_interface = DogActor()
        self.window = None
