import tkinter as tk
from typing import List, Dict

class FullscreenOverlay:
    def __init__(self, break_duration, on_close):
        self.break_duration = break_duration
        self.on_close = on_close
        self.root = None
        self.remaining = break_duration

    def show(self):
        self.remaining = self.break_duration
        print("Initializing Tkinter root...")
        self.root = tk.Tk()

        # Setup window
        print("Configuring window attributes...")
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)

        # Background logic
        bg_color = '#0A0E1A'
        self.root.configure(bg=bg_color)

        # Background Image Implementation
        try:
            from pathlib import Path
            img_path = Path(__file__).parent.parent / "assets" / "bg.png"
            if img_path.exists():
                self.bg_image = tk.PhotoImage(file=str(img_path))
                self.bg_label = tk.Label(self.root, image=self.bg_image)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                print("Background image loaded successfully.")
            else:
                print(f"Background image not found at {img_path}, using solid color.")
        except Exception as e:
            print(f"Error loading background image: {e}")

        # Ensure it's actually visible and centered
        self.root.update_idletasks()
        self.root.lift()
        self.root.grab_set()

        # UI Elements
        print("Adding UI elements...")
        main_frame = tk.Frame(self.root, bg=bg_color)
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        steps = [
            "1. Look 20 feet away",
            "2. Stand up and stretch",
            "3. Blink 20 times slowly"
        ]

        step_frame = tk.Frame(main_frame, bg=bg_color)
        step_frame.pack(pady=20)

        for step in steps:
            lbl = tk.Label(
                step_frame,
                text=step,
                font=("SF Pro Text", 28),
                fg="#8899AA",
                bg=bg_color,
                pady=10
            )
            lbl.pack()

        self.label_timer = tk.Label(
            main_frame,
            text=str(self.remaining),
            font=("SF Pro Display", 160, "bold"),
            fg="#E8F4FD",
            bg=bg_color
        )
        self.label_timer.pack(pady=40)

        print("Starting mainloop...")
        self._update_timer()
        self.root.mainloop()
        print("Mainloop exited")

    def _update_timer(self):
        if self.remaining > 0:
            self.remaining -= 1
            self.label_timer.config(text=str(self.remaining))
            self.root.after(1000, self._update_timer)
        else:
            self.root.destroy()
            if self.on_close:
                self.on_close()
