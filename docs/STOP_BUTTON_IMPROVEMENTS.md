# Stop Button Improvements

## Problem
Previously, clicking the **Stop** button in the UI would not immediately halt motor movements. The system would wait for the current motor movements to complete before stopping, which could take several seconds depending on the choreography.

## Root Cause
1. The stop flag was only checked at the **start** of each command
2. `wait_motors_to_finish()` would loop until all motors completed their movements
3. Individual motors didn't check the stop flag during execution
4. Motor queues weren't cleared on stop

## Solution Implemented

### 1. **Immediate Stop Check in Wait Loop**
**File**: `choreography/NewChoreographyVisitor.py`

Added stop flag check inside `wait_motors_to_finish()`:
```python
def wait_motors_to_finish(self):
    all_motors_reached_target = False
    while not all_motors_reached_target:
        # Check if stop was requested during wait
        if self.stop_flag:
            raise StopParsingException("Stopping the parsing process")
        # ... rest of loop
```

### 2. **Immediate Motor Stop**
**File**: `service/myparser.py`

Modified `stop()` to immediately stop all motors:
```python
def stop(self):
    if self.visitor is not None:
        self.visitor.stop_flag = True
        # Immediately stop all motors
        for motor in self.motors.values():
            motor.stop_immediately()
```

### 3. **New `stop_immediately()` Method**
**Files**: 
- `stepper/stepper.py`
- `stepper/mockstepper.py`

Added new method that:
- Sets `running = False` to stop the motor thread
- **Clears the task queue** to cancel pending movements
- Sets `target_pos = pos` to stop current movement
- Resets `isExecuting` flag
- **Updates `pending_target_deg` to current position** (critical for next move!)
- Saves current position to config
- Turns off GPIO pins immediately
- Uses `timer.join(timeout=0.5)` to avoid hanging
- **Restarts the motor thread** with `track_target()` so it's ready for next choreography

## Benefits

✅ **Immediate Response**: Stop button now halts motors within ~0.5 seconds maximum
✅ **State Consistency**: Current position is saved correctly
✅ **Queue Clear**: Pending movements are discarded
✅ **Safe GPIO**: All pins are turned off properly
✅ **No Hangs**: Timeout prevents infinite waits

## Behavior

### Before:
```
User clicks STOP
  → Wait for current move to finish (could be 5-10 seconds)
  → Set stop flag
  → Raise exception
  → Stop
```

### After:
```
User clicks STOP
  → Set stop flag immediately
  → Clear all motor queues
  → Set target = current position (stops movement)
  → Break wait loops
  → Save positions
  → Stop (< 0.5 seconds)
```

## Technical Details

### Motor State on Stop:
- `running = False` - stops the motor thread
- `target_pos = pos` - no more movement
- `pending_target_deg = current_deg` - **queue reset and ready for next move**
- `isExecuting = False` - signals completion
- Position saved to `config.yaml`
- **Thread restarted** - motor ready for next choreography

### Code Consistency:
The changes maintain code consistency by:
1. Properly saving motor positions before stopping
2. Clearing queues to prevent stale commands
3. Resetting all relevant flags
4. **Preserving position state for next choreography** - critical fix!
5. **Restarting motor thread** so it's ready to accept new commands
6. Using proper exception handling
7. Maintaining the same interface (no breaking changes)

## Testing Recommendations

1. **Basic Stop**: Start a long choreography, click stop, verify immediate halt
2. **Position Accuracy**: Check that `config.yaml` shows correct positions after stop
3. **Resume After Stop**: Execute another choreography after stopping
4. **Sync Commands**: Test stopping during `sync{}` blocks
5. **Multiple Motors**: Verify all motors stop together
6. **Edge Cases**: Test stopping at start, middle, and end of movements

## Usage

No changes needed in UI or API - the stop button works the same way:
```javascript
// UI already calls this correctly
fetch(`${BASE_URL}/stop/${currentFilename}`, { method: 'POST' })
```

## Date: December 4, 2025
