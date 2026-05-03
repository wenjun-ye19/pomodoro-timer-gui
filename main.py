import tkinter as tk
from tkinter import messagebox
import time
import os
import sys

# --- Configuration ---
WORK_TIME = 25 * 60
BREAK_TIME = 5 * 60

# Colours for a calm and focused aesthetic
COLOR_WORK = "#E0F7FA"  # Light Cyan (Calm Focus)
COLOR_BREAK = "#FFF9C4" # Light Yellow (Relax)
COLOR_TEXT = "#37474F"  # Dark Grey Text

# Button colors
COLOR_BTN_BG = "#FFFFFF"     # White Button Background (Matches everything)
COLOR_BTN_FG = "#37474F"     # Dark Grey Text on buttons
COLOR_BTN_ACTIVE = "#ECEFF1" # Slightly darker white for "pressed" feel

COLOR_BTN_START = "#A5D6A7"  # Green for Start button
COLOR_BTN_PAUSE = "#E57373"  # Red for Pause button
COLOR_BTN_RESET = "#FFCC80"  # Orange for Reset button
COLOR_BTN_WORK = "#B3E5FC"   # Light Blue for Work mode button
COLOR_BTN_BREAK = "#FFF59D"  # Light Yellow for Break mode button

FONT_LARGE = ("Helvetica", 48, "bold")
FONT_MEDIUM = ("Helvetica", 14)

class FocusTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Stoic Focus Timer")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        
        # State variables
        self.time_left = WORK_TIME
        self.is_running = False
        self.mode = "work" # 'work' or 'break'
        self.timer_id = None
        
        # Setup UI
        self.setup_ui()
        self.update_display()
        
    def setup_ui(self):
        # Frame for layout
        self.frame = tk.Frame(self.root, bg=COLOR_WORK)
        self.frame.pack(fill="both", expand=True)
        
        # Title Label
        self.title_label = tk.Label(
            self.frame, text="Focus Mode", font=("Helvetica", 16, "bold"),
            bg=COLOR_WORK, fg=COLOR_TEXT
        )
        self.title_label.pack(pady=(20, 10))
        
        # Timer Display
        self.time_label = tk.Label(
            self.frame, text="25:00", font=FONT_LARGE,
            bg=COLOR_WORK, fg=COLOR_TEXT
        )
        self.time_label.pack(pady=10)
        
        # Buttons Frame
        self.btn_frame = tk.Frame(self.frame, bg=COLOR_WORK)
        self.btn_frame.pack(pady=20)
        
        btn_style = {
            "font": FONT_MEDIUM,
            "width": 8,
            #"bg": COLOR_BTN_BG,
            "fg": COLOR_BTN_FG,
            "borderwidth": 1,
            "relief": "raised",
            "activebackground": COLOR_BTN_ACTIVE,
            "activeforeground": COLOR_TEXT
        }
        
        # Start/Pause Button
        self.start_btn = tk.Button(
            self.btn_frame, text="Start",
            command=self.toggle_timer, bg=COLOR_BTN_START, **btn_style
        )
        self.start_btn.grid(row=0, column=0, padx=5)
        
        # Reset Button
        self.reset_btn = tk.Button(
            self.btn_frame, text="Reset",
            command=self.reset_timer, bg=COLOR_BTN_RESET, **btn_style
        )
        self.reset_btn.grid(row=0, column=1, padx=5)
        
        # Mode Switch Buttons
        self.mode_frame = tk.Frame(self.frame, bg=COLOR_WORK)
        self.mode_frame.pack(pady=10)
        
        # Work Mode Button
        tk.Button(
            self.mode_frame, text="Work",
            command=lambda: self.switch_mode("work"), bg=COLOR_BTN_WORK,
            **btn_style
        ).grid(row=0, column=0, padx=5)
        
        # Break Mode Button
        tk.Button(
            self.mode_frame, text="Break",
            command=lambda: self.switch_mode("break"), bg=COLOR_BTN_BREAK,
            **btn_style
        ).grid(row=0, column=1, padx=5)

    def format_time(self, seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def update_display(self):
        """Updates the label text."""
        self.time_label.config(text=self.format_time(self.time_left))
        
        # Determine current background
        current_bg = COLOR_WORK if self.mode == "work" else COLOR_BREAK
        
        # Apply background to frames and labels
        self.frame.config(bg=current_bg)
        self.title_label.config(bg=current_bg)
        self.time_label.config(bg=current_bg)
        
        # Ensure buttons and mode frame also match the current background
        self.btn_frame.config(bg=current_bg)
        self.mode_frame.config(bg=current_bg)
        
        # Update colors based on mode
        if self.mode == "work":
            self.title_label.config(text="🍅 Focus Time")
        else:
            self.title_label.config(text="☕ Break Time")

    def toggle_timer(self):
        if self.is_running:
            self.pause_timer()
        else:
            self.start_timer()

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_btn.config(text="Pause", bg=COLOR_BTN_PAUSE) # Red when running
            self.run_timer()

    def pause_timer(self):
        self.is_running = False
        self.start_btn.config(text="Start", bg=COLOR_BTN_START) # Green when paused
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def run_timer(self):
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
            self.update_display()
            # Schedule next update in 1000ms (1 second)
            self.timer_id = self.root.after(1000, self.run_timer)
        elif self.time_left == 0:
            self.timer_finished()

    def timer_finished(self):
        self.is_running = False
        self.start_btn.config(text="Start", bg=COLOR_BTN_START)
        self.play_alert()
        
        msg = "Work session complete! Time for a break." if self.mode == "work" else "Break over! Back to focus."
        messagebox.showinfo("Timer Done", msg)
        
        # Auto-switch suggestion (optional logic)
        if self.mode == "work":
            self.switch_mode("break")
        else:
            self.switch_mode("work")
        self.reset_timer() # Reset to full duration of new mode

    def reset_timer(self):
        self.pause_timer()
        self.time_left = WORK_TIME if self.mode == "work" else BREAK_TIME
        self.update_display()

    def switch_mode(self, new_mode):
        self.mode = new_mode
        self.pause_timer()
        self.time_left = WORK_TIME if self.mode == "work" else BREAK_TIME
        self.start_btn.config(text="Start")
        self.update_display()

    def play_alert(self):
        """Cross-platform alert."""
        try:
            import winsound
            winsound.Beep(600, 500)
            winsound.Beep(800, 500)
        except ImportError:
            # Linux/Mac fallback (terminal bell)
            print("\a")

if __name__ == "__main__":
    root = tk.Tk()
    app = FocusTimer(root)
    root.mainloop()