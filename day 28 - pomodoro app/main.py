import tkinter as tk


PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

reps = 0
timer = None


def main():

    # ---------------------------- TIMER RESET ----------------------------------- #
    def reset_timer():
        window.after_cancel(timer)
        timer_label.configure(text="Timer", foreground=GREEN)
        canvas.itemconfig(timer_text, text="00:00")
        pomodoro_ticks.configure(text="")
        global reps
        reps = 0

    # ---------------------------- TIMER MECHANISM ------------------------------- #
    def start_timer():
        global reps
        reps += 1

        work_sec = WORK_MIN * 60
        short_break_sec = SHORT_BREAK_MIN * 60
        long_break_sec = LONG_BREAK_MIN * 60

        if reps % 2 == 0:
            if reps == 8:
                time = long_break_sec
                timer_label.configure(text="Break!", foreground=RED)
            else:
                time = short_break_sec
                timer_label.configure(text="Break", foreground=PINK)
        else:
            time = work_sec
            timer_label.configure(text="Work", foreground=GREEN)

        count_down(time)

    # ---------------------------- COUNTDOWN MECHANISM --------------------------- #
    def count_down(count):

        count_min = count // 60
        count_sec = count % 60

        # format nicely
        if count_min < 10:
            count_min = f"0{count_min}"
        if count_sec < 10:
            count_sec = f"0{count_sec}"

        canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
        if count > 0:
            global timer
            timer = window.after(1000, count_down, count - 1)
        else:
            start_timer()
            pomodoro_ticks.configure(text="✓" * int(reps//2))

    # ---------------------------- UI SETUP -------------------------------------- #
    window = tk.Tk()
    window.title = "Pomodoro"
    padding = 25
    window.config(padx=padding, pady=padding-15, bg=YELLOW)
    window.rowconfigure(4)
    window.columnconfigure(3)

    tomato_img = tk.PhotoImage(file="tomato.png")
    canvas_w = tomato_img.width() + 50
    canvas_h = tomato_img.height() + 10
    centre_x = canvas_w / 2
    centre_y = canvas_h / 2

    canvas = tk.Canvas(width=canvas_w, height=canvas_h, bg=YELLOW, highlightthickness=0)
    canvas.create_image(centre_x, centre_y, image=tomato_img)
    timer_text = canvas.create_text(centre_x, centre_y + 20, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
    canvas.grid(row=1, column=1)

    timer_label = tk.Label(text="Timer", font=(FONT_NAME, 50), fg=GREEN, bg=YELLOW)
    timer_label.grid(row=0, column=1)

    start_button = tk.Button(text="Start", highlightthickness=0, command=start_timer, font=(FONT_NAME, 12))
    start_button.grid(row=2, column=0)

    reset_button = tk.Button(text="Reset", highlightthickness=0, command=reset_timer, font=(FONT_NAME, 12))
    reset_button.grid(row=2, column=2)

    pomodoro_ticks = tk.Label(font=(FONT_NAME, 16, "bold"), fg=GREEN, bg=YELLOW)
    pomodoro_ticks.grid(row=3, column=1)

    window.mainloop()


if __name__ == '__main__':
    main()
