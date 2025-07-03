import tkinter as tk
from tkinter import font, ttk
import time
import threading
import pygame

# Global variables
paused = False
stopped = False
timer_thread = None
total_seconds = 0
dark_mode = True

# Play "Time's Up" sound
def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("timer_sound.wav")
    pygame.mixer.music.play()

# Convert HH:MM:SS to seconds
def get_total_seconds(time_str):
    try:
        h, m, s = map(int, time_str.strip().split(":"))
        return h * 3600 + m * 60 + s
    except:
        return None

def start_timer():
    global paused, stopped, total_seconds, timer_thread
    if timer_thread and timer_thread.is_alive():
        return

    time_input = entry.get()
    total_seconds = get_total_seconds(time_input)

    if total_seconds is None:
        label.config(text="❌ Invalid! Use HH:MM:SS", fg="red")
        return

    paused = False
    stopped = False
    label.config(fg="#00FF66")
    timer_thread = threading.Thread(target=run_timer)
    timer_thread.start()

def run_timer():
    global total_seconds, paused, stopped
    max_time = total_seconds

    while total_seconds >= 0 and not stopped:
        if not paused:
            hrs, rem = divmod(total_seconds, 3600)
            mins, secs = divmod(rem, 60)
            timer = f'{hrs:02d}:{mins:02d}:{secs:02d}'
            label.config(text=timer)
            progress['maximum'] = max_time
            progress['value'] = max_time - total_seconds
            time.sleep(1)
            total_seconds -= 1
        else:
            time.sleep(0.2)

    if not stopped and total_seconds < 0:
        label.config(text="⏰ Time's Up!", fg="#FF4444")
        play_sound()
        if auto_restart.get():
            start_timer()

def pause_resume_timer():
    global paused
    if timer_thread and timer_thread.is_alive():
        paused = not paused
        pause_btn.config(text="▶ Resume" if paused else "⏸ Pause")

def reset_timer():
    global stopped, paused, total_seconds
    stopped = True
    paused = False
    total_seconds = 0
    label.config(text="00:00:00", fg="#00FF66")
    progress['value'] = 0
    pause_btn.config(text="⏸ Pause")

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

def apply_theme():
    bg = "#121212" if dark_mode else "#ffffff"
    fg = "white" if dark_mode else "#000000"
    entry_bg = "#1e1e1e" if dark_mode else "#f0f0f0"
    root.config(bg=bg)
    entry_label.config(bg=bg, fg=fg)
    label.config(bg=bg, fg="#00FF66")
    header.config(bg=bg, fg=fg)
    button_frame1.config(bg=bg)
    button_frame2.config(bg=bg)
    preset_frame.config(bg=bg)
    auto_restart_check.config(bg=bg, fg=fg, selectcolor=bg)
    entry.config(bg=entry_bg, fg="#00FF66")
    for btn in [start_btn, pause_btn, reset_btn, theme_btn]:
        btn.config(bg="#1f1f1f", fg="white", activebackground="#333333")
    for child in preset_frame.winfo_children():
        child.config(bg="#1f1f1f", fg="white", activebackground="#333333")

def on_enter(e): e.widget.config(bg="#2c2c2c")
def on_leave(e): e.widget.config(bg="#1f1f1f")

def set_preset_time(minutes):
    time_str = f"00:{minutes:02d}:00"
    entry.delete(0, tk.END)
    entry.insert(0, time_str)

# GUI setup
root = tk.Tk()
root.title("⏳ Countdown Timer")
root.geometry("600x550")
root.configure(bg="#121212")

# Fonts
header = tk.Label(root, text="⏱ Countdown Timer", font=("Segoe UI", 24, "bold"), fg="white", bg="#121212")
header.pack(pady=(20, 10))

# Preset Buttons
preset_frame = tk.Frame(root, bg="#121212")
preset_frame.pack(pady=(0, 5))

preset_times = [("🕔 5 Min", 5), ("🔟 10 Min", 10), ("⏱ 15 Min", 15)]
for label_txt, mins in preset_times:
    btn = tk.Button(preset_frame, text=label_txt, command=lambda m=mins: set_preset_time(m),
                    font=("Segoe UI", 11), bg="#1f1f1f", fg="white", activebackground="#333333",
                    width=10, relief="flat", bd=0, cursor="hand2")
    btn.pack(side=tk.LEFT, padx=5)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

entry_label = tk.Label(root, text="Enter time (HH:MM:SS):", font=("Segoe UI", 13), fg="#dddddd", bg="#121212")
entry_label.pack()

entry = tk.Entry(root, width=18, font=("Courier", 22), justify="center", bg="#1e1e1e",
                 fg="#00FF66", bd=0, relief="flat", insertbackground="#00FF66")
entry.pack(pady=15)

label = tk.Label(root, text="00:00:00", font=("Courier", 56, "bold"), fg="#00FF66", bg="#121212")
label.pack(pady=20)

style = ttk.Style()
style.theme_use("default")
style.configure("green.Horizontal.TProgressbar", troughcolor="#333", background="#00FF66", thickness=20)
progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate", style="green.Horizontal.TProgressbar")
progress.pack(pady=10)

auto_restart = tk.BooleanVar()
auto_restart_check = tk.Checkbutton(root, text="🔁 Auto-Restart", variable=auto_restart,
                                    font=("Segoe UI", 12), bg="#121212", fg="white",
                                    activebackground="#121212", selectcolor="#121212")
auto_restart_check.pack()

button_frame1 = tk.Frame(root, bg="#121212")
button_frame1.pack(pady=10)
button_frame2 = tk.Frame(root, bg="#121212")
button_frame2.pack(pady=5)

button_style = {
    "font": ("Segoe UI", 13, "bold"),
    "bg": "#1f1f1f",
    "fg": "white",
    "activebackground": "#333333",
    "width": 11,
    "bd": 0,
    "relief": "flat",
    "cursor": "hand2"
}

start_btn = tk.Button(button_frame1, text="▶ Start", command=start_timer, **button_style)
start_btn.grid(row=0, column=0, padx=10)

pause_btn = tk.Button(button_frame1, text="⏸ Pause", command=pause_resume_timer, **button_style)
pause_btn.grid(row=0, column=1, padx=10)

reset_btn = tk.Button(button_frame1, text="🔄 Reset", command=reset_timer, **button_style)
reset_btn.grid(row=0, column=2, padx=10)

theme_btn = tk.Button(button_frame2, text="🌓 Theme", command=toggle_theme, **button_style)
theme_btn.grid(row=0, column=0, padx=10)

for btn in [start_btn, pause_btn, reset_btn, theme_btn]:
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

apply_theme()
root.mainloop()