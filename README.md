# Robotic Arm Project (Ongoing)

STM32-based robotic arm project focused on embedded control systems and robotic system design. The long-term goal is a 4-5 DOF manipulator with ROS2 integration, computer vision, and AI-assisted task execution using an NVIDIA Jetson Nano. This project is a work in progress and is documented regularly...
<br><br>
Here are some videos demonstrating the current progress:
* [Base & Shoulder Calibration and Homing (6-14-2026)](https://youtu.be/knIQMhBv_wg)
* [PID Position Control Demo (5-29-2026)](https://youtu.be/YCUa2xMnsVE)

Project Started: May 2026
<br>
Last Documentation Update: 6/14/2026

## Project Goals 

* Design and build a 4 or 5 DOF robotic arm
* Implement real-time control system for precise mechanics
* Enable AI functionality using computer vision on NVIDIA Jetson Nano
* Design custom PCB integrating power systems, embedded processing, and motor driving

## Status 

### Completed
* Shoulder joint mechanical prototype
* Shoulder joint PID positional control using STM32
* Rotational base mechanical prototype (CAD)
* STM32 embedded software architecture 

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
---
<div>
  <img align="right" src="media/5-28-2026/CAD_Prototype_5-28-2026.jpg" width="275"> 
  <p>The mechanical structure is being developed using OnShape. The current prototype shows basic shoulder joint and rotating base design. The design distributes mechanical loads through dedicated bearings rather than motor shafts and maximizes torque closer to the shoulder joint. The new design improves stiffness and reduces footprint from the previous version. <br><br> Current work includes adding limit switch stops to the shoulder joint and designing the shoulder-elbow link & elbow joint.</p>
  <br clear="right" />
</div>

### Embedded Architecture 
---
<div>
  <img align="right" src="media/5-28-2026/Embedded_Prototype_5-29-2026.jpeg" width="250"> 
  
  <p>The robotic arm is powered by an STM32 Nucleo-F446RE, responsible for all of the real-time control code. Motors are driven by IBT-2 type motor driver modules rated for up to 43A. <br> <br> The plan is to flesh out communication between the STM32 and an NVIDIA Jetson Nano which will handle higher level computation using ROS2.</p>
  <br clear="right" />
</div>


### Control
---
The shoulder joint currently uses a 1kHz closed-loop PID controller running on an STM32F446RE. Joint position is determined using an encoder updated every control loop cycle. The motor is driven using an IBT-2 type motor driver module. 

[PID Position Control Demo](https://youtu.be/YCUa2xMnsVE)

## Technical Stack

### Hardware
* STM32 Nucleo F446RE
* NVIDIA Jetson Nano (planned)
* IBT-2 Motor Driver Modules
* Geared DC Motors with Encoders
### Software
* C (STM32)
* FreeRTOS (planned)
* ROS2 (planned)
### Design Tools 
* OnShape (CAD)
* STM32CubeMX & STM32CubeIDE
* Git

## Repository Structure 
````text
robotic-arm/
├── firmware/ 
│   └── arm_stm32/
├── hardware/
│   ├──  CAD/
│   └──  KiCAD/
├── media/
├── software/
└── README.md
````

## Code Structure
* `firmware/arm_stm32/` - STM32 project main folder 
* `firmware/arm_stm32/Core/Src/` - Source files for STM32 real-time embedded control
* `firmware/arm_stm32/Core/Inc/` - Header files for embedded code

## Media 

[PID Position Control Demo (5-28-2026)](https://youtu.be/YCUa2xMnsVE)
[Base & Shoulder Calibration and Homing (6-14-2026)](https://youtu.be/knIQMhBv_wg)

<div align="left">
  <img src="media/5-28-2026/CAD_Prototype_5-28-2026.jpg" width="300"/>
  <img src="media/5-28-2026/Embedded_Prototype_5-29-2026.jpeg" width="220"/>
  <br clear="leftt" />
  <img src="media/6-14-2026/CAD_Prototype_6-14-2026.jpg" width="300"/>
  <img src="media/6-14-2026/Embedded_Prototype_6-14-2026.jpeg" width="300"/>
  <img src="media/6-14-2026/Mechanical_Prototype_6-14-2026.jpeg" width="300"/>
</div>

<div align="right">
  
</div>






