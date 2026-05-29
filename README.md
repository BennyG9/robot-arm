# Robotic Arm Project (Ongoing)

## Project Goals 

* Designa and build a 4 or 5 DOF robotic arm
* Implement real-time control system for precise mechanics
* Enable AI functionlity using computer vision on NVIDIA Jetson Nano
* Design custom PCB integrating power systems, microprocessing, and motor driving

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

<div>
  <img src="media/Embedded_Prototype_5-29-2026.jpeg" width="200"> 
  
  <p>The robotic arm is powered by an STM32 Nucleo-F446RE, taking care of all of the real-time control code. Motors are driven by IBT-2 type motor driver modules rated for up to 43A. <br> <br> The plan is to flesh out communication between the STM32 and an NVIDIA Jetson Nano which will handle higher level computation using ROS2.</p>
  <p> . </p>
</div>


### Control

So far, the shoulder joint is just controlled using a simple 1kHz PID loop. 

[PID Position Control Demo](https://youtu.be/YCUa2xMnsVE)


## Code Structure
* `firmware/arm_stm32/` - STM32 project main folder 
* `firmware/arm_stm32/Core/Src/` - Source files for STM32 real-time embedded control
* `firmware/arm_stm32/Core/Inc/` - Header files for embedded code

## Media 

[Robotic Arm CAD (OnShape)](https://cad.onshape.com/documents/4a9cd08e29866666f506ada9/w/f0abfb5ca58521d456a9c369/e/990587cd5cd4e16cd3d5d83a)

[PID Position Control Demo (5-28-2026)](https://youtu.be/YCUa2xMnsVE)

<div align="left">
  <img src="media/CAD_Prototype_5-28-2026.jpg" width="300"/>
  <img src="media/Embedded_Prototype_5-29-2026.jpeg" width="220"/>
</div>

<div align="right">
  
</div>






