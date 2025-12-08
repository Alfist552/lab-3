import tkinter as tk
from tkinter import ttk
import random
import os
from PIL import Image, ImageTk

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

    def load_card_images(self):
        try:
            print("Загрузка изображений")
            back_path = os.path.join("cards", "car_back.png")
            if os.path.exists(back_path):
                try:
                    img = img.resize((80, 80))
                    self.card_back_image = ImageTk.PhotoImage(img)
                    print("Загружено")
        except Exception as e:
            print(f"Не удалось загрузить рубашку {e}")

        self.card_images = []
        card_number = 1

        while True:
            front_path = os.path.join("cards", f"card_{card_number}.png")
            if not os.path.exists(front_path):
                break

            try:
                img = Image.open(front_path)
                img = img.resize((80, 80))
                tk_img = ImageTk.PhotoImage(img)
                self.card_images.append(tk_img)
                card_number += 1
            except Exception as e:
                print("Ошибка загрузки")
                break
        if len(self.card_images) > 0:
            self.use_images = True
            print (f" Загружено {len(self.card_images)} изображений")
        else:
            self.use_images = False

            except Exception as e:
                print("Ошибка загрузки")
                self.use_images = False


