Write-Host "Build Communication Protocol..."


# copy protocol.json to ROS2 communication pkg
cp protocol.json ../software/arm_ros2_ws/src/stm32_bridge/stm32_bridge/


# generate protocol files for STM32 firmware


Write-Host "Built Communication Protocol"
