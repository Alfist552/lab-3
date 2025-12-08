import tkinter as tk
from tkinter import ttk
import random

class Memory:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.initialize_variables()
        self.interface()
        self.start_new_game()

    def setup_window(self):
        try:
            self.root.title("Memory game")
            self.root.geometry("800x600")
            self.root.resizatable(True, True)
            self.root.protocol("WM_DELETE_WINDOW",self.on_closing)
        except Exception as e:
            print(f"Произошла ошибка при настройке")

