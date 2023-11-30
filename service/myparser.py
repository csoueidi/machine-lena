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
from choreography.NewChoreographyVisitor import NewChoreographyVisitor
from choreography.StopParsingException import StopParsingException
from choreography.CustomErrorListener import CustomErrorListener
import config.config as config
import time

class MyParser:
    def __init__(self):
            self.motors = config.get_motors_map()
            self.visitor = None

    def stop(self):
        if self.visitor is not None:
            self.visitor.stop_flag = True

    def pause(self):
        if self.visitor is not None:
            self.visitor.pause_flag.set()   

    def resume(self):
        if self.visitor is not None:
            self.visitor.pause_flag.clear()             

    def execute(self, file_path, filename):
 
        with open(file_path, "r") as file:
            input_stream = InputStream(file.read())

        # Create a lexer and parser
        lexer = ChoreographyLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = ChoreographyParser(stream)
        parser.removeErrorListeners()  # Remove default listeners
        parser.addErrorListener(CustomErrorListener()) 
 
        start_time = time.time()
        try:
            tree = parser.choreography()
            self.visitor = NewChoreographyVisitor(self.motors, mock=False)
            self.visitor.visit(tree)
        except StopParsingException:
            print("Execution was stopped.")
            for motor_id, motor in self.motors.items():
                motor.stop()
            return "Execution of " + filename + " was stopped after " + str(round(time.time() - start_time)) + " seconds."

        except Exception as e:  # This will catch syntax errors from the custom listener
            print(f"Error occurred during parsing: {e}")
            return "Bad syntax in " + filename
            # Handle the exception as needed
    

    

        self.check_motors_finished()

        for motor_id, motor in self.motors.items():
            # Call some method on each motor
            # print(f"Stopping motor {motor_id} pos {motor.get_pos()} angle {motor.get_pos_deg()}" )
            motor.stop()

        print("All motors stopped naturally")
        return "Executed " + filename + " in " + str(round(time.time() - start_time)) + " seconds."
         
    def check_motors_finished(self):
        all_motors_reached_target = False
        while not all_motors_reached_target:
            time.sleep(0.01)
            all_motors_reached_target = True
            for motor in self.motors.values():
                if motor.isExecuting:
                    all_motors_reached_target = False
                    break
    
    