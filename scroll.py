import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar_v = ttk.Scrollbar(self, orient="vertical", cursor="sb_v_double_arrow", command=canvas.yview)
        scrollbar_h = ttk.Scrollbar(self, orient="horizontal", cursor="tcross", command=canvas.xview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        # Adjust for vertical scrollbar width
        scrollbar_v.pack(side="right", fill="y")
        scrollbar_h.pack(side="bottom", fill="x")
        canvas.pack(side="top",fill="x",  expand=True)
        
        # Draw a rectangle on the canvas
        for i in range(6):
            canvas.create_rectangle(0, (i-1)*40, 3000, i*40, fill="blue")
        


# Test the ScrollableFrame
root = tk.Tk()
root.title("Scrollable Frame Test")

scrollable_frame = ScrollableFrame(root)
scrollable_frame.pack(fill="both", expand=False, pady=10, padx=10)

begin_label = ttk.Label(root, text="Press Time: ")
begin_label.pack(pady=10, side = "left",expand=True)

begin_label = ttk.Label(root, text="Release Time: ")
begin_label.pack(pady=10, side = "left",expand=True)

def canvas_click(event):
    x = event.x
    y = event.y
    print(f"Clicked at ({x}, {y})")

root.bind("<Button-1>", canvas_click)

# Set the base size of the window
root.geometry("800x400")

root.mainloop()
