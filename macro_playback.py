import csv 
import time
import threading
from pynput import keyboard
from pynput.keyboard import Controller, Key
import math

global_stop = False

def run_playback(commands):
    keyboard = Controller()
    start_time = time.perf_counter()  # Get the start time
    for command in commands:
        if global_stop:  # Check if global_stop flag is set
            print("playback stopped.")
            return
        action, key, timestamp = command
        target_time = start_time + timestamp  # Calculate the absolute time for the command
        
        # Wait until the target time is reached
        while time.perf_counter() < target_time:
            pass
        
        # Perform the action
        if action == 'press':
            keyboard.press(key)
        elif action == 'release':
            keyboard.release(key)
    
    print("Playback finished.")

def import_csv(filename):
    letters = []
    keypress_info = []

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            letter = row[0]
            press_release_pairs = [eval(pair) for pair in row[1:]]
            letters.append(letter)
            keypress_info.append(press_release_pairs)

    return letters, keypress_info

def compile_history(letters, history):
    MAX_INTEGER = math.inf
    commands = []
    letter_index = [0] * len(letters)  # Initialize letter index with zeros
    
    while True:
        for i, index in enumerate(letter_index):
            if index > 2 * len(history[i]) - 1:
                letter_index[i] = -1
        
        if max(letter_index) == -1:
            return commands
        
        small_times = [MAX_INTEGER if index == -1 else history[i][index // 2][index % 2 == 1] for i, index in enumerate(letter_index)]
        action_time = min(small_times)
        next_action_index = small_times.index(action_time)
        release = letter_index[next_action_index] % 2 == 1
        action = 'release' if release else 'press'
        commands.append([action, letters[next_action_index], action_time])
        letter_index[next_action_index] += 1

class PLAYBACK():
    def __init__(self):
        filename = "test.csv"
        self.letters, self.history = import_csv(filename)
        self.thread = None
        self.pressed_keys = {}

    def on_press(self, key):
        global global_stop
        if hasattr(key, "char"):
            if key.char == 'z':  # Set global_stop flag to stop playback
                global_stop = True
            if key.char == 'x':  # Set global_stop flag to stop playback and exit
                global_stop = True
                return False
            if key.char == 'q' and 'q' not in self.pressed_keys:  # Start playback if 'q' is pressed and not already pressed
                self.run()
                self.pressed_keys['q'] = True

    def on_release(self, key):
        if hasattr(key, "char"):
            if key.char == 'q' and 'q' in self.pressed_keys:  # Remove 'q' from pressed_keys if released
                self.pressed_keys.pop('q')

    def run(self):
        global global_stop
        if self.thread and self.thread.is_alive():  # If thread is running, wait for it to finish
            self.thread.join()
        commands = compile_history(self.letters, self.history)
        global_stop = False  # Reset global_stop flag
        self.thread = threading.Thread(target=run_playback, args=(commands,))
        self.thread.start()  # Start the playback in a separate thread

playback = PLAYBACK()

with keyboard.Listener(on_press=playback.on_press, on_release=playback.on_release) as listener:
    listener.join()
