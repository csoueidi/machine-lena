import time
import config
 
def main():
    # Load motor configurations from the YAML file
    motor_config = config.load_config('/home/pi/demo/code/machine/config1.yaml')
    motors = config.create_motors(motor_config)

    for i in range(1):
        for name, motor in motors.items():
            motor.speed_frps(0.1)
            motor.move(0.9)
            motor.move(0)
            motor.move(0.4)
            motor.move(0)
            # motor.speed_frps(0.2)
            # motor.move(0.7)
            # motor.move(0)
            # motor.move(0.7)
            # motor.move(0)
            # motor.speed_frps(0.9)
            # motor.move(0.2)
            # motor.move(0)
            # motor.move(0.2)
            # motor.move(0)
            # motor.speed_frps(0.2)
            # motor.move(0.15)
            # motor.move(0)
            # motor.move(0.15)
            # motor.move(0)
     
            # motor.speed_frps(0.2)
            # motor.move(0.5)
            # motor.move(0)
            # motor.move(0.5)
            # motor.move(0)
 
 
 

    # # # Command each motor to rotate by the specified degree
    # for name, motor in motors.items():
    #     print(f"Rotating {name} by {deg} degrees")

    #     motor.move_deg(deg,speed)
    #     motor.move_deg((0 - deg),speed)
 

    # # Wait for all motors to reach their target positions
    all_motors_reached_target = False
    while not all_motors_reached_target:
        time.sleep(1)
        all_motors_reached_target = True
        for motor in motors.values():
            if motor.isExecuting:
                all_motors_reached_target = False
                break
 

    for motor in motors.values():
        print(f"Stopping motor {name} pos {motor.get_pos()} angle {motor.get_pos_deg()}" )
        motor.stop()
    print("All motors have reached their target positions.")

if __name__ == "__main__":
    main()
