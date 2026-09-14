import rclpy
from rclpy.node import Node

from arm_interfaces.srv import ForwardKinematics

import numpy as np
import math

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


    def get_transformation_matrices(self, q):
        phi = q[0]
        theta1 = q[1]
        theta2 = q[2]

        # Ground - ground transform
        T0 = np.array([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])

        # Ground - top of base transform    rotz(-phi)
        T01 = np.array([[math.cos(-phi), -math.sin(-phi), 0, 0],
                        [math.sin(-phi), math.cos(-phi), 0, 0],
                        [0, 0, 0, base_height],
                        [0, 0, 0, 1]])

        # Top of base - shoulder transform  rotx(-theta1)
        T12 = np.array([[1, 0, 0, 0],
                        [0, math.cos(-theta1), -math.sin(-theta1), 0],
                        [0, math.sin(-theta1), math.cos(-theta1), L1],
                        [0, 0, 0, 1]])

        # Shoulder - elbow1 transform   roty(pi/2)
        T23 = np.array([[0, 0, 1, 0],
                        [0, 1, 0, 0],
                        [-1, 0, 0, L2],
                        [0, 0, 0, 1]])

        # Elbow1 - elbow2 transform     roty(-pi/2) * rotx(theta2)
        T34 = np.array([[0, -math.sin(theta2), -math.cos(theta2), 0],
                        [0, math.cos(theta2), -math.sin(theta2), 0],
                        [1, 0, 0, l3],
                        [0, 0, 0, 1]])

        # Elbow2 - end effector transform
        T45 = np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, L3],
                        [0, 0, 0, 1]])

        return [T0, T01, T12, T23, T34, T45]

    def forward_kinematics(self, q):

        transformations = self.get_transformation_matrices(q)

        frames = transformations
        for i in range(1, len(frames)):
            frames[i] = frames[i-1] @ frames[i]
            pass

        return frames


    def fk_callback(self, request, response):
        frames = self.forward_kinematics(request.angles)
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