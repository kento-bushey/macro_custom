from pynput.keyboard import Controller
import time

def type_phrase(phrase):
    keyboard = Controller()

    # Type each character in the phrase
    for char in phrase:
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(0.1)  # Add a small delay between key presses

# Example phrase to type
phrase_to_type = "Hello, world!"

# Call the function to type the phrase
type_phrase(phrase_to_type)
