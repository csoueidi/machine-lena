import config
import time
from threading import Thread

# Load motor configurations
motor_config = config.load_config('/home/pi/demo/code/machine/config1.yaml')
motors = config.create_motors_map(motor_config)

# Command Functions
def move_command(args):
    print(f"move command {args}")
    arm_id, position = args[0], args[1]
    speed = args[2] if len(args) > 2 else None

    if arm_id in motors:
        motor = motors.get(arm_id)
        if speed is not None:
            motor.move(position, speed)
        else:
            motor.move(position)

def sync(commands):
    threads = [Thread(target=command) for command in commands]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # Check if all motors have reached their target
    check_motors_finished()

def check_motors_finished():
    all_motors_reached_target = False
    while not all_motors_reached_target:
        time.sleep(0.01)
        all_motors_reached_target = True
        for motor in motors.values():
            if motor.isExecuting:
                all_motors_reached_target = False
                break

def repeat(times, commands):
    for _ in range(times):
        sync(commands)

def set_frps(speed):
    for motor in motors.values():
        motor.speed_frps(speed)  # Assuming your motor class has this method

# Choreography Parsing
def parse_choreography(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            parse_line(line.strip())

def parse_line(line):
    if not line or line.startswith('#'):
        return

    parts = line.split()
    command = parts[0]
    try:
        args = eval(' '.join(parts[1:]))  # Evaluate the rest of the line as a Python expression
    except Exception as e:
        print(f"Error parsing line: '{line}'")
        print(f"Exception: {e}")
        return

    if command == 'set_frps':
        set_frps(args)
    elif command == 'move':
        move_command(args)
    elif command == 'sync':
        command_functions = [lambda arg=arg: move_command(arg) for arg in args]
        sync(command_functions)
    elif command == 'repeat':
        if not isinstance(args, list) or len(args) != 2:
            print(f"Invalid format for repeat command: '{line}'")
            return

        repeat_count, repeat_blocks = args
        repeat_commands = []
        for block in repeat_blocks:
            if all(isinstance(item, list) for item in block):  # Check if all items are lists (indicating sync block)
                sync_commands = [lambda item=item: move_command(item) for item in block]
                repeat_commands.append(lambda: sync(sync_commands))
            else:
                print(f"Invalid format within repeat block: '{block}'")
                return
        repeat(repeat_count, repeat_commands)



# Execute Choreography
choreography_file = "/home/pi/demo/code/machine/ch1.txt"
parse_choreography(choreography_file)
