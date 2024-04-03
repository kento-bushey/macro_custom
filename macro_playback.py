import csv 
import time
import threading
from pynput import keyboard
from pynput.keyboard import Controller, Key

def run_playback(letter, keystrokes):
    keyboard = Controller()
    if len(keystrokes)==0:
        return
    curr_wait = 0
    prev_release = 0
    for i in range(len(keystrokes)):
        press_time= keystrokes[i][0]
        release_time = keystrokes[i][1]

        curr_wait = press_time-prev_release
        
        time.sleep(curr_wait)

        hold_time = release_time - press_time

        keyboard.press(letter)
        time.sleep(hold_time)
        keyboard.release(letter)

        prev_release = release_time

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

class PLAYBACK():
    def __init__(self):
        filename = "test.csv"
        self.letters, self.history = import_csv(filename)
        self.threads = []
        self.pressed_keys = {}

    def on_press(self,key):
        if hasattr(key, "char"):
            if key.char == 'x':
                return False
            if key.char == 'q' and not 'q' in self.pressed_keys:
                self.run()
                self.pressed_keys['q'] = True
                self.threads = []

    def on_release(self,key):
        if hasattr(key, "char"):
            if key.char == 'q' and 'q' in self.pressed_keys:
                self.pressed_keys.pop('q')

    def run(self):
        for i in range(len(self.letters)):
            self.threads.append(threading.Thread(target=run_playback, args=(self.letters[i], self.history[i])))
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()

playback = PLAYBACK()

with keyboard.Listener(on_press=playback.on_press, on_release=playback.on_release) as listener:
    listener.join()
