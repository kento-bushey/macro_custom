import threading
import time
from pynput.keyboard import Controller

# Function to simulate keyboard input
def simulate_input(key, interval):
    keyboard = Controller()
    for i in range(3):
        keyboard.press(key)
        keyboard.release(key)  # Convert key to string and type it
        time.sleep(interval)  # Wait for the specified interval

# Create threads for typing '1' and '2' with different intervals
thread1 = threading.Thread(target=simulate_input, args=('1', 1))  # Typing '1' every 1 second
thread2 = threading.Thread(target=simulate_input, args=('2', 2))  # Typing '2' every 2 seconds

# Start the threads
thread1.start()
thread2.start()

# Wait for the threads to finish (which will never happen in this case)
thread1.join()
thread2.join()
