import rclpy
from rclpy.node import Node

from arm_interfaces.srv import ForwardKinematics
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

        self.get_logger().info("Forward Kinematics Initiated")
        pass


    def fk_callback(self, request, response):
        frames = forward_kinematics(request.angles)
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