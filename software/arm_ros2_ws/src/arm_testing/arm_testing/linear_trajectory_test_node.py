import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from arm_interfaces.srv import RobotParameters 
from arm_interfaces.srv import Calibrate 
from arm_interfaces.srv import Home
from arm_interfaces.srv import GetTrajectory

from arm_interfaces.msg import JointStates 

from arm_interfaces.action import FollowTrajectory 

from kinematics.forward_kinematics import forward_kinematics 

import time

import numpy as np
rng = np.random.default_rng()


# TODO:
#       loop state machine
#       joint state logger
#       /is stable signal/
#       /randomized trajectory request/ 
#       /actively executing flag/ 
#       /initial calibrate and home/



class LinearTrajectoryTest(Node):

    stability_time_constant = 3.

    def __init__(self):
        super.__init__("linear_trajectory_test_node")

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

        #Calibration
        self.calibrate_client = self.create_client(Calibrate, "calibrate")

        #Homing
        self.home_clinet = self.create_client(Home, "home")

        #Trajectory Generation + Execution
        self.traj_client = self.create_client(GetTrajectory, "get_trajectory")
        self._trajectory_client = ActionClient(
            self,
            FollowTrajectory,
            'follow_trajectory'
        )
        self.trajectory_active = False        

        #Joint state subscriber 
        self.joint_sub = self.create_subscription(JointStates, "joint_states", self.joint_states_callback, 10)
        self.current_angles = [0., 0., 0.]
        self.last_zero_update = None
        self.stable = True

        # timer
        self.timer = self.create_timer(0.01, self.timer_callback)

        self.get_logger().info("Linear Trajectory Test Starting...")

        self.startup()
        pass


    #initialize variables and setup robot
    def startup(self):
        # calibrate
        cal_request = Calibrate.Request()
        self.calibrate_client.call_async(cal_request)

        # home
        home_request = Home.Request()                        #test whether delay needs to be added
        self.home_clinet.call_async(home_request)
        pass


    #subscriber callback for JointStates
    def joint_states_callback(self, msg):
        #save angles 
        new_angles = [msg.base, msg.shoulder, msg.elbow]

        #angle gradient 
        DQ = new_angles - self.current_angles

        #set last_zero_update flag to current time if angles NOT changing
        if(not any(DQ)):                                                             #might need to allow for floating point errors, tiny fluctuations?

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


    # 100 Hz loop, set stability flag
    def timer_callback(self):
        #Stability Flag
        #unstable if actively requesting/executing trajectory
        if(self.trajectory_active):
            self.stable = False
        #unstable if angles are actively changing 
        elif(self.last_zero_update == None):
            self.stable = False
        #set to stable if last zero was long enough ago 
        elif(time.monotonic() - self.last_zero_update > self.stability_time_constant):
            self.stable = True
        pass




    #start request + execution chain for trajectory with randomized end point 
    def random_trajectory(self):
        #trajectory flag
        self.trajectory_active = True

        #stuff trajectory data request 
        request = GetTrajectory.Request()
        request.trajectory_type = "linear"
        request.starting_angles = (np.radians(self.current_angles).astype(float)).tolist()
        request.pos1 = self.get_end_coordinates(self.current_angles)
        request.pos2 = self.get_end_coordinates(self.random_angles())
        request.radius = 0.
        request.resolution = 200

        #call new function when data received 
        future = self.traj_client.call_async(request)
        future.add_done_callback(self.trajectory_data_request_callback)
        pass

    #trajectory data received 
    def trajectory_data_request_callback(self, future):
        #get trajectory data from future
        trajectory = future.result().trajectory
        trajectory.time_parameterization_function = [dt + 0.03 for dt in trajectory.time_parameterization_function]

        #initialize action goal
        goal = FollowTrajectory.Goal()
        goal.trajectory = trajectory 

        #send goal and pass callbacks 
        self._trajectory_client.wait_for_server()
        send_goal_future = self._trajectory_client.send_goal_async(goal, feedback_callback=self.trajectory_feedback_callback)
        send_goal_future.add_done_callback(self.trajectory_response_callback)
        pass

    # sees whether action server accepted or rejected trajectory 
    def trajectory_response_callback(self, future):
        goal_handle = future.result()

        # log result 
        if(not goal_handle.accepted):
            self.get_logger().warning("Trajectory Not Accepted..")
            return 
        self.get_logger().info("Starting Trajectory Execution...")

        # start action and call function on completion
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.trajectory_result_callback)
        pass

    # done callback
    def trajectory_result_callback(self, future):
        wrapped_result = future.result()
        result = wrapped_result.result

        # log result
        if(wrapped_result.status == 4 and result.success):
            self.get_logger().info("Trajectory Completed Successfully")

        else:
            self.get_logger().info("Trajectory Quit")

        # set active flag back to false
        self.trajectory_active = False
        pass

    #not currently doing anything with feedback data
    def trajectory_feedback_callback(self, feedback_msg):
        pass



    #helper function that converts angles to end-effector position
    def get_end_coordinates(self, angles):
        frames = np.reshape(forward_kinematics(np.array(angles), self.parameters), (6,4,4))
        return (frames[5][:3,3].astype(float)).tolist()

    #helper function that generates nice random angles within robot specs
    def random_angles(self):
        angles = [
            #phi on [base_min, base_max]
            rng.uniform(self.parameters.base_joint_min, self.parameters.base_joint_max),

            #theta1 on [0, shoulder_max]
            rng.uniform(0., self.parameters.shoulder_joint_max),

            #theta2 on [elbow_min, 0]
            rng.uniform(self.parameters.elbow_joint_min, 0.)
        ]
        return angles 

pass



def main():
    rclpy.init()
    node = LinearTrajectoryTest()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()