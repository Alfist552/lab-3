import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk
import sys


class Memory:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.initialize_variables()
        self.load_card_images()
        self.interface()
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

    def interface(self):
        try:
            print('Создание интерфейса')
            main_frame = tk.Frame(self.root)
            main_frame.pack(fill = tk.BOTH, expand = True, padx = 10, pady = 10)

            title = ttk.Label(
                main_frame,
                text = 'Игра "Memory"',
                font = ("Arial", 24, "bold")
            )
            title.pack(pady = 20)

            if self.use_images:
                mode_text = f"Режим картинки: ({len(self.card_images)} доступно)"
            else:
                mode_text = "Картинки не загружены"

            mode_label = ttk.Label(
                main_frame,
                text= mode_text,
                font = ("Arial", 12)
            )
            mode_label.pack(pady = 10)

            print("Создание интерфейса")

        except Exception as e:
            print("Ошибка создания интерфейса")
            self.show_error_message("interface", e)

    def start_new_game(self):
        try:
            print("Начало игры")

            if self.use_images:
                info = f"Игра {self.grid_size} * {self.grid_size}"
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
