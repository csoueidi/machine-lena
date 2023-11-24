

import sys
from pathlib import Path

# Adding the parent directory to sys.path
parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

from choreography.ChoreographyParser import ChoreographyParser
from choreography.ChoreographyVisitor import ChoreographyVisitor
import time

class MyChoreographyVisitor(ChoreographyVisitor):
    def __init__(self, motors):
        self.motors = motors 
        pass

    def visitMoveCommand(self, ctx: ChoreographyParser.MoveCommandContext):
        motor_id = ctx.motor().getText() if ctx.motor() else "all"
        degree = float(ctx.degree().getText())
        speed = float(ctx.speed().getText()) if ctx.speed() else None

        if motor_id == "all":
            for motor in self.motors.values():
                if speed is not None:
                    motor.move(degree, speed)                    
                else:
                    motor.move(degree)
        else:      
            motor = self.motors.get(int(motor_id))
            if speed is not None:
                motor.move(degree, speed)
            else:
                motor.move(degree)
 
    def check_motors_finished(self):
        all_motors_reached_target = False
        while not all_motors_reached_target:
            time.sleep(0.01)
            all_motors_reached_target = True
            for motor in self.motors.values():
                if motor.isExecuting:
                    all_motors_reached_target = False
                    break    
 
    def visitSyncCommand(self, ctx:ChoreographyParser.SyncCommandContext):
        self.check_motors_finished()
        for moveCmd in ctx.moveCommand():
            self.visit(moveCmd)
        self.check_motors_finished()    
        print("Synchronized move commands executed")
        # Additional synchronization logic goes here

    
    def visitRepeatCommand(self, ctx:ChoreographyParser.RepeatCommandContext):
        times = int(ctx.times().getText())
        for _ in range(times):
            for cmd in ctx.command():
                self.visit(cmd)
        print(f"Repeated commands {times} times")

 
    def visitSetFrpsCommand(self, ctx:ChoreographyParser.SetFrpsCommandContext):
        speed =  float(ctx.speed().getText())
        print(f"Set FRPS to {speed}")
        for motor in self.motors.values():
            motor.speed_frps(speed)
        
 
    def visitWaitCommand(self, ctx:ChoreographyParser.WaitCommandContext):
        seconds = float(ctx.seconds().getText())
        print(f"Waiting for {seconds} seconds")
        time.sleep(seconds)
        # More logic if necessary
    

    

