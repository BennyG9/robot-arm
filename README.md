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

[Robotic Arm CAD (OnShape)](https://cad.onshape.com/documents/4a9cd08e29866666f506ada9/w/f0abfb5ca58521d456a9c369/e/990587cd5cd4e16cd3d5d83a)

<div align="center">
  <img src="media/CAD_Prototype_5-28-2026.jpg" width="300"/>
</div>

### Embedded Architecture 

<div align="center">
  <img src="media/Embedded_Prototype_5-29-2026.jpeg" width="300"/>
</div>

### Control




## Code Structure
* `firmware/arm_stm32/` - STM32 project main folder 
* `firmware/arm_stm32/Core/Src/` - Source files for STM32 real-time embedded control
* `firmware/arm_stm32/Core/Inc/` - Header files for embedded code

## Media 
