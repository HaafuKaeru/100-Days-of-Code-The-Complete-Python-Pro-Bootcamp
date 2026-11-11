import tkinter as tk
from json import JSONDecodeError

import pyperclip
import json

from random import choice, randint, shuffle
from tkinter import messagebox

# set higher resolution tkinter rendering
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(True)


def main():

    # ---------------------------- SEARCH PASSWORD ----------------------------- #
    def search():
        website = website_entry.get()
        try:
            with open("data.json", "r") as f:
                data_dict = json.load(f)
        except FileNotFoundError:
            messagebox.showerror(
                "Error",
                "No data file found"
            )
        else:
            if website in data_dict.keys():
                messagebox.showinfo(
                    f"{website}",
                    f"Email: {data_dict[website]['email']}\n"
                    f"Password: {data_dict[website]['password']}"
                )
            else:
                messagebox.showerror(
                    "Error",
                    f"No details for the {website} exists"
                )

    # ---------------------------- SAVE PASSWORD ------------------------------- #
    def save():
        website = website_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        new_data = {
            website: {
                "email": email,
                "password": password,
            }
        }

        if not website or not password:
            messagebox.showwarning(
                title="Warning",
                message="Website or password cannot be empty!"
            )
            return

        is_ok = messagebox.askokcancel(
            title=website,
            message=f"These are the details entered:\n"
                    f"Email: {email}\n"
                    f"Password: {password}\n"
                    f"Is it ok to save?"
        )
        if is_ok:
            try:
                with open("data.json", "r") as f:
                    data = json.load(f)
            except FileNotFoundError:
                with open("data.json", "w") as f:
                    json.dump(new_data, f, indent=4)
            else:
                data.update(new_data)
                with open(file="data.json", mode="w") as f:
                    json.dump(data, f, indent=4)
            finally:
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
    website_entry.configure(width=24)
    website_entry.focus()
    website_entry.grid(row=1, column=1)

    search_button = tk.Button()
    search_button.configure(text="Search", command=search)
    search_button.grid(row=1, column=2, sticky="we")

    email_label = tk.Label()
    email_label.configure(text="Email/emailname:")
    email_label.grid(row=2, column=0)

    email_entry = tk.Entry()
    email_entry.configure(width=42)
    email_entry.insert(0, "flavioryu@gmail.com")
    email_entry.grid(row=2, column=1, columnspan=2)

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