import json
import os
import random
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from PIL import Image, ImageTk

# todo: add card border as background to the text box
# todo: remove "deck is empty" messages
# todo: add remaining icons

main_dir = Path(__file__).parent
cards_dir = main_dir / "cards"
icons_dir = main_dir / "icons"
banner_dir = main_dir


class CardDrawingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Card Drawing Game")
        self.master.geometry("1920x1080")

        self.cards = self.load_cards()
        self.load_images()
        self.create_widgets()

    def load_cards(self):
        try:
            with open(cards_dir / "cards.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "cards.json file not found!")
            return {}

    def load_images(self):
        self.icons = {}
        for category in self.cards:
            for card_type in self.cards[category]:
                icon_path = icons_dir / f"{card_type.lower().replace(' ', '_')}.png"
                if icon_path.exists:
                    self.icons[card_type] = ImageTk.PhotoImage(
                        Image.open(icon_path).resize((48, 48))
                    )
                else:
                    self.icons[card_type] = None

        banner_path = banner_dir / "banner.png"
        if banner_path.exists:
            self.banner = ImageTk.PhotoImage(
                Image.open(banner_path).resize((1920, 150))
            )
        else:
            self.banner = None

    def create_widgets(self):
        # Banner
        if self.banner:
            banner_label = tk.Label(self.master, image=self.banner)
            banner_label.pack(pady=10)

        # Main frame
        main_frame = tk.Frame(self.master)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Left column (Holidays and Surprise)
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="ns")
        self.create_category_frame(left_frame, "holidays")
        self.create_category_frame(left_frame, "surprise")

        # Center column (Card display)
        center_frame = tk.Frame(main_frame)
        center_frame.grid(row=0, column=1, padx=20)
        self.result_text = tk.Text(
            center_frame, wrap=tk.WORD, width=40, height=10, font=("Arial", 16)
        )
        self.result_text.pack(expand=True, fill="both")

        # Right column (Class)
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=2, sticky="ns")
        self.create_category_frame(right_frame, "class")

        # Configure grid
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

    def create_category_frame(self, parent, category):
        category_frame = tk.LabelFrame(
            parent, text=category.capitalize(), font=("Arial", 14, "bold")
        )
        category_frame.pack(fill="x", padx=10, pady=3, expand=True)

        for card_type in self.cards[category]:
            button_frame = tk.Frame(category_frame)
            button_frame.pack(fill="x", padx=5, pady=1)

            icon = self.icons.get(card_type)
            if icon:
                icon_label = tk.Label(button_frame, image=icon)
                icon_label.pack(side="left")
                icon_label.bind("<Button-1>", lambda e, t=card_type: self.draw_card(t))

            button = tk.Button(
                button_frame,
                text=card_type,
                command=lambda t=card_type: self.draw_card(t),
                font=("Arial", 12),
            )
            button.pack(side="left", expand=True, fill="x")

    def draw_card(self, card_type):
        for category, types in self.cards.items():
            if card_type in types and types[card_type]:
                card = random.choice(types[card_type])
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(
                    tk.END,
                    f"{category.capitalize()} - {card_type.capitalize()} card:\n\n{card}",
                )
                self.result_text.config(state=tk.DISABLED)
                return
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"No cards available in {card_type} deck.")


def main():
    root = tk.Tk()
    app = CardDrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
