from launch import LaunchDescription

from launch_ros.actions import Node


def generate_launch_description():

    request_node = Node(
        package="trajectory",
        executable="trajectory_node",
        name="trajectory_node",
        output="screen",
    )

    execute_node = Node(
        package="trajectory",
        executable="trajectory_executor",
        name="execute_trajectory",
        output="screen",
    )


    return LaunchDescription([
        request_node,
        execute_node,
    ])
