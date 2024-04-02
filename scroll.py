import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar_h = ttk.Scrollbar(self, orient="horizontal",cursor= "tcross", command=canvas.xview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar_h.set)
        scrollbar_h.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        # Draw a rectangle on the canvas
        for i in range(6):
            canvas.create_rectangle(0, (i-1)*50, 3000, i*50, fill="blue")
        

# Test the ScrollableFrame
root = tk.Tk()
root.title("Scrollable Frame Test")

scrollable_frame = ScrollableFrame(root)
scrollable_frame.pack(fill="both", expand=True, pady=10, padx=10)

label = ttk.Label(root, text="Some text below the canvas")
label.pack(pady=25)

# Set the base size of the window
root.geometry("800x400")

root.mainloop()
