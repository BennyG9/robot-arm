# Robotic Arm Project (Ongoing)

## Project Goals 

Design and build a 4 or 5 DOF robotc arm with precise mechanics and control systems 

## Status 

### Completed
* Shoulder joint mechanical protorype
* Shoulder joint PID positional control using STM32
* Rotational base mechanical prototype (CAD)

### In Progress
* Shoulder joint re-design
* Shoulder-elbow link
* Elbow joint mechanical prototype 

### Planned
* 2 then 3-DOF mechanics and control, ultimately expand to 4 or 5 DOF
* NVIDIA Jetson Nano + STM32 distributed system for high-level planning and real-time control
* RTOS implementation 
* ROS2 package for high-level robot interfacing
* AI and computer vision integration

## How it Works 

### Mechanical Design


### Embedded Architecture 



### Embedded Control



## Code Structure
* `firmware/arm_stm32/` - STM32 project main folder 
* `firmware/arm_stm32/Core/Src/` - Source files for STM32 real-time embedded control
* `firmware/arm_stm32/Core/Inc/` - Header files for embedded code
