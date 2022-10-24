from tkinter import messagebox
from dog.dog_interface import DogPlayerInterface
from classes.GlobalDogActor import SingletonDogActor


class AtorJogador(DogPlayerInterface):
    def __init__(self) -> None:
        super().__init__()
        self.window = None
        singleton = SingletonDogActor()
        self.dog_server_interface = singleton.dog_actor
    

    def receive_start(self, start_status):
        message = start_status.get_message()
        messagebox.showinfo(message=message)