from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory

# launch nodes
from launch_ros.actions import Node

# launch launch files
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

import os


def generate_launch_description():

    teleop_node = Node(
        package="arm_teleop",
        executable="keyboard_teleop_node",
        name="keyboard_teleop_node",
        output="screen",
    )

    hardware = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("arm_bringup"), "launch", "hardware.launch.py")
        )
    )

    return LaunchDescription([
        teleop_node,
        hardware,
    ])
