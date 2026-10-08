
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
from tkinter import *
import math
import time

# ---------------------------- TIMER RESET ------------------------------- # 

# ---------------------------- TIMER MECHANISM ------------------------------- # 

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 


  

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

from pathlib import Path
from tkinter import *


# ---------------------------- TIMER STATE ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.minsize(width=500, height=400)
window.config(padx=40, pady=25, bg=YELLOW)

current_phase = "Work"
remaining_seconds = WORK_MIN * 60
completed_work_sessions = 0
is_running = False
timer_after_id = None


def format_time(seconds):
    minutes, secs = divmod(seconds, 60)
    return f"{minutes:02}:{secs:02}"


def update_display():
    canvas.itemconfig(timer_text, text=format_time(remaining_seconds))
    canvas.itemconfig(phase_text, text=current_phase)
    canvas.itemconfig(checkmark_text, text="✔ " * completed_work_sessions)


def start_pause_timer():
    global is_running, timer_after_id
    if is_running:
        is_running = False
        if timer_after_id is not None:
            window.after_cancel(timer_after_id)
            timer_after_id = None
        start_button.config(text="Start")
    else:
        is_running = True
        start_button.config(text="Pause")
        timer_after_id = window.after(1000, countdown)


def countdown():
    global remaining_seconds, timer_after_id, current_phase
    timer_after_id = None
    if not is_running:
        return

    remaining_seconds -= 1
    if remaining_seconds > 0:
        update_display()
        timer_after_id = window.after(1000, countdown)
        return

    if current_phase == "Work":
        global completed_work_sessions
        completed_work_sessions += 1
        if completed_work_sessions % 4 == 0:
            current_phase = "Long Break"
            remaining_seconds = LONG_BREAK_MIN * 60
        else:
            current_phase = "Short Break"
            remaining_seconds = SHORT_BREAK_MIN * 60
    else:
        current_phase = "Work"
        remaining_seconds = WORK_MIN * 60

    update_display()
    timer_after_id = window.after(1000, countdown)


def reset_timer():
    global is_running, timer_after_id, current_phase
    global remaining_seconds, completed_work_sessions
    if timer_after_id is not None:
        window.after_cancel(timer_after_id)
        timer_after_id = None
    is_running = False
    current_phase = "Work"
    remaining_seconds = WORK_MIN * 60
    completed_work_sessions = 0
    start_button.config(text="Start")
    update_display()


# ---------------------------- UI SETUP ------------------------------- #
canvas = Canvas(window, width=300, height=260, bg=YELLOW, highlightthickness=0)
canvas.pack(pady=(5, 10))

try:
    tomato_img = PhotoImage(file=str(Path(__file__).with_name("tomato.png")))
    canvas.create_image(150, 130, image=tomato_img)
except TclError:
    # Keep the timer usable when the optional tomato image is unavailable.
    canvas.create_oval(65, 45, 235, 215, fill=RED, outline=RED)
    canvas.create_polygon(135, 55, 150, 25, 165, 55, fill=GREEN, outline=GREEN)

phase_text = canvas.create_text(150, 85, text=current_phase, fill="white", font=(FONT_NAME, 18, "bold"))
timer_text = canvas.create_text(150, 135, text=format_time(remaining_seconds), fill="white", font=(FONT_NAME, 30, "bold"))
checkmark_text = canvas.create_text(150, 185, text="", fill=GREEN, font=(FONT_NAME, 16, "bold"))

controls = Frame(window, bg=YELLOW)
controls.pack()
start_button = Button(controls, text="Start", width=10, command=start_pause_timer)
start_button.pack(side=LEFT, padx=8)
reset_button = Button(controls, text="Reset", width=10, command=reset_timer)
reset_button.pack(side=LEFT, padx=8)

window.mainloop()