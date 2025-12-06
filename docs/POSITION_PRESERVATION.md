# Position Preservation After Immediate Stop

## The Critical Issue

When implementing immediate stop functionality, we discovered a subtle but important issue: **position state must be preserved** so that subsequent choreographies can continue from where the motors stopped.

## The Problem Scenario

### Without Proper Preservation:
```
1. Choreography A starts: Motor at 0°
2. Move to 50° starts
3. User clicks STOP at 25° (mid-movement)
4. Motor stops at 25°
5. Choreography B starts: Move to 30%
   ❌ Motor thinks it's at 0° and moves incorrectly!
```

### With Proper Preservation:
```
1. Choreography A starts: Motor at 0°
2. Move to 50° starts
3. User clicks STOP at 25° (mid-movement)
4. Motor stops at 25°, saves position
5. Choreography B starts: Move to 30%
   ✅ Motor knows it's at 25° and moves correctly!
```

## State Variables That Must Be Preserved

### 1. `self.pos` (Current Step Position)
- **What**: The actual step count from home position
- **Why**: This is the physical position of the motor
- **Saved**: To `config.yaml` via `config.update_initial_position()`
- **Used**: When motors are re-initialized, they read this value

### 2. `self.pending_target_deg` (Pending Target in Degrees)
- **What**: The target position after all queued moves complete
- **Why**: Next `move()` commands are relative to this value
- **Critical**: Must be updated to current position on stop!
- **Example**: 
  ```python
  # Motor at 25° when stopped
  self.pending_target_deg = self.get_pos_deg()  # Set to 25°
  # Next move(0.3) will calculate: 0.3 * max_deg - 25° = correct relative movement
  ```

### 3. `self.target_pos` (Target Step Position)
- **What**: The immediate target for the motor thread loop
- **Why**: Setting this equal to `pos` stops movement immediately
- **Reset**: `self.target_pos = self.pos` on stop

## Code Flow Analysis

### Normal Stop (Graceful):
```python
def stop(self):
    self.running = False           # Tell thread to stop
    self.timer.join()              # Wait for thread to finish naturally
    config.update_initial_position(self.motor_name, self.pos)  # Save position
    # GPIO cleanup...
```

### Immediate Stop (Emergency):
```python
def stop_immediately(self):
    self.running = False           # Tell thread to stop NOW
    
    # Clear queue - no more pending moves
    while not self.tasks.empty():
        self.tasks.get_nowait()
    
    # Stop movement immediately
    self.target_pos = self.pos
    
    # ⚠️ CRITICAL: Update pending target to current position
    self.pending_target_deg = self.get_pos_deg()
    
    self.isExecuting = False
    self.timer.join(timeout=0.5)   # Quick wait
    
    # Save position for next session
    config.update_initial_position(self.motor_name, self.pos)
    
    # GPIO cleanup...
    
    # ⚠️ CRITICAL: Restart thread so motor is ready
    self.track_target()
```

## Why Restart the Thread?

After stopping, we call `self.track_target()` which:
1. Stops the old thread (if still alive)
2. Creates a new thread
3. Starts the motor control loop again

**This is essential because:**
- The motor needs an active thread to process new commands
- Without restart, the next choreography would fail
- The thread needs to be in a clean state with no leftover flags

## Testing the Fix

### Test Case 1: Stop and Resume
```python
# Start choreography
move(1, 0.5)  # Move to 50%

# Stop mid-movement (at ~25%)
stop_immediately()

# Check state
print(motor.pos)                  # Should be ~25% in steps
print(motor.pending_target_deg)   # Should be ~25% in degrees
print(motor.target_pos)           # Should equal motor.pos

# Start new choreography
move(2, 0.3)  # Move to 30%
# Should move from 25% to 30% (5% movement)
```

### Test Case 2: Multiple Stops
```python
move(1, 0.8)  # Start moving to 80%
stop_immediately()  # Stop at ~40%

move(1, 0.6)  # Move to 60%
stop_immediately()  # Stop at ~50%

move(1, 1.0)  # Move to 100%
# Should move from 50% to 100%
```

## Configuration Persistence

The position is also saved to `config.yaml`:

```yaml
motors:
  1:
    initial_position: 1250  # Steps from home
    # ... other config
```

When the application restarts, motors are initialized with:
```python
Stepper(..., initial_position=config['initial_position'])
```

This ensures position is preserved even across application restarts!

## Common Pitfalls Avoided

### ❌ Mistake 1: Not updating `pending_target_deg`
```python
# Wrong:
self.target_pos = self.pos
# pending_target_deg still points to old target!
# Next move() will calculate wrong relative movement
```

### ❌ Mistake 2: Not restarting thread
```python
# Wrong:
self.running = False
self.timer.join()
# Thread is dead, motor won't respond to new commands!
```

### ❌ Mistake 3: Not saving to config
```python
# Wrong:
self.target_pos = self.pos
self.pending_target_deg = self.get_pos_deg()
# Position lost on app restart!
```

### ✅ Correct Implementation:
```python
self.target_pos = self.pos
self.pending_target_deg = self.get_pos_deg()
config.update_initial_position(self.motor_name, self.pos)
self.track_target()  # Restart for next use
```

## Summary

Position preservation requires careful handling of **three levels** of state:

1. **Thread state**: `running`, `isExecuting`, `timer`
2. **Position state**: `pos`, `target_pos`, `pending_target_deg`
3. **Persistent state**: `config.yaml` entries

All three must be properly managed during immediate stop to ensure:
- ✅ Motor stops immediately
- ✅ Current position is preserved
- ✅ Next choreography starts from correct position
- ✅ Position survives application restart
- ✅ Motor is ready to accept new commands

## Date: December 4, 2025
