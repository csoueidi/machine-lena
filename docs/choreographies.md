## The Choreography Language and Execution Framework

To control the movements of the stepper motors in our mechanical installation, we developed a custom **Choreography Language**. This language allows us to script complex motor sequences in a clear and precise manner, facilitating synchronized movements and intricate patterns without dealing with low-level motor control code. This allows us to focus on the artistic expression of the installation while maintaining full control over the mechanical elements.

### Purpose and Design Goals

- **Simplify Motor Control**: Provide a straightforward syntax to define motor actions.
- **Enable Synchronization**: Allow multiple motors to move together or in coordinated sequences.
- **Support Complex Sequences**: Include constructs like loops, timing controls, and speed adjustments.
- **Enhance Readability**: Make scripts easy to read and maintain.
- **User-Friendly Interface**: Offer an accessible way for users to create, edit, and execute choreographies.

### Understanding the Language

#### Representation of Movement

In our Choreography Language, motor movements are defined by the **percentage of the arm's opening**. A value of `0` represents the arm fully closed, while `1` indicates the arm fully open. This abstraction allows us to specify positions in a way that is intuitive and independent of the physical characteristics of the motors. Another key aspect of the language is the ability to control the speed of movements, providing flexibility in the execution of sequences.

#### Core Commands

1. **Move Command**

   Instructs a motor or all motors to move to a specified position based on the percentage of arm opening.

   - **Syntax**: `move(motor_id, percentage, speed);`

     - `motor_id`: The identifier of the motor (e.g., `1`, `2`, or `all` for all motors).
     - `percentage`: The target position as a fraction between `0` and `1`; represents the percentage of how much the mechanical arm will open.
     - `speed` (optional): The speed of the movement, in fractional rotations per second (FRPS).

   - **Examples**:
     - `move(1, 0.5);` moves motor 1 to 50% open at the current default speed.
     - `move(2, 0.75, 0.3);` moves motor 2 to 75% open at 0.3 FRPS.
     - `move(all, 1);` moves all motors to fully open.

2. **Sync Command**

   Executes multiple move commands simultaneously, ensuring that all included movements start at the same time and waits for all to complete before proceeding to the next command.

   - **Syntax**:

     ```
     sync {
         move commands
     }
     ```

   - **Example**:
     ```
     sync {
         move(1, 0.9);
         move(2, 0.9);
         move(3, 0.9);
         move(4, 0.9);
     }
     ```
     All four motors begin moving to 90% open at the same time.

3. **Repeat Command**

   Repeats a set of commands a specified number of times.

   - **Syntax**:

     ```
     repeat times {
         commands
     }
     ```

     - `times`: The number of times to repeat the enclosed commands.

   - **Example**:
     ```
     repeat 3 {
         move(1, 0);
         move(1, 1);
     }
     ```
     Motor 1 alternates between fully closed and fully open three times.

4. **Set Speed Command (`set_frps`)**

   Sets the default speed for subsequent move commands.

   - **Syntax**: `set_frps speed;`

     - `speed`: The speed in fractional rotations per second.

   - **Example**: `set_frps 0.5;` sets the default speed to 0.5 FRPS.

5. **Wait Command**

   Pauses execution for a specified number of seconds.

   - **Syntax**: `wait(seconds);`

     - `seconds`: The duration to wait.

   - **Example**: `wait(2);` pauses execution for 2 seconds.

### How the Language Works

#### Defining Movement Sequences

The Choreography Language allows us to script sequences by combining the core commands:

- **Sequential Execution**: Commands are executed in the order they appear unless modified by `sync` or `repeat`.
- **Default Speed**: Movements use the current default speed set by `set_frps`, unless a specific speed is provided in the command.
- **Motor Identification**: Motors are referenced by their IDs, enabling control of individual motors or all motors collectively.

#### Synchronization and Timing

- **Synchronization with `sync`**: Ensures that all move commands within the block start simultaneously and complete before moving to the next command.
- **Repetition with `repeat`**: Automates repetitive movement patterns efficiently.
- **Timing with `wait`**: Controls the pacing of sequences, allowing for precise timing between actions.

### Practical Examples

#### Example 1: Basic Movement Sequence

```plaintext
set_frps 0.2;

move(1, 0.5);
move(2, 0.5);
move(3, 0.5);
move(4, 0.5);
```

- Sets the default speed to 0.2 FRPS.
- Sequentially moves each motor to 50% open.

#### Example 2: Synchronized Movement

```plaintext
set_frps 0.5;

sync {
    move(all, 1);
}
```

- Sets the default speed to 0.5 FRPS.
- All motors move to fully open simultaneously.

#### Example 3: Repeated Movements with Pauses

```plaintext
repeat 2 {
    move(1, 0);
    wait(1);
    move(1, 1);
    wait(1);
}
```

- Repeats the sequence twice:
  - Motor 1 moves to fully closed.
  - Waits for 1 second.
  - Motor 1 moves to fully open.
  - Waits for 1 second.

#### Example 4: Complex Sequence

```plaintext
set_frps 0.3;

sync {
    move(1, 0.25);
    move(2, 0.25);
}

wait(0.5);

sync {
    move(3, 0.75);
    move(4, 0.75);
}

repeat 3 {
    move(1, 0);
    move(2, 0);
    wait(0.2);
    move(1, 0.25);
    move(2, 0.25);
    wait(0.2);
}
```

- Sets the default speed to 0.3 FRPS.
- Synchronously moves motors 1 and 2 to 25% open.
- Waits for half a second.
- Synchronously moves motors 3 and 4 to 75% open.
- Repeats a sequence three times where motors 1 and 2 oscillate between fully closed and 25% open with short waits.

### Execution Framework Overview

#### High-Level Process

1. **Script Loading**: The choreography script is loaded into the system.
2. **Command Interpretation**: Each command is parsed and interpreted in sequence.
3. **Motor Control**: Commands are translated into actions performed by the motors.
   - **Move Commands**: The motors are instructed to move to the specified percentage of opening.
   - **Sync Blocks**: The framework ensures that all move commands within a sync block start at the same time and waits for their completion.
   - **Repeat Blocks**: The enclosed commands are executed multiple times as specified.
   - **Wait Commands**: Introduce precise delays between actions.

#### Motor Interaction

- **Motor Instances**: Each motor is represented by an instance of the `Stepper` class, which handles low-level motor control.
- **Command Execution**: The execution framework calls methods on these motor instances to perform movements.
- **Synchronization**: The framework manages the timing to synchronize movements across multiple motors.

### User Interface Integration

To facilitate easy creation, editing, and execution of choreography scripts, we developed a web-based **HTML User Interface**. This interface allows users to manage choreography files directly from a browser, enhancing accessibility and streamlining the workflow.

#### Key Features

- **File Management**: Users can create new choreography files, load existing ones, and delete obsolete scripts.
- **Script Editing**: An integrated text editor enables users to write and modify choreography scripts within the browser.
- **Execution Control**: Users can execute the currently loaded script and stop execution if necessary.
- **Real-Time Feedback**: A log section displays execution status and system messages, providing immediate feedback.

#### Benefits

- **Ease of Access**: The web interface can be accessed from any device with a browser, without the need for additional software.
- **User-Friendly**: Simplifies interaction with the choreography system, making it accessible to users with varying technical backgrounds.
- **Improved Workflow**: Integrates script management and execution, allowing for rapid development and testing of choreographies.

### Advantages of the Choreography Language and Interface

- **Simplifies Complex Control**: Allows us to define intricate movement sequences without dealing with low-level motor commands.
- **Enhances Readability**: The syntax is clear and descriptive, making scripts easy to understand and modify.
- **Facilitates Collaboration**: Team members with different expertise can read, write, and manage scripts effectively using the interface.
- **Increases Flexibility**: Adjustments to movement sequences can be made quickly by editing the script through the interface.
- **Streamlines Workflow**: The integrated interface consolidates scripting and execution, improving efficiency.

### Use Cases in the Project

- **Performance Programming**: Designing and adjusting sequences for the installation during rehearsals and performances.
- **Interactive Responses**: Creating scripts that respond to sensor inputs, such as moving when someone approaches.
- **Testing and Calibration**: Running specific movements to test motor functionality or calibrate positions.

### Conclusion

The Choreography Language, combined with the execution framework and user interface, provides a powerful and flexible toolset for controlling the stepper motors in our mechanical installation. By abstracting motor movements into percentage-based positions and providing intuitive commands for synchronization and timing, we can create complex, coordinated sequences that enhance the artistic expression of the installation. The web-based interface further simplifies the process, making it accessible and efficient for the entire team.
