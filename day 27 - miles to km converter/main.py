from tkinter import *


def main():

    def miles_to_km():
        miles = float(miles_input.get())
        km = miles * 1.609
        kilometer_result_label.config(text=round(km))

    window = Tk()
    window.title("Miles to Kilometer converter")
    window.config(padx=20, pady=20)

    miles_input = Entry()
    miles_input.grid(row=0, column=1)

    miles_label = Label(text="Miles")
    miles_label.grid(row=0, column=2)

    is_equal_label = Label(text="is equal to")
    is_equal_label.grid(row=1, column=0)

    kilometer_result_label = Label(text="0")
    kilometer_result_label.grid(row=1, column=1)

    kilometer_label = Label(text="Km")
    kilometer_label.grid(row=1, column=2)

    calculate_button = Button(text="Calculate")
    calculate_button.grid(row=2, column=1)
    calculate_button.configure(command=miles_to_km)

    window.mainloop()


if __name__ == '__main__':
    main()
