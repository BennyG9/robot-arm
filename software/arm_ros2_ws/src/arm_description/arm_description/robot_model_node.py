import rclpy
from rclpy.node import Node

from pathlib import Path
from ament_index_python.packages import (
    get_package_share_directory,
)

from arm_interfaces.srv import RobotParameters 
from arm_description.parse_urdf import parse_kinematics_parameters


class RobotModelNode(Node):

    def __init__(self):
        super().__init__("robot_model_node")

        # get path to robot.urdf.xacro file containing robot config
        package_directory = Path(get_package_share_directory("arm_description"))
        xacro_path = package_directory / "urdf" / "robot.urdf.xacro"

        # extract relevant parameters 
        self.parameters = parse_kinematics_parameters(str(xacro_path))

        # fk service
        self.robot_parameters_srv = self.create_service(
            RobotParameters,
            "robot_parameters",
            self.robot_parameters_callback
        )
        
        self.get_logger().info("Service Ready: /RobotParameters")
        pass


    def robot_parameters_callback(self, request, response):
        response.names = self.parameters.keys()
        response.parameters = self.parameters.values()
        return response

    pass



def main(args=None):
    rclpy.init(args=args)

    node = RobotModelNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()