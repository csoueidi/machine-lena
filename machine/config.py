import yaml
from stepper import Stepper

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
            invert_dir=settings.get('inverted', False)  # Default to False if not specified
        

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
            invert_dir=settings.get('inverted', False)
        )
    return motors    
    


# pip install pyyaml
