import rclpy
from rclpy.node import Node

from arm_interfaces.msg import JointStates 
from arm_interfaces.srv import RobotParameters 

from kinematics.forward_kinematics import forward_kinematics 

import time
import numpy as np

# service call gives trajectory data, sets logging flag 
# waits for trajectory to start, keep certain number of starting angles logged 
# logs trajectory while unstable 
# stop logging when stable & @ end of trajectory 
# save data to some file 

class TrajectoryLoggerNode(Node):

    stability_time_constant = 3.

    def __init__(self):
        super().__init__('trajectory_logger_node')

        #Get Robot Parameters 
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

        #Joint State Subscriber 
        self.joint_sub = self.create_subscription(JointStates, "joint_states", self.joint_states_callback, 10)
        self.current_angles[0., 0., 0.]
        self.last_zero_update = None 

        #Main Loop
        self.timer = self.create_timer(0.01, self.timer_callback)
        self.stable = True

        self.get_logger().info("Trajectory Logger Initiated")
        pass


    def joint_states_callback(self, msg):
        #save angles 
        new_angles = [msg.base, msg.shoulder, msg.elbow]

        #angle gradient 
        DQ = new_angles - self.current_angles

        #set last_zero_update flag to current time if angles NOT changing
        if(not any(DQ)):                                                          #might need to allow for floating point errors, tiny fluctuations?

            #only update if they were changing on last update
            if(self.last_zero_update == None):
                self.last_zero_update = time.monotonic()

        #set last_zero_update flag to None if published angles ARE changing 
        else:
            self.last_zero_update = None
            pass

        #save angles 
        self.current_angles = new_angles
        pass


    def timer_callback(self):
        #set stability flag
        if(self.last_zero_update == None):
            self.stable = False 
        elif(time.monotonic() - self.last_zero_update > self.stability_time_constant):
            self.stable = True 
        pass



    def get_end_coordinates(self, angles):
        frames = np.reshape(forward_kinematics(np.array(angles), self.parameters), (6,4,4))
        return (frames[5][:3,3].astype(float)).tolist()

    pass




def main():
    rclpy.init()
    node = TrajectoryLoggerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()







