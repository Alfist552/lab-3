import tkinter as tk
from tkinter import ttk
import random
import os

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
            self.show_error_message("setup_window", e)

    def initialize_variables(self):
        try:
            self.grid_size = 6
            self.game_active = False
            self.cards = []
            self.flipped.cards = []
            self.matched.pairs = 0
            self.total_pairs = 0
            self.moves = 0
            self.card_images = []
            self.card_back_image = None

        except Exception as e:
            print("Ошибка инициализации")
            self.show_error_mesage("initialize_variables", e)