 
# Commands
 
java -jar binaries/antlr-4.13.1-complete.jar -Dlanguage=Python3 -no-listener -visitor choreography/Choreography.g4

pip3 install antlr4-python3-runtime  



pip install flask-cors

pip install flask


python3 -m http.server 8001



# File management
import os
import config  # Assuming this is your custom module for loading configs

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the config file
config_path = os.path.join(current_dir, '..', 'config', 'config1.yaml')

# Load the config
motor_config = config.load_config(config_path)

