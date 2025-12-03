

import sys
from pathlib import Path
import threading

# Adding the parent directory to sys.path
parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

from choreography.ChoreographyParser import ChoreographyParser
from choreography.ChoreographyVisitor import ChoreographyVisitor
from choreography.StopParsingException import StopParsingException
import time 



class NewChoreographyVisitor(ChoreographyVisitor):
    def __init__(self, motors, mock=False, filename=None, debug_logger=None):
        self.motors = motors 
        self.mock = mock
        self.frps = 0
        self.pause_flag = threading.Event()
        self.stop_flag = False
        self.current_line = None
        self.current_command = None
        self.filename = filename
        self.execution_logs = []
        self.debug_logger = debug_logger
    
    def log_debug(self, message):
        """Log to debug file if logger is available"""
        if self.debug_logger:
            self.debug_logger.info(message)

    def check_control_flags(self):
        # Check if the process should be paused
        if self.pause_flag.is_set():
            self.pause_flag.wait()  # Wait until the flag is cleared to resume

        # Check if the process should be stopped
        if self.stop_flag:
            raise StopParsingException("Stopping the parsing process")  # Custom exception to stop parsing


    def visitMoveCommand(self, ctx: ChoreographyParser.MoveCommandContext):
        self.check_control_flags()
        self.current_line = ctx.start.line
        self.current_command = ctx.getText()
        
        start_time = time.time()
        
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
                    motor.move(degree, self.frps)
        
        else:      
            motor = self.motors.get(int(motor_id))
            if speed is not None:
                motor.move(degree, speed)
            else:
                motor.move(degree)
        
        elapsed = round(time.time() - start_time, 3)
        log_entry = f"[{self.filename}] Line {self.current_line}: move motor {motor_id} {degree}% ({elapsed}s)"
        self.execution_logs.append(log_entry)
        print(log_entry)
        self.log_debug(log_entry)
 
    def wait_motors_to_finish(self):
        all_motors_reached_target = False
        while not all_motors_reached_target:
            time.sleep(0.01)
            all_motors_reached_target = True
            for motor in self.motors.values():
                if motor.isExecuting:
                    all_motors_reached_target = False
                    break
 
    def visitSyncCommand(self, ctx:ChoreographyParser.SyncCommandContext):
        self.check_control_flags()
        self.current_line = ctx.start.line
        self.current_command = "sync"
        
        start_time = time.time()
        
        self.wait_motors_to_finish()
        for moveCmd in ctx.moveCommand():
            self.visit(moveCmd)
        self.wait_motors_to_finish()    

        elapsed = round(time.time() - start_time, 3)
        log_entry = f"[{self.filename}] Line {self.current_line}: sync command ({elapsed}s)"
        self.execution_logs.append(log_entry)
        print(log_entry)
        self.log_debug(log_entry)

        if self.mock:
            print("Synchronized move commands executed")

    
    def visitRepeatCommand(self, ctx:ChoreographyParser.RepeatCommandContext):
        self.check_control_flags()
        self.current_line = ctx.start.line
        self.current_command = ctx.getText()
        
        times = int(ctx.times().getText())
        for _ in range(times):
            for cmd in ctx.command():
                self.visit(cmd)
        if self.mock:
            print(f"Repeated commands {times} times")        
        

 
    def visitSetFrpsCommand(self, ctx:ChoreographyParser.SetFrpsCommandContext):
        self.check_control_flags()
        self.current_line = ctx.start.line
        self.current_command = ctx.getText()
        
        start_time = time.time()
        speed =  float(ctx.speed().getText())
        self.frps = speed
        for motor in self.motors.values():
            motor.speed_frps(speed)
        
        elapsed = round(time.time() - start_time, 3)
        log_entry = f"[{self.filename}] Line {self.current_line}: set speed {speed} frps ({elapsed}s)"
        self.execution_logs.append(log_entry)
        print(log_entry)
        self.log_debug(log_entry)
        
        if self.mock:
            print(f"Set FRPS to {speed}")    
        
 
    def visitWaitCommand(self, ctx:ChoreographyParser.WaitCommandContext):
        self.check_control_flags()
        self.current_line = ctx.start.line
        self.current_command = ctx.getText()
        
        start_time = time.time()
        seconds = float(ctx.seconds().getText())
        time.sleep(seconds)
        self.wait_motors_to_finish()
        
        elapsed = round(time.time() - start_time, 3)
        log_entry = f"[{self.filename}] Line {self.current_line}: wait {seconds}s ({elapsed}s)"
        self.execution_logs.append(log_entry)
        print(log_entry)
        self.log_debug(log_entry)
        
        if self.mock:
            print(f"Waiting for {seconds} seconds")
    

    

