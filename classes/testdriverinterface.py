from TB6560Interface import TB6560Interface
import time
from pynput.keyboard import Key, Listener

# Assuming TB6560Interface is already defined and imported
io = TB6560Interface()

# Initialize the speed
current_speed = 10000
stepSize=50;
io.setSpeed(current_speed)
# io.moveOneBySteps('x', 1)
print("Press 'a', 'd', 'w', or 's' to control the motor. Press 'q' to quit.")
x=0

def on_press(key):
    global current_speed
    global x
    x = x + 1
    if x % 20 != 0:
        pass
    try:
        if key.char == 'q':
            print("Program exiting.")
            return False  # Stop listener
        elif key.char == 'a':
            io.setSpeed(current_speed)
            io.moveOneBySteps('x', stepSize)
        elif key.char == 'd':
            io.setSpeed(-current_speed)
            io.moveOneBySteps('x', stepSize)
        elif key.char == 'w':
            current_speed += 10  # Increase speed
            io.setSpeed(current_speed)
        elif key.char == 's':
            current_speed -= 10  # Decrease speed
            io.setSpeed(current_speed)
    except AttributeError:
        pass  # Special keys (like arrow keys) will be ignored

def on_release(key):
    try:
        if key.char in ['a', 'd']:
            # Stop the motor when 'a' or 'd' is released
            io.setSpeed(0)
    except AttributeError:
        pass  # Special keys (like arrow keys) will be ignored

# Collect events until released
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
