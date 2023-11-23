import RPi.GPIO as GPIO
import threading
import time
import math
import queue

class Stepper:
    def __init__(self, step_pin, dir_pin, en_pin=None, steps_per_rev=200, speed_sps=10,  max_deg = 360, min_deg=0,invert_dir=False):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(step_pin, GPIO.OUT)
        GPIO.setup(dir_pin, GPIO.OUT)

        if en_pin is not None:
            GPIO.setup(en_pin, GPIO.OUT)
            GPIO.output(en_pin, GPIO.HIGH)

        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.en_pin = en_pin
        self.invert_dir = invert_dir

        self.steps_per_rev = steps_per_rev
        self.speed_sps = speed_sps
        self.target_pos = 0
        self.pos = 0
        self.update_rate = 1.0 / speed_sps

        self.max_steps = max_deg * steps_per_rev / 360
        self.min_steps = min_deg * steps_per_rev / 360
       
        self.tasks = queue.Queue()
        self.running = False
        self.isExecuting = False
        self.timer = None
        self.track_target()
    
    
    def enqueue_item(self, item):
        self.tasks.put(item)

    def dequeue_item(self):
        if not self.tasks.empty():
            return self.tasks.get()
        return None


    def speed(self, sps):
        self.speed_sps = sps
        self.update_rate = 1.0 / sps
        if self.running:
            self.track_target()

    def speed_rps(self, rps):
        self.speed(rps * self.steps_per_rev)

    def target(self, t):
        self.target_pos = t


    def move(self,deg):
        self.enqueue_item(deg)
        


    def target_deg(self, deg):

        target_steps = self.steps_per_rev * deg / 360.0
        target_steps = math.ceil(target_steps)
        # print(f"target steps {target_steps}")
        self.target_pos = self.pos + target_steps
         
    def set_direction(self, d):
        self.invert_dir = d

    def target_rad(self, rad):
        self.target(self.steps_per_rev * rad / (2.0 * math.pi))

    def get_pos(self):
        return self.pos

    def get_pos_deg(self):
        return self.get_pos() * 360.0 / self.steps_per_rev

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


    def _timer_callback(self):
        while self.running:
            if(not self.isExecuting):
                item = self.dequeue_item()
                if item is not None:
                      self.target_deg(item)

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
        self.running = False
        if self.timer is not None and self.timer.is_alive():
            self.timer.join()
        GPIO.output(self.step_pin, GPIO.LOW)
        GPIO.output(self.dir_pin, GPIO.LOW)
        if self.en_pin is not None:
            GPIO.output(self.en_pin, GPIO.LOW)

    def reset_motor(motor):
        # Move to home position or set current position as home
        motor.overwrite_pos(0)  # Setting current position as 'home'       

# Example usage
# stepper = Stepper(step_pin=17, dir_pin=27, en_pin=22)
# stepper.target_deg(90)
# time.sleep(5)
# stepper.stop()
# GPIO.cleanup()
