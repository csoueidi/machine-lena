from BufferInterface import BufferInterface
from time import sleep

class TB6560Interface:
    def __init__(self):
        # Virtual pin definitions for BufferInterface
        self.pinenable = 0
        self.pindir = {'x': 1,}
        self.pinstep = {'x': 2,}
        self.pinaux = 7

        # Initialize BufferInterface
        self.io = BufferInterface()
        
        # Set default parameters, speed in pulses per second (Hz)
        self.speed = {'x': 10.0,
                      }
        
        # Initialize operation variables
        self.pos = {'x': 0,
                    }
        
        self.busyFlag = False
        
    def setSpeed(self, speed, stepper=None):
        # """Set the speed of a stepper, if no stepper was specified, apply to all."""
        if stepper is None:
            # No stepper was specified, apply to all
            for i in self.speed.keys():
                self.speed[i] = speed
        else:
            self.speed[stepper] = speed
    
    
    def moveOneBySteps(self, stepper, steps):
        # """Move the specified stepper a number of steps."""
        self.busyFlag = True
        # TODO: Create a new thread
        #self.io.write(self.pinenable, 1) # Enable the controller
        if self.speed[stepper] != 0:
            
            # Set direction of movement
            if self.speed[stepper] > 0:
                self.io.write(self.pindir[stepper], 1)
            else:
                self.io.write(self.pindir[stepper], 0)
            
            # Calculate delay between each
            delay = 1.0 / abs(self.speed[stepper])
            for i in range(steps):
                self.io.write(self.pinstep[stepper], 1)
                sleep(delay)
                self.io.write(self.pinstep[stepper], 0)
                sleep(delay)
            
        #self.io.write(self.pinenable, 0) # Disable the controller
        self.busyFlag = False
        
    def getPosition(self):
        return [self.pos['x'], self.pos['y'], self.pos['z']]

    def isBusy(self):
        return self.busyFlag
        
    
