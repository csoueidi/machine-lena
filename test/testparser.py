import sys
from pathlib import Path
import os
import time
 

# Adding the parent directory to sys.path
parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

from antlr4 import *
from choreography.ChoreographyLexer import ChoreographyLexer
from choreography.ChoreographyParser import ChoreographyParser
from choreography.MyChoreographyVisitor import MyChoreographyVisitor
import config.config as config
import time


motors = config.get_motors_map()

def main():
      # Check if an argument is provided
    if len(sys.argv) < 2:
        print("Usage: test.py <path_to_chor_file>")
        sys.exit(1)

    # Get the file path from the command line argument
    file_name = sys.argv[1]
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    chor_path = os.path.join(current_dir, file_name)
    with open(chor_path, "r") as file:
        input_stream = InputStream(file.read())

    # Create a lexer and parser
    lexer = ChoreographyLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ChoreographyParser(stream)

    # Parse the input and create a parse tree
    tree = parser.choreography()

    # Create and apply the visitor
    visitor = MyChoreographyVisitor(motors, mock=False)
    # Start the timer
    start_time = time.time()

    visitor.visit(tree)

   

    check_motors_finished()
    for motor_id, motor in motors.items():
        # Call some method on each motor
        # print(f"Stopping motor {motor_id} pos {motor.get_pos()} angle {motor.get_pos_deg()}" )
        motor.stop()
        print("All motors stopped")

    end_time = time.time()
    duration = end_time - start_time
    print(f"Time taken for {file_name} : {duration} seconds")
 
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


 