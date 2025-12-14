import yaml
import sys
from pathlib import Path
import os

parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

from stepper.stepper import Stepper

current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, 'config1.yaml')

def get_motors_map():
   
    motor_config = load_config(config_path)
    return create_motors_map(motor_config)   

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
        return config

def create_motors(config):
    motors = {}
    for name, settings in config['motors'].items():
        motors[name] = Stepper(
            step_pin=settings['step_pin'],
            dir_pin=settings['dir_pin'],
            steps_per_rev=settings['steps_per_rev'],
            speed_sps=settings['steps_per_second'],
            max_deg=settings.get('max_deg', 360),  # Default to 360 degrees if not specified
            min_deg=settings.get('min_deg', 0),    # Default to 0 degrees if not specified
            invert_dir=settings.get('inverted', False),  # Default to False if not specified
            initial_position=settings.get('initial_position', 0),
            led_pin=settings.get('led_pin', None)
        )
    return motors

def create_motors_map(config):
    motors = {}
    for name, settings in config['motors'].items():
        motor_name = int(name)  # Convert the name to an integer
        motors[motor_name] = Stepper(
            step_pin=settings['step_pin'],
            dir_pin=settings['dir_pin'],
            steps_per_rev=settings['steps_per_rev'],
            speed_sps=settings['steps_per_second'],
            max_deg=settings.get('max_deg', 360),
            min_deg=settings.get('min_deg', 0),
            invert_dir=settings.get('inverted', False),
            motor_name = motor_name,
            initial_position=settings.get('initial_position', 0),
            led_pin=settings.get('led_pin', None)
        )
    return motors    


def update_initial_position(motor_name, new_initial_position):
    # Load the current configuration
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Check if the specified motor exists in the configuration
    if motor_name in config['motors']:
        # Update the initial position for the specified motor
        config['motors'][motor_name]['initial_position'] = new_initial_position
    else:
        print(f"Motor {motor_name} not found in the configuration.")
        return

    # Write the updated configuration back to the file
    with open(config_path, 'w') as file:
        yaml.safe_dump(config, file, default_flow_style=False)

 




# pip install pyyaml
