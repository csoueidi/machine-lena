# Quick Start: Motor LED Control

## ✅ Implementation Complete!

Your motors now have speed-reactive LED lighting! Each motor's LED automatically adjusts brightness based on movement speed.

## Hardware Connections

Connect LEDs to your Raspberry Pi GPIO pins:

```
Motor 1 LED: GPIO 16 → [Resistor] → LED → GND
Motor 2 LED: GPIO 12 → [Resistor] → LED → GND  
Motor 3 LED: GPIO 7  → [Resistor] → LED → GND
Motor 4 LED: GPIO 1  → [Resistor] → LED → GND
```

**Resistor**: Use 220Ω-470Ω depending on your LED

## How It Works

```
Motor Speed (frps)  →  LED Brightness
─────────────────────────────────────
   0.00 (stopped)   →  OFF (0%)
   0.02 (crawling)  →  Very dim (10%)
   0.05 (slow)      →  Dim (30%)
   0.15 (medium)    →  Medium (50%)
   0.50 (fast)      →  Bright (75%)
   2.50 (very fast) →  Full (100%)
```

## Usage

**No code changes needed!** Just run your existing choreographies:

```bash
cd /home/pi/Code/machine-code/machine
python ui/app.py
```

The LEDs will automatically:
- ✨ Light up when motor moves
- 💡 Adjust brightness based on speed
- 🌑 Turn off when motor stops

## Customization

Want different brightness levels? Edit this function:

**File**: `/home/pi/Code/machine-code/machine/lights/motor_led_controller.py`

```python
def speed_to_brightness(self, frps: float) -> int:
    if frps <= 0:
        return 0
    
    if frps < 0.03:      # ← Change these thresholds
        return 10        # ← Change these brightness values
    elif frps < 0.08:
        return 30
    # ... and so on
```

## Testing

1. Start your application
2. Run any choreography
3. Watch the LEDs respond to motor movements!

Each motor's LED independently reflects its speed - ultra-smooth visual feedback! 🎉

## Troubleshooting

**LEDs not lighting?**
- Check GPIO pin connections match config
- Verify resistor values (220Ω-470Ω recommended)
- Check LED polarity (longer leg = positive)
- Ensure motors are actually moving

**LEDs too bright/dim?**
- Adjust resistor values (higher Ω = dimmer)
- Or customize brightness in `motor_led_controller.py`

## What Was Changed

✅ Added LED controller class  
✅ Integrated into motor control loop  
✅ Updated configuration files  
✅ Zero impact on existing functionality  

**All your existing code works exactly as before!**
