import tkinter as tk
from tkinter import ttk, messagebox
import os
import random
from PIL import Image, ImageTk
import sys


class Memory:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.initialize_variables()
        self.load_card_images()
        self.show_main_menu()
        self.start_new_game()

    def setup_window(self):
        try:
            self.root.title("Memory game")
            self.root.geometry("800x600")
            self.root.resizable(True, True)
            self.root.protocol("WM_DELETE_WINDOW",self.on_closing)
        except Exception as e:
            print(f"Произошла ошибка при настройке")
            self.show_error_message("setup_window", e)

    def initialize_variables(self):
        try:
            self.grid_size = 6
            self.game_active = False
            self.can_click = True

            self.cards = []
            self.flipped_cards = []
            self.matched_pairs = 0
            self.total_pairs = 0
            self.moves = 0

            self.card_images = []
            self.card_back_image = None
            self.use_images = True

        except Exception as e:
            print("Ошибка инициализации")
            self.show_error_message("initialize_variables", e)

    def load_card_images(self):
        try:
            print("Загрузка изображений")

            if not os.path.exists("cards"):
                print("Папка не найдена")
                messagebox.showerror(
                    "Ошибка загрузки картинок"
                )
                self.use_images = False
                return

            back_path = os.path.join("cards", "card_back.png")

            if not os.path.exists(back_path):
                print("Не найден файл")

                messagebox.showerror(
                    "Ошибка загрузки картинок"
                )
                self.card_back_image = None
                self.use_images = False
                return
            else:
                try:
                    img = Image.open(back_path)
                    img = img.resize((80, 80))
                    self.card_back_image = ImageTk.PhotoImage(img)
                    print("Загружено")
                except Exception as e:
                    print(f"Не удалось загрузить карточку: {e}")

                    self.card_back_image = None
                    self.use_images = False
                    return

            self.card_images = []
            card_number = 1

            while True:
                front_path = os.path.join("cards", f"card_{card_number}.png")
                if os.path.exists(front_path):
                    try:
                        img = Image.open(front_path)
                        img = img.resize((80, 80))
                        tk_img = ImageTk.PhotoImage(img)
                        self.card_images.append(tk_img)
                        card_number += 1
                    except Exception as e:
                        print("Ошибка загрузки")
                        card_number += 1
                else:
                    print(f"Картинка {card_number} не найдена")
                    break


            min_pairs_needed = (self.grid_size * self.grid_size) // 2

            if len(self.card_images) < min_pairs_needed:
                print(f"Недостаточно картинок")

                messagebox.showwarning(
                    "Мало картинок"
                )
                self.use_images = False
            else:
                print(f"Загружено {len(self.card_images)} картинок")
                self.use_images = True

        except Exception as e:
            print("Ошибка")
            messagebox.showerror("Ошибка загрузки", e)
            self.use_images = False

    def show_main_menu(self):
        try:
            for widget in self.root.winfo_children():
                widget.destroy()

            main_frame = tk.Frame(self.root, bg="lightblue")
            main_frame.pack(fill=tk.BOTH, expand=True)

            title = tk.Label(
                main_frame,
                text='Игра "Memory"',
                font=("Arial", 36, "bold"),
                bg="lightblue",
                fg="darkblue"
            )
            title.pack(pady=50)

            start_btn = tk.Button(
                main_frame,
                text="Начать игру",
                font=("Arial", 20),
                bg="green",
                fg="white",
                width=20,
                height=2,
                command=self.start_game_from_menu
            )
            start_btn.pack(pady=20)

            rules_btn = tk.Button(
                main_frame,
                text="Как играть?",
                font=("Arial", 20),
                bg="orange",
                fg="white",
                width=20,
                height=2,
                command=self.show_rules
            )
            rules_btn.pack(pady=20)

        except Exception as e:
            print(f"Ошибка показа меню: {e}")
            self.show_error_message("show_main_menu", e)

    def create_game_board(self):
        try:
            if not self.use_images:
                return

            print("Создание игрового поля...")

            for widget in self.root.winfo_children():
                widget.destroy()

            main_frame = tk.Frame(self.root)
            main_frame.grid(row=0, column=0, sticky="nsew")

            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_columnconfigure(0, weight=1)

            title = tk.Label(
                main_frame,
                text='Игра "Memory"',
                font=("Arial", 24, "bold")
            )
            title.grid(row=0, column=0, pady=10, columnspan=self.grid_size)

            self.moves_label = tk.Label(
                main_frame,
                text=f"Ходы: {self.moves}",
                font=("Arial", 14)
            )
            self.moves_label.grid(row=1, column=0, pady=5, columnspan=self.grid_size)

            self.game_frame = tk.Frame(main_frame)
            self.game_frame.grid(row=2, column=0, pady=20, columnspan=self.grid_size)

            menu_btn = tk.Button(
                main_frame,
                text="В меню",
                font=("Arial", 12),
                command=self.show_main_menu
            )

            menu_btn.grid(row=3, column=0, pady=10, columnspan=self.grid_size)

            self.prepare_cards()

            for i in range(self.grid_size):
                self.game_frame.grid_rowconfigure(i, weight=1)
                self.game_frame.grid_columnconfigure(i, weight=1)

            self.card_buttons = []
            for row in range(self.grid_size):
                row_buttons = []
                for col in range(self.grid_size):
                    index = row * self.grid_size + col
                    card = self.cards[index]
                    btn = tk.Button(
                        self.game_frame,
                        image=self.card_back_image,
                        width=80,
                        height=80,
                        command=lambda r=row, c=col: self.card_click(r, c)
                    )
                    btn.grid(row=row, column=col, padx=2, pady=2)

                    btn.card_image = self.card_images[card] if self.use_images else None
                    btn.card_value = card
                    btn.is_flipped = False
                    btn.is_matched = False

                    row_buttons.append(btn)

                self.card_buttons.append(row_buttons)

                print(f"Создано поле {self.grid_size}x{self.grid_size}")

        except Exception as e:
            print(f"Ошибка создания игрового поля: {e}")
            self.show_error_message("create_game_board", e)

    def prepare_cards(self):
        self.total_pairs = (self.grid_size * self.grid_size) // 2
        available_cards = min(self.total_pairs, len(self.card_images))
        card_values = list(range(available_cards)) * 2
        if len(card_values) < self.grid_size * self.grid_size:
            while len(card_values) < self.grid_size * self.grid_size:
                card_values.append(random.randint(0, available_cards - 1))
        random.shuffle(card_values)
        self.cards = card_values

        print(f"Подготовлено {len(self.cards)} карточек ({self.total_pairs} пар)")

    def card_click(self, row, col):

        if not self.can_click:
            return

        btn = self.card_buttons[row][col]

        if btn.is_flipped or btn.is_matched:
            return

        btn.config(image=btn.card_image)
        btn.is_flipped = True
        self.flipped_cards.append((row,col))

        if len(self.flipped_cards) == 2:
            self.can_click = False
            self.check_match()

    def check_match(self):
        if len(self.flipped_cards) < 2:
            return

        self.root.after(1000, self.do_check_match)

    def do_check_match(self):
        if len(self.flipped_cards) < 2:
            return

        row1, col1 = self.flipped_cards[0]
        row2, col2 = self.flipped_cards[1]

        self.flipped_cards.clear()

        btn1 = self.card_buttons[row1][col1]
        btn2 = self.card_buttons[row2][col2]

        self.moves += 1

        if btn1.card_value == btn2.card_value:
            btn1.is_matched = True
            btn2.is_matched = True
            self.matched_pairs += 1

            btn1.config(bg = 'light green')
            btn2.config(bg = 'light green')

            self.can_click = True

            if self.matched_pairs == self.total_pairs:
                messagebox.showinfo("Собраны все карточки!", f"Вы выиграли за {self.moves} ходов!")
        else:
            self.root.after(550, lambda: self.flip_back(btn1, btn2))

    def flip_back(self, btn1, btn2):
        """Переворачивает карточки обратно и разблокирует клики"""
        btn1.config(image=self.card_back_image)
        btn2.config(image=self.card_back_image)
        btn1.is_flipped = False
        btn2.is_flipped = False
        self.can_click = True

    def start_new_game(self):
        try:
            print("Начало игры")

            if self.use_images:
                info = f"Игра {self.grid_size} * {self.grid_size}"
                self.create_game_board()
            else:
                print("Недостаточно картинок")
                return
            print (f" {info}")

        except Exception as e:
            print(f"Ошибка создания игры")
            self.show_error_message("start_new_game", e)

    def closing_game(self):
        try:
            print("Закрытие игры")
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            print("Ошибка закрытия игры")

    def on_closing(self):
        self.closing_game()

    def show_error_message(self, *args):
        str_args = [str(arg) for arg in args]
        message = ' '.join(str_args)
        print(f'Ошибка: {message}')


def main():
    try:
        print("="*50)
        print("Игра Memory")
        print("="*50)

        root = tk.Tk()

        game = Memory(root)

        root.mainloop()

    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
