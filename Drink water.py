import tkinter as tk
from tkinter import messagebox, ttk
import platform
import shutil
import os

# Simple, robust text-to-speech fallback
try:
    import pyttsx3
    _engine = pyttsx3.init()
    def speak(text):
        _engine.say(text)
        _engine.runAndWait()
except Exception:
    if platform.system() == "Darwin":
        def speak(text): os.system(f'say "{text}"')
    elif platform.system() == "Linux" and shutil.which("espeak"):
        def speak(text): os.system(f'espeak "{text}"')
    else:
        def speak(text): pass  # no-op fallback


DEFAULT_MINUTES = 60
SNOOZE_MINUTES = 5

class WaterReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💧 Water Reminder")
        self.root.geometry("360x230")
        self.root.resizable(False, False)
        self.interval_var = tk.DoubleVar(value=DEFAULT_MINUTES)

        # UI
        frame = tk.Frame(root, padx=12, pady=12)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Stay Hydrated!", font=("Arial", 16, "bold")).pack(pady=(0, 8))

        row = tk.Frame(frame)
        row.pack(pady=(0, 8))
        tk.Label(row, text="Interval (min):").pack(side="left")
        self.interval_entry = tk.Entry(row, width=6, justify="center", textvariable=self.interval_var)
        self.interval_entry.pack(side="left", padx=6)

        self.time_label = tk.Label(frame, text="--:-- remaining", font=("Arial", 12))
        self.time_label.pack()

        self.progress = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=8)

        btns = tk.Frame(frame)
        btns.pack(pady=(6, 0))
        self.start_btn = tk.Button(btns, text="Start", width=10, command=self.start)
        self.start_btn.pack(side="left", padx=6)
        self.stop_btn = tk.Button(btns, text="Stop", width=10, command=self.stop, state="disabled")
        self.stop_btn.pack(side="left", padx=6)
        self.snooze_btn = tk.Button(frame, text=f"Snooze {SNOOZE_MINUTES} min", command=self.snooze, state="disabled")
        self.snooze_btn.pack(pady=(8, 0))

        # State
        self.running = False
        self.interval_secs = int(DEFAULT_MINUTES * 60)
        self.elapsed = 0
        self._after_id = None

        self.update_ui()

        # ensure after callbacks are cancelled on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_ui(self):
        # Ensure progress and time label reflect current state
        self.progress["maximum"] = max(1, self.interval_secs)
        remaining = max(0, self.interval_secs - self.elapsed)
        self.progress["value"] = self.elapsed
        m, s = divmod(int(remaining), 60)
        self.time_label.config(text=f"{m:02d}:{s:02d} remaining")

    def notify(self):
        try:
            messagebox.showinfo("💧 Reminder", "Time to drink water!")
        except Exception:
            pass
        try:
            self.root.bell()
        except Exception:
            pass
        speak("Time to drink water!")

    def tick(self):
        if not self.running:
            return
        self.elapsed += 1
        if self.elapsed >= self.interval_secs:
            self.notify()
            self.elapsed = 0  # start next cycle
        self.update_ui()
        self._after_id = self.root.after(1000, self.tick)

    def start(self):
        if self.running:
            return
        try:
            minutes = float(self.interval_var.get())
            if minutes <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Invalid interval", "Enter a positive number of minutes.")
            return
        self.interval_secs = max(1, int(minutes * 60))
        self.elapsed = 0
        self.running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.snooze_btn.config(state="normal")
        self.update_ui()
        self.tick()

    def stop(self):
        if not self.running:
            return
        self.running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.snooze_btn.config(state="disabled")
        if self._after_id:
            try:
                self.root.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
        self.elapsed = 0
        self.update_ui()

    def snooze(self):
        if not self.running:
            return
        snooze_secs = int(SNOOZE_MINUTES * 60)
        # schedule next alert after snooze; clamp so it's not negative
        self.elapsed = max(0, self.interval_secs - snooze_secs)
        self.update_ui()

    def on_close(self):
        # clean up pending after callbacks then close
        if self._after_id:
            try:
                self.root.after_cancel(self._after_id)
            except Exception:
                pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = WaterReminderApp(root)
    root.mainloop()