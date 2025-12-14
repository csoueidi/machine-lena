# LED Brightness Configuration

This document describes how LED brightness is mapped to motor speed (frps - fractional rotations per second).

## Brightness Mapping

The LED brightness is controlled using PWM (Pulse Width Modulation) with the following default mapping:

| Speed Range (frps) | Brightness (0-100) | Description |
|-------------------|-------------------|-------------|
| 0                 | 0                 | Motor stopped - LED off |
| < 0.03            | 10                | Ultra slow - very dim |
| 0.03 - 0.08       | 30                | Slow movement |
| 0.08 - 0.3        | 50                | Medium speed |
| 0.3 - 2.0         | 75                | Fast movement |
| > 2.0             | 100               | Very fast (explosions, shakes) |

## Customizing Brightness Levels

To modify the brightness mapping for your specific setup:

1. Edit the `speed_to_brightness()` method in `/home/pi/Code/machine-code/machine/lights/motor_led_controller.py`
2. Adjust the threshold values (frps ranges) to match your motor speeds
3. Adjust the brightness values (0-100) to achieve desired visual effect

### Example:
```python
def speed_to_brightness(self, frps: float) -> int:
    if frps <= 0:
        return 0
    
    if frps < 0.05:      # Adjust this threshold
        return 15        # Adjust this brightness
    elif frps < 0.1:
        return 35
    # ... etc
```

## PWM Frequency

The default PWM frequency is 500 Hz, which eliminates visible LED flicker. This can be adjusted in the `MotorLEDController` initialization if needed.

## LED Pin Configuration

LED pins are configured per motor in `config1.yaml`:

```yaml
motors:
  1:
    led_pin: 16  # GPIO pin for motor 1 LED
  2:
    led_pin: 12  # GPIO pin for motor 2 LED
  # ... etc
```

## Technical Details

- LEDs are controlled using PWM duty cycle (0-100%)
- Brightness updates happen in real-time as motor speed changes
- LED automatically turns off when motor stops
- Thread-safe implementation for concurrent motor operations
