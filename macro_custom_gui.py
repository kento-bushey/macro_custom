import tkinter as tk
from pynput import keyboard
import time
import csv

class Recording:
    def __init__(self):
        self.records = {}
        self.start = time.time()
        self.stop = time.time()
        self.recording = False

    def begin_recording(self):
        self.recording = True
        self.start = time.time()

    def stop_recording(self):
        self.recording = False
        self.stop = time.time()

    def record_key_press(self, char):
        timestamp = time.time() - self.start
        if char in self.records:
            self.records[char].append(timestamp)
        else:
            self.records[char] = [timestamp]

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Key', 'Timestamp'])
            for key, timestamps in self.records.items():
                for timestamp in timestamps:
                    writer.writerow([key, timestamp])

    def print_record(self):
        print(self.records)

class KeyRecord:
    def __init__(self):
        self.start_key = 'q'
        self.stop_key = 'w'
        self.recording = False
        self.key_pressed = {}
        self.record = Recording()

    def on_press(self, key):
        try:
            if hasattr(key, 'char'):
                if key.char == self.start_key:
                    if not self.key_pressed.get(self.start_key, False):
                        self.key_pressed[self.start_key] = True
                        if not self.recording:
                            self.start_recording()

                elif key.char == self.stop_key:
                    if not self.key_pressed.get(self.stop_key, False):
                        self.key_pressed[self.stop_key] = True
                        if self.recording:
                            self.stop_recording()

                else:
                    self.key_pressed[key.char] = True
                
                    if self.recording:
                        self.record.record_key_press(key.char)

        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if hasattr(key, 'char'):
                if key.char in [self.start_key, self.stop_key]:
                    self.key_pressed[key.char] = False
                else:
                    self.key_pressed.pop(key.char, None)
        except AttributeError:
            pass

    def start_recording(self):
        self.recording = True
        print("Recording started...")
        self.record.begin_recording()
        

    def stop_recording(self):
        self.recording = False
        print("Recording stopped...")
        self.record.stop_recording()
        self.record.print_record()

class GUI:
    def __init__(self, key_record):
        self.key_record = key_record
        self.root = tk.Tk()
        self.root.title("Keyboard Recorder")
        self.root.geometry("400x300")

        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)

        self.start_key_label = tk.Label(self.root, text=f"Current start button: '{self.key_record.start_key}'")
        self.start_key_label.pack(pady=5)

        start_key_button = tk.Button(self.root, text="Change start button", command=self.change_start_button)
        start_key_button.pack(pady=5)

        self.stop_key_label = tk.Label(self.root, text=f"Current start button: '{self.key_record.stop_key}'")
        self.stop_key_label.pack(pady=5)

        stop_key_button = tk.Button(self.root, text="Change stop button", command=self.change_stop_button)
        stop_key_button.pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def change_start_button(self):
        self.start_key_label.config(text="Press any key to change")
        self.root.bind("<Key>", lambda event: self.rebind(event, "start"))

    def change_stop_button(self):
        self.stop_key_label.config(text="Press any key to change")
        self.root.bind("<Key>", lambda event: self.rebind(event, "stop"))

    def rebind(self, event, key):
        if key == "start":
            self.key_record.start_key = event.char
            self.start_key_label.config(text=f"Start button changed to '{self.key_record.start_key}'")
        elif key == "stop":
            self.key_record.stop_key = event.char
            self.stop_key_label.config(text=f"Stop button changed to '{self.key_record.stop_key}'")

        self.root.unbind("<Key>")

    def on_closing(self):
        self.root.destroy()


if __name__ == "__main__":
    key_record = KeyRecord()
    listener = keyboard.Listener(on_press=key_record.on_press, on_release=key_record.on_release)
    listener.start()
    gui = GUI(key_record)
    gui.root.mainloop()
