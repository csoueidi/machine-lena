import sys
from pathlib import Path

# Adding the parent directory to sys.path
parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

from antlr4 import *
from choreography.ChoreographyLexer import ChoreographyLexer
from choreography.ChoreographyParser import ChoreographyParser
from MyChoreographyVisitor import MyChoreographyVisitor
import config
import time



motor_config = config.load_config('/home/pi/demo/code/machine/config1.yaml')
    
    # motor_config = config.load_config('/home/pi/demo/code/machine/config1.yaml')
motors = config.create_motors_map(motor_config)   

def main():
    # Read input from file
    with open("/home/pi/demo/code/test/sample.chor", "r") as file:
        input_stream = InputStream(file.read())

    # Create a lexer and parser
    lexer = ChoreographyLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ChoreographyParser(stream)

    # Parse the input and create a parse tree
    tree = parser.choreography()

    # Create and apply the visitor
    visitor = MyChoreographyVisitor(motors)
    visitor.visit(tree)

    check_motors_finished()
    for motor_id, motor in motors.items():
        # Call some method on each motor
        print(f"Stopping motor {motor_id} pos {motor.get_pos()} angle {motor.get_pos_deg()}" )
        motor.stop()

 
    print("All motors have reached their target positions.")

def check_motors_finished():
    all_motors_reached_target = False
    while not all_motors_reached_target:
        time.sleep(0.01)
        all_motors_reached_target = True
        for motor in motors.values():
            if motor.isExecuting:
                all_motors_reached_target = False
                break

if __name__ == "__main__":
    main()


 