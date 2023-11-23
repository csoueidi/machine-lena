import time
import config
import argparse  # Import the argparse module

def main(deg,seconds):
    # Load motor configurations from the YAML file
    motor_config = config.load_config('/home/pi/demo/code/machine/config1.yaml')
    motors = config.create_motors(motor_config)

    # Command each motor to rotate by the specified degree
    for name, motor in motors.items():
        print(f"Rotating {name} by {deg} degrees")
        if deg < 0:
            motor.set_direction(False)
        motor.move(abs(deg))
        motor.move((-1-deg))
        motor.speed(2000)
        motor.move(abs(deg))
        motor.move((-1-deg))

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
        print(f"Stopping motor {name} pos {motor.get_pos()}" )
        motor.stop()
    print("All motors have reached their target positions.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rotate motors by a specified degree.')
    parser.add_argument('degree', type=int, help='Degree of rotation for the motors')
    parser.add_argument('seconds', type=int, help='Seconds before terminating')
   
    args = parser.parse_args()
    main(args.degree,args.seconds)
