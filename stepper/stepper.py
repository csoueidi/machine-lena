import RPi.GPIO as GPIO
import threading
import time
import math
import queue
import sys
from pathlib import Path
import os

parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

import config.config as config

class Stepper:
    def __init__(self, step_pin, dir_pin, en_pin=None, steps_per_rev=200, speed_sps=10,  max_deg = 360, min_deg=0,invert_dir=False, motor_name=None, initial_position=0):
        
        GPIO.setmode(GPIO.BCM)
        # GPIO Configuration modes
        GPIO.setwarnings(False)
        GPIO.setup(step_pin, GPIO.OUT)
        GPIO.setup(dir_pin, GPIO.OUT)

        if motor_name is not None:
            self.motor_name = motor_name
            # print(f"Intiated motor {motor_name}")

        if en_pin is not None:
            GPIO.setup(en_pin, GPIO.OUT)
            GPIO.output(en_pin, GPIO.HIGH)

        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.en_pin = en_pin
        self.invert_dir = invert_dir

        self.steps_per_rev = steps_per_rev
        self.speed_sps = speed_sps
        self.target_pos = initial_position
        self.pos = initial_position
        self.update_rate = 1.0 / speed_sps

       
        self.max_deg = max_deg  
        self.maxsteps = max_deg * steps_per_rev / 360
      
 
       
        self.tasks = queue.Queue()
        self.running = False
        self.isExecuting = False
        self.pending_target_deg = self.get_pos_deg()  # Track the target after all queued moves
        self.timer = None
        self.track_target()
    
    def enqueue_item(self, degree, speed, is_move):
        # Enqueue a tuple containing degree and speed
        self.tasks.put((degree, speed,is_move))

    def dequeue_item(self):
        if not self.tasks.empty():
            return self.tasks.get()
        return None

 

    def speed(self, sps):
        self.speed_sps = sps
        self.update_rate = 1.0 / sps
        # if self.running:
        #     self.track_target()

    def speed_rps(self, rps):
        self.speed(rps * self.steps_per_rev)

    def speed_frps(self, frps):
        self.speed(frps * self.maxsteps)    

    def target(self, t):
        self.target_pos = t

    def get_position(self):
        nofrevstoopen = self.max_deg / 360.0
        maxpos = nofrevstoopen * self.steps_per_rev
        currentdegree = self.pos / maxpos
        return round(currentdegree, 2)



    def move(self, percentage, frps=None):
        
        # Check if percentage is between 0 and 1 (inclusive)
        if abs(percentage) > 1:
            percentage = 1
        elif percentage < 0:
            percentage = 0

        # Calculate absolute target degree
        target_degree = self.max_deg * percentage
        
        # Calculate relative movement from pending target (not current position)
        relative_degree = target_degree - self.pending_target_deg
        self.pending_target_deg = target_degree
        
        print(f"Motor {self.motor_name}: move({percentage}) -> target={target_degree}°, relative={relative_degree}°, pending={self.pending_target_deg}°")

        # Rest of your function logic goes here
        if frps is not None:
            self.enqueue_item(relative_degree, frps, False)
        else:
            self.enqueue_item(relative_degree, (self.speed_sps / self.maxsteps), False)


    def move_deg(self,deg,speed=None):        
        if speed is not None:
            self.enqueue_item(deg,speed, False)
        else:
            self.enqueue_item(deg, self.speed_sps, False)    
        



         
    def set_direction(self, d):
        self.invert_dir = d

    def target_rad(self, rad):
        self.target(self.steps_per_rev * rad / (2.0 * math.pi))

    def get_pos(self):
        return self.pos

    def get_pos_deg(self):
        return round(self.get_pos() * 360.0 / self.steps_per_rev)

    def get_pos_rad(self):
        return self.get_pos() * (2.0 * math.pi) / self.steps_per_rev

    def overwrite_pos(self, p):
        self.pos = p

    def overwrite_pos_deg(self, deg):
        self.overwrite_pos(deg * self.steps_per_rev / 360.0)

    def overwrite_pos_rad(self, rad):
        self.overwrite_pos(rad * self.steps_per_rev / (2.0 * math.pi))

    def enable(self, enable):
        if self.en_pin is not None:
            GPIO.output(self.en_pin, GPIO.HIGH if enable else GPIO.LOW)
        self.enabled = enable

    def is_enabled(self):
        return self.enabled

    def step(self, direction):         
        if direction > 0:
            GPIO.output(self.dir_pin, GPIO.HIGH if not self.invert_dir else GPIO.LOW)
        elif direction < 0:
            GPIO.output(self.dir_pin, GPIO.LOW if not self.invert_dir else GPIO.HIGH)

        GPIO.output(self.step_pin, GPIO.HIGH)
        time.sleep(0.00005)
        GPIO.output(self.step_pin, GPIO.LOW)
        time.sleep(0.00005)

        self.pos += direction
   
    
        # print("Moved to pos " + str(self.pos))
        # print(f"Position degree {self.get_pos_deg()}")
        # print(f"target_pos   {self.target_pos}")
        # print(f"self.pos {self.pos}")

    def target_deg(self, deg):
        # This method is called from the timer thread

        target_steps = self.steps_per_rev * deg / 360.0
        target_steps = math.ceil(target_steps)

        # print(f"target steps {target_steps}")
        # self.target_pos = self.pos + target_steps
        
        self.target_pos = math.ceil(max(0, min(self.pos + target_steps, self.maxsteps)))
       
        # print(f"Setting target pos  {self.target_pos}")

    def _timer_callback(self):
        while self.running:
            if(not self.isExecuting):
                item = self.dequeue_item()
                if item is not None:
                    degree, vel, is_move = item
                    # degree is already relative movement, no need to recalculate
                    print(f"Motor {self.motor_name}: Dequeued degree={degree}°, current_pos={self.get_pos_deg()}°")
                    velocity = vel * self.maxsteps    
                    self.speed(velocity)
                    self.target_deg(degree)

            if self.target_pos > self.pos:
                self.step(1)
                self.isExecuting = True
            elif self.target_pos < self.pos:
                self.step(-1)
                self.isExecuting = True
            else:
                self.isExecuting = False

            time.sleep(self.update_rate)

    def track_target(self):
        if self.timer is not None and self.timer.is_alive():
            self.running = False
            self.timer.join()

        self.running = True
        self.timer = threading.Thread(target=self._timer_callback)
        self.timer.start()

    def stop(self):
        if not self.running:
            return
        self.running = False
        if self.timer is not None and self.timer.is_alive():
            self.timer.join()

        config.update_initial_position(self.motor_name, self.pos)

        GPIO.output(self.step_pin, GPIO.LOW)
        GPIO.output(self.dir_pin, GPIO.LOW)
        if self.en_pin is not None:
            GPIO.output(self.en_pin, GPIO.LOW)

    def save_position(self):
        config.update_initial_position(self.motor_name, self.pos)

    def reset_motor(motor):
        # Move to home position or set current position as home
        motor.overwrite_pos(0)  # Setting current position as 'home'       

# Example usage
# stepper = Stepper(step_pin=17, dir_pin=27, en_pin=22)
# stepper.target_deg(90)
# time.sleep(5)
# stepper.stop()
# GPIO.cleanup()
