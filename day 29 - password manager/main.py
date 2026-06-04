import tkinter as tk
import pyperclip

from random import choice, randint, shuffle
from tkinter import messagebox

# set higher resolution tkinter rendering
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(True)


def main():

    # ---------------------------- SAVE PASSWORD ------------------------------- #
    def save():
        website = website_entry.get()
        user = user_entry.get()
        password = password_entry.get()

        if not website or not password:
            messagebox.showwarning(
                title="Warning",
                message="Website or password cannot be empty!"
            )
            return

        is_ok = messagebox.askokcancel(
            title=website,
            message=f"These are the details entered:\n"
                    f"Email: {user}\n"
                    f"Password: {password}\n"
                    f"Is it ok to save?"
        )
        if is_ok:
            with open(file="data.txt", mode="a") as f:
                f.write(f"{website} | {user} | {password}")
                f.write("\n")

            for entry in [website_entry, password_entry]:
                entry.delete(0, tk.END)

    # ---------------------------- PASSWORD GENERATOR -------------------------- #
    def generate():
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u',
                   'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                   'P',
                   'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        password_list = [choice(letters) for _ in range(randint(8, 10))]
        password_list.extend([choice(symbols) for _ in range(randint(2, 4))])
        password_list.extend([choice(numbers) for _ in range(randint(2, 4))])
        shuffle(password_list)

        password_entry.delete(0, tk.END)
        password = "".join(password_list)
        password_entry.insert(0, password)
        pyperclip.copy(password)

    # ---------------------------- UI SETUP ------------------------------- #
    window = tk.Tk()
    window.title("Password Manager")
    window.configure(
        padx=50,
        pady=50
    )

    image = tk.PhotoImage(file="logo.png")

    canvas = tk.Canvas()
    canvas.configure(
        width=200,
        height=200,
    )
    canvas.create_image(100, 100, image=image)
    canvas.grid(row=0, column=1)

    website_label = tk.Label()
    website_label.configure(text="Website:")
    website_label.grid(row=1, column=0)

    website_entry = tk.Entry()
    website_entry.configure(width=42)
    website_entry.focus()
    website_entry.grid(row=1, column=1, columnspan=2)

    user_label = tk.Label()
    user_label.configure(text="Email/Username:")
    user_label.grid(row=2, column=0)

    user_entry = tk.Entry()
    user_entry.configure(width=42)
    user_entry.insert(0, "flavioryu@gmail.com")
    user_entry.grid(row=2, column=1, columnspan=2)

    password_label = tk.Label()
    password_label.configure(text="Password:")
    password_label.grid(row=3, column=0)

    password_entry = tk.Entry()
    password_entry.configure(width=24)
    password_entry.grid(row=3, column=1, sticky="w")

    generate_button = tk.Button()
    generate_button.configure(text="Generate Password", command=generate)
    generate_button.grid(row=3, column=2)

    add_button = tk.Button()
    add_button.configure(text="Add", command=save)
    add_button.grid(row=4, column=1, columnspan=2, sticky="we")

    window.mainloop()


if __name__ == "__main__":
    main()