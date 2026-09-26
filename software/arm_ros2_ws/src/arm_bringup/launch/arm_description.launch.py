from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

import os
import xacro


def generate_launch_description():

    # xacro file
    package_dir = get_package_share_directory("arm_description")
    xacro_file = os.path.join(package_dir, "urdf", "robot.urdf.xacro")
    arm_description = xacro.process_file(xacro_file).toxml()

    # state publisher
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {
                'robot_description': arm_description
            }
        ]
    )

    # model export node
    robot_model_node = Node(
        package="arm_description",
        executable="robot_model_node",
        name="robot_model_node",
        output="screen"
    )

    # validation node
    validation_node = Node(
        package="arm_description",
        executable="validation_node",
        name="validation_node",
        output="screen"
    )

    return LaunchDescription([
        robot_state_publisher,
        robot_model_node,
        validation_node
    ])