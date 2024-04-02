import tkinter as tk
from pynput import keyboard
from tkinter import filedialog
import time
import csv

class Recording:
    def __init__(self):
        self.records = {}
        self.start = time.time()
        self.stop = time.time()
        self.recording = False

    def reset(self):
        self.records = {}
        self.start = time.time()
        self.stop = time.time()

    def begin_recording(self):
        self.recording = True
        self.start = time.time()

    def stop_recording(self):
        self.recording = False
        self.stop = time.time()

    def record_key_press(self, char):
        timestamp = time.time() - self.start
        if char in self.records:
            self.records[char].append([timestamp])
        else:
            self.records[char] = [timestamp]

    def record_key_release(self, char):
        timestamp = time.time() - self.start
        if char in self.records:
            last_index = len(self.records[char]) - 1
            self.records[char].append(timestamp)

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Key', 'Timestamps'])
            for key, timestamps in self.records.items():
                row = [key] + timestamps  # Combine key with list of timestamps
                writer.writerow(row)

    def print_record(self):
        print(self.records)

class KeyRecord:
    def __init__(self):
        self.start_key = 'q'
        self.stop_key = 'w'
        self.recording = False 
        self.key_pressed = {}
        self.record = Recording()
        self.listening = True   # if listening is true, then we can start recording when the start recording button is pressed

    def on_press(self, key):
        if self.listening:
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
                        first_press = True
                        if key.char in self.key_pressed:
                            if self.key_pressed[key.char] == True:
                                first_press = False
                        if self.recording and first_press:
                            self.record.record_key_press(key.char)
                        self.key_pressed[key.char] = True

            except AttributeError:
                pass

    def on_release(self, key):
        try:
            if hasattr(key, 'char'):
                if self.recording:
                    self.record.record_key_release(key.char)
                self.key_pressed[key.char] = False
        except AttributeError:
            pass

    def start_recording(self):
        self.recording = True
        print("Recording started...")
        self.record.begin_recording()
        self.record.reset()
        

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
        file_menu.add_command(label="Save", command=self.save_to_csv_dialog)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)

        self.start_key_label = tk.Label(self.root, text=f"Current start button: '{self.key_record.start_key}'")
        self.start_key_label.pack(pady=5)

        start_key_button = tk.Button(self.root, text="Change start button", command=lambda: self.change_button("start"))
        start_key_button.pack(pady=5)

        self.stop_key_label = tk.Label(self.root, text=f"Current stop button: '{self.key_record.stop_key}'")
        self.stop_key_label.pack(pady=5)

        stop_key_button = tk.Button(self.root, text="Change stop button", command=lambda: self.change_button("stop"))
        stop_key_button.pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def change_button(self, button_type):
        self.key_record.listening = False
        if button_type == "start":
            self.start_key_label.config(text="Press any key to change")
            self.root.bind("<Key>", lambda event: self.rebind_and_check_release(event, "start"))
        elif button_type == "stop":
            self.stop_key_label.config(text="Press any key to change")
            self.root.bind("<Key>", lambda event: self.rebind_and_check_release(event, "stop"))

    def rebind_and_check_release(self, event, button_type):
        self.rebind(event, button_type)
        if self.all_keys_released():
            self.key_record.listening = True

    def rebind(self, event, button_type):
        if button_type == "start":
            self.key_record.start_key = event.char
            self.start_key_label.config(text=f"Start button changed to '{self.key_record.start_key}'")
        elif button_type == "stop":
            self.key_record.stop_key = event.char
            self.stop_key_label.config(text=f"Stop button changed to '{self.key_record.stop_key}'")

        self.root.unbind("<Key>")

    def on_closing(self):
        self.root.destroy()

    def save_to_csv_dialog(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            self.key_record.record.save_to_csv(filename)

    def all_keys_released(self):
        return not any(self.key_record.key_pressed.values())

if __name__ == "__main__":
    key_record = KeyRecord()
    listener = keyboard.Listener(on_press=key_record.on_press, on_release=key_record.on_release)
    listener.start()
    gui = GUI(key_record)
    gui.root.mainloop()
