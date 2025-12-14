import RPi.GPIO as GPIO
import threading


class MotorLEDController:
    """
    Controls LED brightness for a motor based on its movement speed.
    Uses PWM to modulate LED intensity according to motor velocity (frps).
    """
    
    def __init__(self, led_pin, pwm_frequency=500):
        """
        Initialize the LED controller for a motor.
        
        Args:
            led_pin: GPIO pin number for the LED
            pwm_frequency: PWM frequency in Hz (default 500Hz to avoid flicker)
        """
        self.led_pin = led_pin
        self.pwm_frequency = pwm_frequency
        self.pwm = None
        self.current_brightness = 0
        self.lock = threading.Lock()
        
        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Clean up any existing PWM on this pin first
        try:
            GPIO.setup(self.led_pin, GPIO.OUT)
            GPIO.output(self.led_pin, GPIO.LOW)
        except:
            pass
        
        # Start PWM at 0% duty cycle
        try:
            self.pwm = GPIO.PWM(self.led_pin, self.pwm_frequency)
            self.pwm.start(0)
            print(f"✓ LED controller initialized on GPIO {self.led_pin}")
        except RuntimeError as e:
            print(f"⚠ PWM already exists on GPIO {self.led_pin}, attempting recovery...")
            # PWM already exists, try to clean it up and recreate
            try:
                GPIO.setup(self.led_pin, GPIO.OUT)
                GPIO.output(self.led_pin, GPIO.LOW)
                self.pwm = GPIO.PWM(self.led_pin, self.pwm_frequency)
                self.pwm.start(0)
                print(f"✓ LED controller recovered on GPIO {self.led_pin}")
            except Exception as e2:
                print(f"✗ Failed to initialize LED on GPIO {self.led_pin}: {e2}")
                self.pwm = None
    
    def speed_to_brightness(self, frps: float) -> int:
        """
        Map frps (fractional rotations per second) to LED brightness [0..100].
        
        Args:
            frps: Speed in fractional rotations per second
            
        Returns:
            Brightness value from 0 to 100
        """
        if frps <= 0:
            return 0

        if frps < 0.03:      # ultra slow
            return 5        # very dim
        elif frps < 0.08:    # slow
            return 15
        elif frps < 0.3:     # medium
            return 25
        elif frps < 2.0:     # fast
            return 50
        else:                # very fast (explosions, shakes, etc.)
            return 75
    
    def update_brightness(self, frps: float):
        """
        Update LED brightness based on motor speed.
        
        Args:
            frps: Current motor speed in fractional rotations per second
        """
        if self.pwm is None:
            return
            
        brightness = self.speed_to_brightness(abs(frps))
        
        with self.lock:
            if brightness != self.current_brightness:
                self.current_brightness = brightness
                try:
                    self.pwm.ChangeDutyCycle(brightness)
                except:
                    pass  # Ignore errors if PWM was cleaned up
    
    def set_brightness(self, brightness: int):
        """
        Manually set LED brightness.
        
        Args:
            brightness: Brightness value from 0 to 100
        """
        if self.pwm is None:
            return
            
        brightness = max(0, min(100, brightness))
        
        with self.lock:
            self.current_brightness = brightness
            try:
                self.pwm.ChangeDutyCycle(brightness)
            except:
                pass  # Ignore errors if PWM was cleaned up
    
    def turn_off(self):
        """Turn off the LED."""
        self.set_brightness(0)
    
    def cleanup(self):
        """Clean up PWM and GPIO resources."""
        try:
            with self.lock:
                if self.pwm is not None:
                    try:
                        self.pwm.stop()
                    except:
                        pass
                    self.pwm = None
            try:
                GPIO.output(self.led_pin, GPIO.LOW)
            except:
                pass
        except:
            pass  # Ignore any cleanup errors
