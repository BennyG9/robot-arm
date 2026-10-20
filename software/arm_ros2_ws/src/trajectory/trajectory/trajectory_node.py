import rclpy
from rclpy.node import Node

from arm_interfaces.srv import RobotParameters
from arm_interfaces.srv import GetTrajectory

from trajectory.generate_path import *
from trajectory.path_to_angles import path_to_angles
from trajectory.time_parameterization import *

import numpy as np

class Trajectory_Node(Node):

    def __init__(self):
        super().__init__('trajectory_node')

        # request trajectory data service 
        self.trajectory_srv = self.create_service(
            GetTrajectory,
            "get_trajectory",
            self.get_trajectory_callback
        )

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


    def get_trajectory_callback(self, request, response):
        #self.get_logger().info("trajectory request received...")

        #request. {trajectory_type, starting_angles, pos1, pos2, radius, resolution}
        #response. {trajectory_length, time_param_func, angles}

        response.trajectory_length = 0
        response.time_param_func = []
        response.angles = []
        
        match(request.trajectory_type):

            # linear trajectory between 2 cartersian coordinates, starting angles given
            case "linear":
                starting_angles = np.array(request.starting_angles)

                # generate path
                path = linear_path(request.pos1, request.pos2, request.resolution)
                Q = path_to_angles(path, self.parameters)

                # choose path corresponding to given starting angles
                path_index = None
                for i in range(4):
                    if(np.allclose(Q[i, :, 0], starting_angles)):
                        path_index = i
                        break
                if(path_index == None): 
                    self.get_logger().error("Unable to generate llinear trajectory")
                    raise Exception("No Path Index Found...")
                path_angles = Q[:][path_index][:]

                # get time dependence
                time_param_func = min_path_time_func(path_angles, self.parameters)

                # stuff into response
                trajectory_length = path_angles.shape[1]
                response.trajectory.length = trajectory_length
                response.trajectory.angles = np.reshape(path_angles, (3*trajectory_length))
                response.trajectory.time_parameterization_function = time_param_func
                
                return response
                

            # catch-all, trajectory type given does not exist
            case _:
                self.get_logger.error("No trajectory type: " + request.type)
                return response
        
        return response
    
pass



def main():
    rclpy.init()
    node = Trajectory_Node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
