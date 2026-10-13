import rclpy
from rclpy.node import Node

from arm_interfaces.srv import RobotParameters

from trajectory.generate_path import *
from trajectory.path_to_angles import path_to_angles

import numpy as np

class Trajectory_Node(Node):

    def __init__(self):
        super().__init__('fk_node')

        # grab robot config data
        self.parameters_client = self.create_client(RobotParameters, "robot_parameters")
        while(not self.parameters_client.wait_for_service(timeout_sec=1.0)):
            self.get_logger().info("Waiting for robot parameters service...")
        self.parameters = {}
        request = RobotParameters.Request()
        future = self.parameters_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        parameter_data = future.result()
        if(parameter_data is None):
            self.get_logger().error("Failed to retreive robot parameters")
        for i in range(len(parameter_data.names)):
            self.parameters[parameter_data.names[i]] = float(parameter_data.parameters[i])

        self.get_logger().info("Trajectory Node Initiated")
        pass


    
pass



def main():
    rclpy.init()
    node = Trajectory_Node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
