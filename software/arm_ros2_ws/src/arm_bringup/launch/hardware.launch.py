from launch import LaunchDescription

from launch_ros.actions import Node


def generate_launch_description():

    stm32_bridge = Node(
        package="stm32_bridge",
        executable="stm32_interface_node",
        name="stm32_interface_node",
        output="screen",
    )


    return LaunchDescription([
        stm32_bridge,
    ])
