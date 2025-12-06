#!/usr/bin/env python3
"""
Test script to verify position preservation after immediate stop.
This tests that motors correctly preserve their position when stopped mid-movement.
"""

import sys
from pathlib import Path
import time

parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

from stepper.mockstepper import Stepper
import config.config as config

def test_position_preservation():
    """Test that position is preserved after immediate stop"""
    
    print("\n" + "="*60)
    print("TESTING POSITION PRESERVATION AFTER IMMEDIATE STOP")
    print("="*60 + "\n")
    
    # Create a mock motor
    motor = Stepper(
        step_pin=17, 
        dir_pin=27, 
        steps_per_rev=200,
        speed_sps=100,
        max_deg=360,
        motor_name="test_motor",
        initial_position=0
    )
    
    print(f"Initial state:")
    print(f"  Position: {motor.get_pos_deg()}° ({motor.pos} steps)")
    print(f"  Pending target: {motor.pending_target_deg}°")
    print(f"  Target pos: {motor.target_pos} steps\n")
    
    # Test 1: Move and stop mid-movement
    print("TEST 1: Move to 50% and stop immediately")
    print("-" * 60)
    
    motor.move(0.5, 2.0)  # Move to 50% at speed 2.0 frps
    time.sleep(0.5)  # Let it start moving
    
    print(f"Mid-movement state:")
    print(f"  Position: {motor.get_pos_deg()}° ({motor.pos} steps)")
    print(f"  Is executing: {motor.isExecuting}")
    
    motor.stop_immediately()
    time.sleep(0.1)  # Let stop complete
    
    stopped_pos_deg = motor.get_pos_deg()
    stopped_pos_steps = motor.pos
    
    print(f"\nAfter immediate stop:")
    print(f"  Position: {stopped_pos_deg}° ({stopped_pos_steps} steps)")
    print(f"  Pending target: {motor.pending_target_deg}°")
    print(f"  Target pos: {motor.target_pos} steps")
    print(f"  Is executing: {motor.isExecuting}")
    print(f"  Thread running: {motor.running}")
    
    # Verify state consistency
    assert motor.target_pos == motor.pos, "❌ target_pos should equal pos after stop"
    assert abs(motor.pending_target_deg - stopped_pos_deg) < 1, "❌ pending_target_deg should match current position"
    assert not motor.isExecuting, "❌ Should not be executing after stop"
    assert motor.running, "❌ Thread should be running and ready for next command"
    
    print("✅ State is consistent after stop\n")
    
    # Test 2: Move again from stopped position
    print("\nTEST 2: Move to 30% from stopped position")
    print("-" * 60)
    
    motor.move(0.3, 2.0)  # Move to 30%
    time.sleep(1.0)  # Let movement complete
    
    final_pos_deg = motor.get_pos_deg()
    expected_pos_deg = 0.3 * 360
    
    print(f"After second move:")
    print(f"  Position: {final_pos_deg}°")
    print(f"  Expected: {expected_pos_deg}°")
    print(f"  Pending target: {motor.pending_target_deg}°")
    
    # Allow some tolerance for timing
    tolerance = 10  # degrees
    assert abs(final_pos_deg - expected_pos_deg) < tolerance, \
        f"❌ Motor should be at ~{expected_pos_deg}°, but is at {final_pos_deg}°"
    
    print(f"✅ Motor moved correctly from stopped position\n")
    
    # Test 3: Multiple stops
    print("\nTEST 3: Multiple stops and moves")
    print("-" * 60)
    
    motor.move(0.8, 2.0)  # Move to 80%
    time.sleep(0.3)
    motor.stop_immediately()
    pos1 = motor.get_pos_deg()
    print(f"Stop 1 at: {pos1}°")
    
    time.sleep(0.2)
    
    motor.move(0.6, 2.0)  # Move to 60%
    time.sleep(0.3)
    motor.stop_immediately()
    pos2 = motor.get_pos_deg()
    print(f"Stop 2 at: {pos2}°")
    
    time.sleep(0.2)
    
    motor.move(1.0, 2.0)  # Move to 100%
    time.sleep(2.0)  # Let it complete
    final_pos = motor.get_pos_deg()
    
    print(f"Final position after multiple stops: {final_pos}°")
    print(f"Expected: ~360°")
    
    assert abs(final_pos - 360) < tolerance, \
        f"❌ Motor should reach 360°, but is at {final_pos}°"
    
    print(f"✅ Multiple stops handled correctly\n")
    
    # Cleanup
    motor.stop()
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED! ✅")
    print("Position is correctly preserved after immediate stops.")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        test_position_preservation()
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
