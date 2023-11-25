

import sys
from pathlib import Path

# Adding the parent directory to sys.path
parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

from choreography.ChoreographyParser import ChoreographyParser
from choreography.ChoreographyVisitor import ChoreographyVisitor
import time

class MyChoreographyVisitor(ChoreographyVisitor):
    def __init__(self, motors, mock=False):
        self.motors = motors 
        self.mock = mock

    def visitMoveCommand(self, ctx: ChoreographyParser.MoveCommandContext):
        motor_id = ctx.motor().getText() if ctx.motor() else "all"
        degree = float(ctx.degree().getText())
        speed = float(ctx.speed().getText()) if ctx.speed() else None

        if self.mock:
            print(f"Move motor {motor_id} {degree} degrees at speed {speed}")
        
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

        if self.mock:
            print("Synchronized move commands executed")

    
    def visitRepeatCommand(self, ctx:ChoreographyParser.RepeatCommandContext):
        times = int(ctx.times().getText())
        for _ in range(times):
            for cmd in ctx.command():
                self.visit(cmd)
        if self.mock:
            print(f"Repeated commands {times} times")        
        

 
    def visitSetFrpsCommand(self, ctx:ChoreographyParser.SetFrpsCommandContext):
        speed =  float(ctx.speed().getText())
        for motor in self.motors.values():
            motor.speed_frps(speed)
        if self.mock:
            print(f"Set FRPS to {speed}")    
        
 
    def visitWaitCommand(self, ctx:ChoreographyParser.WaitCommandContext):
        seconds = float(ctx.seconds().getText())
        time.sleep(seconds)
        if self.mock:
            print(f"Waiting for {seconds} seconds")
    

    

