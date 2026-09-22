import rclpy
from rclpy.node import Node

from arm_interfaces.srv import InverseKinematics
from arm_interfaces.srv import RobotParameters
from kinematics.inverse_kinematics import inverse_kinematics

import numpy as np

class IKNode(Node):

    def __init__(self):
        super().__init__('ik_node')

        # ik service
        self.inverse_kinematics_srv = self.create_service(
            InverseKinematics,
            "ik",
            self.ik_callback
        )

        # grab robot config data
        self.parameters = {}
        self.parameters_client = self.create_client(RobotParameters, "robot_parameters")
        request = RobotParameters.request()
        self.future = self.parameters_client.call_async(request)
        parameter_data = self.result
        for i in range(len(parameter_data.names)):
            self.parameters[parameter_data.names[i]] = float(parameter_data.parameters[i])

        self.get_logger().info("Inverse Kinematics Initiated")
        pass


    def ik_callback(self, request, response):
        valid, configs = inverse_kinematics(request.coordinates, self.parameters)
        response.validity = valid
        response.configurations = np.reshape(configs, (1, 12))
        return response
pass



def main():
    rclpy.init()
    node = IKNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()