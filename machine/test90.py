import time
import config
import argparse  # Import the argparse module

def main(deg,speed):
    # Load motor configurations from the YAML file
    motor_config = config.load_config('/home/pi/demo/code/machine/config1.yaml')
    motors = config.create_motors(motor_config)

    #  # Command each motor to rotate by the specified degree
    for name, motor in motors.items():
        print(f"Rotating {name} by {deg} degrees")

        motor.move(deg,speed)
        motor.move(deg,speed)
        motor.move(deg,speed)
        # motor.move(deg,speed)
        # motor.move(deg,speed)
        # motor.move((0 - deg),speed)

    # # # Command each motor to rotate by the specified degree
    # for name, motor in motors.items():
    #     print(f"Rotating {name} by {deg} degrees")

    #     motor.move_deg(deg,speed)
    #     motor.move_deg((0 - deg),speed)
    #     motor.move_deg(deg,speed*2)
    #     motor.move_deg((0 - deg),speed*2)
    #     motor.move_deg(deg,speed)
    #     motor.move_deg((0 - deg),speed)
    #     motor.move_deg(deg,speed)
    #     motor.move_deg((0 - deg),speed)
    #     # motor.move_deg(deg,speed)
    #     # motor.move_deg((0 - deg),speed)
    #     # motor.move_deg(deg,speed)
    #     # motor.move_deg((0 - deg),speed)
    #     # motor.move_deg(deg,speed)
    #     # motor.move_deg((0 - deg),speed)
 

  # Command each motor to rotate by the specified degree
   


    # # Wait for all motors to reach their target positions
    all_motors_reached_target = False
    while not all_motors_reached_target:
        time.sleep(1)
        all_motors_reached_target = True
        for motor in motors.values():
            if motor.isExecuting:
                all_motors_reached_target = False
                break
   
    # time.sleep(seconds)  # Wait a short time before checking again

    # for motor in motors.values():
    #  print(f"Motor {name} pos {motor.get_pos()}" )


    # for name, motor in motors.items():
    #     print(f"Rotating {name} by {(-1 - deg)} degrees")
    #     motor.target_deg((-1-deg))

    # time.sleep(seconds)  

    for motor in motors.values():
        print(f"Stopping motor {name} pos {motor.get_pos()} angle {motor.get_pos_deg()}" )
        motor.stop()
    print("All motors have reached their target positions.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rotate motors by a specified degree.')
    parser.add_argument('degree', type=float, help='Degree of rotation for the motors')
    parser.add_argument('speed', type=int, help='Speed before terminating')
   
    args = parser.parse_args()
    main(args.degree,args.speed)
