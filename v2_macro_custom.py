import tkinter as tk
from pynput import keyboard
from tkinter import filedialog
import time
import csv

class RECORD:
    def __init__(self):
        self.history = {}

    def record_key_press(self, char, press_time, release_time):
        if char in self.history:
            self.history[char].append((press_time, release_time))
        else:
            self.history[char] = [(press_time, release_time)]

    def print(self):
        print(self.history)

    def convert_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Character', 'Press-Release Pairs'])
            for char, times in self.history.items():
                row = [char]
                for press_time, release_time in times:
                    row.append((press_time, release_time))
                writer.writerow(row)

class RECORD_HANDLER:
    def __init__(self, bindings):
        self.is_recording = False
        self.record = RECORD()
        self.keys_pressed = {}
        self.start_time = time.time()
        self.bindings = bindings

    def reset(self):
        self.record = RECORD()
        self.keys_pressed = {}
        self.start_time = time.time()

    def on_press(self, key):
        current_time = time.time() - self.start_time

        char = key.char
        if char not in self.keys_pressed:
            self.keys_pressed[char] = current_time

    def on_release(self, key):
        current_time = time.time() - self.start_time
        char = key.char
        if char in self.keys_pressed:
            if self.check_binds(char): # true if recording is true
                press_time = self.keys_pressed[char]
                self.record.record_key_press(char, press_time, current_time)
                self.keys_pressed.pop(char)


    def check_binds(self, char):
        if char == self.bindings["print"]:
            self.record.print()
            return False
        if char == self.bindings["begin_recording"]:
            print("Starting recording...")
            self.reset()
            self.is_recording = True
            return False
        if char == self.bindings["stop_recording"]:
            print("Recording stopped...")
            self.is_recording = False
            return False
        if char == self.bindings["save_recording"]:
            print("Saving...")
            self.record.convert_to_csv("test.csv")
            return False
        return self.is_recording

class MASTER:
    def __init__(self):
        self.bindings = {"print" : 'q', "begin_recording" : 'w', "stop_recording" : 'e',"save_recording" : 'r'}
        self.record_handler = RECORD_HANDLER(self.bindings)

    def on_press(self, key):
        if hasattr(key, "char"):
            if key.char =='x':
                    return False
            self.record_handler.on_press(key)

    def on_release(self, key):
        if hasattr(key, "char"):
            self.record_handler.on_release(key)


master = MASTER()
with keyboard.Listener(on_press=master.on_press, on_release=master.on_release) as listener:
    listener.join()
