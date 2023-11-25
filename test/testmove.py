import time
import config.config as config
 
def main():
    
    motors = config.get_motors_map

    for i in range(1):
        for name, motor in motors.items():
            motor.speed_frps(0.1)
            motor.move(0.9)
            motor.move(0)
            motor.move(0.4)
            motor.move(0)
             
 
 
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
