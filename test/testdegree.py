import time
import config.config as config
 
def main():
   
    motors = config.get_motors_map

   
    for name, motor in motors.items():
        motor.move_deg(360,1000)
        motor.move_deg(-360,1000)
       
 
 

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
