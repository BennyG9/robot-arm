from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory

from launch_ros.actions import Node

from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

import os

def generate_launch_description():

    # STM32 interface
    hardware = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("arm_bringup"), "launch", "hardware.launch.py")
        )
    )

    # description + parameters + validation + kinematics 
    robot_model = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("arm_bringup"), "launch", "robot_model.launch.py")
        )
    )

    # trajectory generation and execution
    trajectory = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("arm_bringup"), "launch", "trajectory.launch.py")
        )
    )

    return LaunchDescription([
        hardware,
        robot_model,
        trajectory,
    ])