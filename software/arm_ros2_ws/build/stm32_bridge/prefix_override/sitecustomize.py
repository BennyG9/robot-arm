import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/bg99/Documents/Projects/robot-arm/software/arm_ros2_ws/install/stm32_bridge'
