import tkinter as tk
import pandas as pd
import random


# set higher resolution tkinter rendering
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(True)


def main():
    BACKGROUND_COLOR = "#B1DDC6"
    rand_word = {}
    words_list = []

    try:
        data = pd.read_csv("data/words_to_learn.csv")
    except FileNotFoundError:
        original_data = pd.read_csv("data/french_words.csv")
        words_list = original_data.to_dict(orient="records")
    else:
        words_list = data.to_dict(orient="records")

    def draw_card():
        global rand_word
        rand_word = random.choice(words_list)
        flash_card.itemconfig(card_title, text="French", fill="black")
        flash_card.itemconfig(card_word, text=rand_word["French"], fill="black")
        flash_card.itemconfig(current_image, image=img_card_front)
        delay_flip()

    def is_known():
        words_list.remove(rand_word)
        diocane = pd.DataFrame(words_list)
        diocane.to_csv("data/words_to_learn.csv")

    def flip_card():
        flash_card.itemconfig(card_title, text="English", fill="white")
        flash_card.itemconfig(card_word, text=rand_word["English"], fill="white")
        flash_card.itemconfig(current_image, image=img_card_back)

    def delay_flip():
        window.after(3000, flip_card)

    window = tk.Tk()
    window.title("Flashy")
    window.configure(padx=50, pady=50, bg=BACKGROUND_COLOR)

    # images
    img_card_back = tk.PhotoImage(file="images/card_back.png")
    img_card_front = tk.PhotoImage(file="images/card_front.png")
    img_right = tk.PhotoImage(file="images/right.png")
    img_wrong = tk.PhotoImage(file="images/wrong.png")

    w, h = 800, 526
    flash_card = tk.Canvas(width=w, height=h, bg=BACKGROUND_COLOR, highlightthickness=0)
    current_image = flash_card.create_image(w/2, h/2, image=img_card_front)
    card_title = flash_card.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
    card_word = flash_card.create_text(400, 263, text="", font=("Ariel", 60, "bold"), tags="word")
    draw_card()
    flash_card.grid(row=0, column=0, columnspan=2)

    incorrect_button = tk.Button(image=img_wrong, highlightthickness=0, borderwidth=0, command=draw_card)
    incorrect_button.grid(row=1, column=0)

    correct_button = tk.Button(image=img_right, highlightthickness=0, borderwidth=0, command=is_known)
    correct_button.grid(row=1, column=1)


    window.mainloop()


if __name__ == '__main__':
    main()