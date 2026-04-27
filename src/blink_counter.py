import tkinter as tk

class BlinkAnimation:
    def __init__(self, canvas, count=20):
        self.canvas = canvas
        self.count = count
        self.eyes = []
        self.current_blink = 0
        self._setup_eyes()

    def _setup_eyes(self):
        # Calculate spacing for the eyes row
        canvas_width = self.canvas.winfo_width()
        if canvas_width <= 1: # Canvas not yet rendered
            canvas_width = 800

        margin = 50
        available_width = canvas_width - (2 * margin)
        spacing = available_width / self.count

        for i in range(self.count):
            x = margin + (i * spacing) + (spacing / 2)
            y = 400 # Center height - will be adjusted by overlay

            # Draw eye (ellipse)
            # We use two ovals for the open eye, or one flat one for closed
            eye = self.canvas.create_oval(x-15, y-10, x+15, y+10, fill="#E8F4FD", outline="#8899AA")
            self.eyes.append(eye)

    def blink_next(self):
        # Close the current eye (flatten it)
        idx = self.current_blink % self.count
        eye = self.eyes[idx]

        # Convert to closed state (flat line)
        self.canvas.coords(eye, self.canvas.coords(eye)[0],
                           (self.canvas.coords(eye)[1] + self.canvas.coords(eye)[3]) / 2,
                           self.canvas.coords(eye)[2],
                           (self.canvas.coords(eye)[1] + self.canvas.coords(eye)[3]) / 2)

        self.current_blink += 1

    def reset(self):
        self.current_blink = 0
        # This would require redrawing or updating coords of all eyes
