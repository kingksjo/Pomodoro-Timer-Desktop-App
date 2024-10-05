import tkinter as tk
import math
import os
import sys
# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
# I did not write this function got from stack overflow 👆
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# ---------------------------- CONSTANTS ------------------------------- #
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
# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    window.after_cancel(timer)
    global reps
    reps = 0
    canvas.itemconfig(timer_countdown, text="00:00")
    timer_label.config(text="Timer", fg=GREEN)
    checkbox.config(text="")
# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps == 1 or reps == 3 or reps == 5 or reps == 7:
        timer_label.config(text="Focus Session", fg=GREEN)
        countdown(work_sec)   
    elif reps == 8:
        timer_label.config(text="Relaxation Time", fg=RED)
        countdown(long_break_sec)   
    elif reps == 2 or reps == 4 or reps == 6:
        timer_label.config(text="Break", fg=PINK)
        countdown(short_break_sec)        
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def countdown(count):

    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"
    

    canvas.itemconfig(timer_countdown, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, countdown, count - 1)
    elif reps == 8:
        timer_label.config(text="Session Complete")
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for i in range(work_sessions):
            marks += "✔️"
        checkbox.config(text=marks)  
# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Pomodoro")
window.minsize(width=300, height=550)
window.config(padx=60, pady=80, bg=YELLOW)

# Timer Label
timer_label = tk.Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 35, "bold"))
timer_label.grid(row=0, column=1)

# Start Button
start_button = tk.Button(text="Start", command=start_timer)
start_button.grid(row=2, column=0)

# Reset Button
reset_button = tk.Button(text="Reset", command=reset_timer)
reset_button.grid(row=2, column=2)

# Checkbox
checkbox = tk.Label(bg=YELLOW, fg=GREEN, font=(FONT_NAME, 20, "bold"))
checkbox.grid(row=3, column=1)

# Timer Canvas
canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
background_img = tk.PhotoImage(file=resource_path(r"assets\\tomato.png"))
canvas.create_image(100, 112, image=background_img)
timer_countdown = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

window.mainloop()