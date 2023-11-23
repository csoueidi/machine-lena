import time
import config
 
 
def main():
    # Load motor configurations from the YAML file
    motor_config = config.load_config('/home/pi/demo/code/machine/config1.yaml')
    motors = config.create_motors_map(motor_config)


    motors.get(3).move(0.1)
    motors.get(3).move(0)
    motors.get(4).move(0.1)
    motors.get(4).move(0)


    all_motors_reached_target = False
    while not all_motors_reached_target:
        time.sleep(1)
        all_motors_reached_target = True
        for motor in motors.values():
            if motor.isExecuting:
                all_motors_reached_target = False
                break
 

    for motor_id, motor in motors.items():
        # Call some method on each motor
        print(f"Stopping motor {motor_id} pos {motor.get_pos()} angle {motor.get_pos_deg()}" )
        motor.stop()

 
    print("All motors have reached their target positions.")

if __name__ == "__main__":
    main()
