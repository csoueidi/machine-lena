# Motor LED Implementation Summary

## Overview
Successfully implemented LED lighting system where each motor has a corresponding LED that lights up based on the motor's movement speed, with brightness proportional to velocity.

## What Was Added

### 1. LED Controller Class (`/lights/motor_led_controller.py`)
- **MotorLEDController**: Manages PWM-controlled LED for each motor
- **Features**:
  - PWM frequency: 500 Hz (flicker-free)
  - Thread-safe brightness updates
  - Speed-to-brightness mapping based on frps (fractional rotations per second)
  - Automatic LED shutdown when motor stops

### 2. Speed-to-Brightness Mapping
The LED brightness is mapped to motor speed as follows:

| Speed (frps) | Brightness | Visual Effect |
|--------------|-----------|---------------|
| 0            | 0% (OFF)  | Motor stopped |
| < 0.03       | 10%       | Ultra slow - very dim |
| 0.03 - 0.08  | 30%       | Slow movement |
| 0.08 - 0.3   | 50%       | Medium speed |
| 0.3 - 2.0    | 75%       | Fast movement |
| > 2.0        | 100%      | Very fast (full brightness) |

### 3. Configuration Updates

**Updated `config1.yaml`**:
```yaml
motors:
  1:
    led_pin: 16  # GPIO pin 16 for motor 1 LED
  2:
    led_pin: 12  # GPIO pin 12 for motor 2 LED
  3:
    led_pin: 7   # GPIO pin 7 for motor 3 LED
  4:
    led_pin: 1   # GPIO pin 1 for motor 4 LED
```

### 4. Stepper Class Integration (`/stepper/stepper.py`)

**Changes made**:
1. Added `led_pin` parameter to `__init__()` method
2. Instantiates `MotorLEDController` when `led_pin` is provided
3. Tracks current motor speed in `current_frps` variable
4. Updates LED brightness in `_timer_callback()` when motor starts moving
5. Turns off LED automatically when motor stops
6. Cleans up LED resources in `stop()` method

**Key implementation points**:
- LED brightness updates happen in the motor control thread
- Brightness is calculated from the speed (frps) parameter passed to each movement
- LED turns off immediately when motor reaches target position
- No performance impact on motor control

### 5. Config Loading Updates (`/config/config.py`)

Updated both `create_motors()` and `create_motors_map()` functions to:
- Read `led_pin` from YAML configuration
- Pass `led_pin` to Stepper constructor
- Default to `None` if no LED pin specified (backward compatible)

### 6. Mock Stepper Updates (`/stepper/mockstepper.py`)

Updated for API consistency:
- Added `led_pin` parameter (not used in mock mode)
- Added dummy `led_controller` and `current_frps` attributes
- Maintains compatibility with testing framework

## How It Works

1. **Initialization**: When a motor is created, if an `led_pin` is specified in config, a `MotorLEDController` is instantiated
2. **Movement Start**: When motor dequeues a movement task, it:
   - Extracts the speed (frps) from the task
   - Updates `current_frps` 
   - Calls `led_controller.update_brightness(frps)` to set LED brightness
3. **During Movement**: LED stays at constant brightness matching the movement speed
4. **Movement Stop**: When motor reaches target position:
   - Sets `current_frps = 0`
   - Calls `led_controller.turn_off()` to turn off LED
5. **Cleanup**: When motor stops completely, LED resources are cleaned up

## Hardware Setup

For each motor, connect an LED circuit:
```
GPIO Pin (e.g., 16) → Resistor (220Ω-470Ω) → LED → Ground
```

**Important**: Use appropriate current-limiting resistors based on your LED specifications.

## Advantages

1. **Non-intrusive**: No impact on existing motor control code
2. **Automatic**: LEDs respond automatically to motor movements
3. **Visual feedback**: Instant visual indication of motor speed
4. **Customizable**: Easy to adjust brightness thresholds in one place
5. **Thread-safe**: Safe for concurrent motor operations
6. **Clean shutdown**: Proper resource cleanup

## Testing

Your existing choreographies will now automatically control the LEDs:
- Run any choreography file through the UI
- LEDs will light up proportionally to motor speeds
- Each motor's LED indicates its individual speed

## Customization

To adjust brightness levels, edit `speed_to_brightness()` in:
`/home/pi/Code/machine-code/machine/lights/motor_led_controller.py`

See `LED_BRIGHTNESS_CONFIG.md` for detailed customization guide.

## Files Modified

1. ✅ `/stepper/stepper.py` - Added LED control integration
2. ✅ `/stepper/mockstepper.py` - API compatibility
3. ✅ `/config/config.py` - LED pin loading
4. ✅ `/config/config1.yaml` - LED pin configuration
5. ✅ `/lights/motor_led_controller.py` - NEW LED controller class
6. ✅ `/LED_BRIGHTNESS_CONFIG.md` - NEW configuration guide

## No Breaking Changes

- Existing code continues to work without modification
- LED functionality is optional (motors without `led_pin` work normally)
- All existing tests and choreographies remain functional
- Mock mode for testing remains intact
