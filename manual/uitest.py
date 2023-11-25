import tkinter as tk
from TB6560Interface import TB6560Interface
import threading

# Initialize TB6560Interface and set speed
io = TB6560Interface()
current_speed = 1000
stepSize = 15
io.setSpeed(current_speed)
moving = False

# Function definitions for button commands
def move(direction):
    global moving
    while moving:
        if direction == 'left':
            io.setSpeed(current_speed)
            io.moveOneBySteps('x', stepSize)
        elif direction == 'right':
            io.setSpeed(-current_speed)
            io.moveOneBySteps('x', stepSize)

def start_move_left(event):
    global moving
    moving = True
    threading.Thread(target=move, args=('left',)).start()

def start_move_right(event):
    global moving
    moving = True
    threading.Thread(target=move, args=('right',)).start()

def stop_move(event):
    global moving
    moving = False

def increase_speed():
    global current_speed
    current_speed += 10
    io.setSpeed(current_speed)

def decrease_speed():
    global current_speed
    current_speed = max(0, current_speed - 10)  # Prevent negative speed
    io.setSpeed(current_speed)

# Create the main window
root = tk.Tk()
root.title("Motor Control")

# Bind key events
root.bind('<KeyPress-a>', start_move_left)
root.bind('<KeyPress-d>', start_move_right)
root.bind('<KeyRelease-a>', stop_move)
root.bind('<KeyRelease-d>', stop_move)


# Create and place buttons
btn_move_left = tk.Button(root, text='Move Left (a)', command=start_move_left, repeatdelay=100, repeatinterval=100)
btn_move_left.pack()

btn_move_right = tk.Button(root, text='Move Right (d)', command=start_move_right, repeatdelay=100, repeatinterval=100)
btn_move_right.pack()

# Create and place buttons
btn_increase_speed = tk.Button(root, text='Increase Speed (w)', command=increase_speed)
btn_increase_speed.pack()

btn_decrease_speed = tk.Button(root, text='Decrease Speed (s)', command=decrease_speed)
btn_decrease_speed.pack()

# Run the application
root.mainloop()
