from launch import LaunchDescription

from launch_ros.actions import Node


def generate_launch_description():

    fk_node = Node(
        package="kinematics",
        executable="forward_kinematics_node",
        name="forward_kinematics_node",
        output="screen",
    )

    ik_node = Node(
        package="kinematics",
        executable="inverse_kinematics_node",
        name="inverse_kinematics_node",
        output="screen",
    )


    return LaunchDescription([
        fk_node,
        ik_node,
    ])