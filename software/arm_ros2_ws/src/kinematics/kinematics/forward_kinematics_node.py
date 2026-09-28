import rclpy
from rclpy.node import Node

from arm_interfaces.srv import ForwardKinematics
from arm_interfaces.srv import RobotParameters
from kinematics.forward_kinematics import forward_kinematics

import numpy as np

class FKNode(Node):

    def __init__(self):
        super().__init__('fk_node')

        # fk service
        self.forward_kinematics_srv = self.create_service(
            ForwardKinematics,
            "fk",
            self.fk_callback
        )

        # grab robot config data
        while(not self.parameters_client.wait_for_service(timeout_sec=1.0)):
            self.get_logger().info("Waiting for robot parameters service...")
        self.parameters = {}
        self.parameters_client = self.create_client(RobotParameters, "robot_parameters")
        request = RobotParameters.request()
        future = self.parameters_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        parameter_data = future.result()
        if(parameter_data is None):
            self.get_logger().error("Failed to retreive robot parameters")
        for i in range(len(parameter_data.names)):
            self.parameters[parameter_data.names[i]] = float(parameter_data.parameters[i])

        self.get_logger().info("Forward Kinematics Initiated")
        pass


    def fk_callback(self, request, response):
        frames = forward_kinematics(request.angles, self.parameters)
        response.frames = np.reshape(frames, (1, 96))
        return response
pass



def main():
    rclpy.init()
    node = FKNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()