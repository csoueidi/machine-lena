
import threading
import time
import math
import queue

class MockGPIO:
    BCM = 'BCM'
    OUT = 'OUT'
    HIGH = 'HIGH'
    LOW = 'LOW'

    @staticmethod
    def setmode(mode):
        print(f"GPIO setmode({mode})")

    @staticmethod
    def setup(pin, mode):
        print(f"GPIO setup(pin={pin}, mode={mode})")

    @staticmethod
    def output(pin, state):
        print(f"GPIO output(pin={pin}, state={state})")

    @staticmethod
    def cleanup():
        print("GPIO cleanup()")

class MockStepper:
    def __init__(self, step_pin, dir_pin, en_pin=None, steps_per_rev=200, speed_sps=10,  max_deg = 360, min_deg=0,invert_dir=False):
        GPIO = MockGPIO
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

       
        self.max_deg = max_deg  
        self.max_steps = max_deg * steps_per_rev / 360
 
       
        self.tasks = queue.Queue()
        self.running = False
        self.isExecuting = False
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

    def speed_frps(self, rps):
        self.speed(rps * self.max_steps)    

    def target(self, t):
        self.target_pos = t

    def move(self, percentage, speed=None):
        # Check if percentage is between 0 and 1 (inclusive)
        if not 0 <= abs(percentage) <= 1:
            return

        # Rest of your function logic goes here
        if speed is not None:
            self.enqueue_item(self.max_deg*percentage, speed, percentage >= 0)
        else:
            self.enqueue_item(self.max_deg*percentage, self.speed_sps, percentage >= 0)


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

    def target_deg(self, deg):
        # This method is called from the timer thread

        target_steps = self.steps_per_rev * deg / 360.0
        target_steps = math.ceil(target_steps)

        # print(f"target steps {target_steps}")
        # self.target_pos = self.pos + target_steps
        
        self.target_pos = math.ceil(max(0, min(self.pos + target_steps, self.max_steps)))
       
        # print(f"Setting target pos  {self.target_pos}")

    def _timer_callback(self):
        while self.running:
            if(not self.isExecuting):
                item = self.dequeue_item()
                if item is not None:
                    degree, speed, is_move = item
                    if is_move:
                        degree = degree - self.get_pos_deg()
                    if degree < 0:
                        self.set_direction(True)
                    self.speed(speed)
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
