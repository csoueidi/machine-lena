

import sys
from pathlib import Path

# Adding the parent directory to sys.path
parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

from choreography.ChoreographyParser import ChoreographyParser
from choreography.ChoreographyVisitor import ChoreographyVisitor
import time
import machine.config





class MyChoreographyVisitor(ChoreographyVisitor):
    def __init__(self):
        # Initialize any necessary variables
        motor_config = config.load_config('/home/pi/demo/code/machine/config1.yaml')
        self.motors = config.create_motors_map(motor_config)     
        pass

    def visitMoveCommand(self, ctx: ChoreographyParser.MoveCommandContext):
        motor = ctx.motor().getText() if ctx.motor() else "all"
        degree = ctx.degree().getText()
        speed = float(ctx.speed().getText()) if ctx.speed() else None

        if motor == "all":
            
             # Handle the move command with optional speed
            if speed is not None:
                print(f"Moving all motors to {degree} degrees at speed {speed}")
            else:
                print(f"Moving all motors to {degree} degrees at last speed")
        else:           
            if speed is not None:
                print(f"Moving motor {motor} to {degree} degrees at speed {speed}")
            else:
                 print(f"Moving motor {motor} to {degree} degrees at last speed")
 
        
      

    # Visit a parse tree produced by ChoreographyParser#syncCommand.
    def visitSyncCommand(self, ctx:ChoreographyParser.SyncCommandContext):
        for moveCmd in ctx.moveCommand():
            self.visit(moveCmd)
        print("Synchronized move commands executed")
        # Additional synchronization logic goes here

    # Visit a parse tree produced by ChoreographyParser#repeatCommand.
    def visitRepeatCommand(self, ctx:ChoreographyParser.RepeatCommandContext):
        times = int(ctx.times().getText())
        for _ in range(times):
            for cmd in ctx.command():
                self.visit(cmd)
        print(f"Repeated commands {times} times")

   # Visit a parse tree produced by ChoreographyParser#setFrpsCommand.
    def visitSetFrpsCommand(self, ctx:ChoreographyParser.SetFrpsCommandContext):
        speed = ctx.speed().getText()
        print(f"Set FRPS to {speed}")
        # Implement the logic to handle the FRPS setting
 

     # Visit a parse tree produced by ChoreographyParser#waitCommand.
    def visitWaitCommand(self, ctx:ChoreographyParser.WaitCommandContext):
        seconds = float(ctx.seconds().getText())
        print(f"Waiting for {seconds} seconds")
        time.sleep(seconds)
        # More logic if necessary
    

    

