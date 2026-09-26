from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory

from launch_ros.actions import Node

from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


import os


def generate_launch_description():

    # robot description launch
    arm_description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("arm_bringup"), "launch", "arm_description.launch.py")
        )
    )

    # kinematics launch
    kinematics = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("arm_bringup"), "launch", "kinematics.launch.py")
        )
    )

    return LaunchDescription([
        arm_description,
        kinematics
    ])