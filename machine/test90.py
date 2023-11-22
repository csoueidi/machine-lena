import time
import config

def main():
    # Load motor configurations from the YAML file
    motor_config = config.load_config('/home/pi/demo/code/machine/config1.yaml')
    motors = config.create_motors(motor_config)

    deg = 15

    # Command each motor to rotate 90 degrees
    for name, motor in motors.items():
        print(f"Rotating {name} by {deg} degrees")
        # motor.speed_rps(1)
        motor.target_deg(deg)



    # Wait for all motors to reach their target positions
    all_motors_reached_target = False
    while not all_motors_reached_target:
        all_motors_reached_target = True
        for motor in motors.values():
            if motor.get_pos_deg() < deg:
                all_motors_reached_target = False
                break
        time.sleep(0.1)  # Wait a short time before checking again

    for motor in motors.values():
        motor.stop()
    print("All motors have reached their target positions.")

    
if __name__ == "__main__":
    main()
