import rclpy
from rclpy.node import Node
#from rclpy.action import ActionServer, GoalResponse, CancelResponse

from arm_interfaces.srv import Calibrate
from arm_interfaces.srv import Home
from arm_interfaces.msg import JointStates
from arm_interfaces.msg import JointTargets
#from arm_interfaces.action import FollowTrajectory 

from .protocol import Protocol

import time
import math
import numpy as np

class STM32Bridge(Node):

    def __init__(self):
        super().__init__('stm32_bridge')

        #Serial communication
        self.protocol = Protocol()

        #Joint State publisher
        self.joint_pub = self.create_publisher(JointStates, "joint_states", 10)

        #Joint Target listener
        self.joint_sub = self.create_subscription(JointTargets, "joint_targets", self.joint_targets_callback, 10)

        #Services
        self.calibrate_srv = self.create_service(
            Calibrate,
            "calibrate",
            self.calibrate_callback
        )
        self.home_srv = self.create_service(
            Home,
            "home",
            self.home_callback
        )

        #Communication loop
        self.comms_timer = self.create_timer(0.0001, self.read_serial)

        #Clear serial
        self.protocol.clear_serial()

        #Trajectory Action
        # self.active_trajectory_action = False #active flag
        # self.active_trajectory_last_timestamp = None #used for timing
        # self.active_trajectory_goal_handle = None #goal_handle object
        # self.active_trajectory_angles = None #store reshaped angles array
        # self.active_trajectory_index = -1 #current point in active trajectory 
        # self.active_trajectory = type("Active_Trajectory_Variables", (), 
        #     {
        #         "active_action": False,                    #active flag
        #         "last_timestamp": -1,                      #timing variable
        #         "goal_handle": None,                       #goal_handle object
        #         "angles": None,                            #reshaped path angles array
        #         "time_parameterization_function": None,    #store time_param function
        #         "length": -1,                              #number of points in path
        #         "index": -1,                               #current point in path
        #         "result": None,                            #action return object
        #         "feedback": None,                          #action feedback object
        #     }       
        # )
        # self._action_server = ActionServer(
        #     self,
        #     FollowTrajectory,
        #     'follow_trajectory',
        #     execute_callback=self.trajectory_execute_callback,
        #     goal_callback=self.trajectory_goal_callback,
        #     cancel_callback=self.trajectory_cancel_callback
        # )
        # self.traj_timer = self.create_timer(0.001, self.trajectory_timer_callback)

        self.get_logger().info("STM32 Bridge Initiated")
        pass

    def read_serial(self):

        # check for packet
        packet = self.protocol.read_packet()

        if(packet == None):
            return
        if(packet == -1):
            print("CHECKSUM ERROR")
            return

        # parse packet
        command, args = self.protocol.parse_packet(packet)

        # executables
        if(self.protocol.get_direction(command) == "JETSON_TO_STM32"):
            pass

        if(command == "JOINT_STATE"):
            self.publish_joint_states(args[0])
            pass

        elif(command == "ERROR_MSG"):
            self.get_logger().info("ERROR CODE: " + str(args[0][0]))
            pass

        pass


    def calibrate_callback(self, request, response):
        self.get_logger().info("Calibrate Command Sent")
        self.protocol.write_packet("CALIBRATE")
        response.success = True
        return response


    def home_callback(self, request, response):
        self.get_logger().info("Home Command Sent")
        self.protocol.write_packet("HOME")
        response.success = True
        return response


    def publish_joint_states(self, joint_angles):
        msg = JointStates()
        msg.base = joint_angles[0]
        msg.shoulder = joint_angles[1]
        msg.elbow = joint_angles[2]
        self.joint_pub.publish(msg)
        pass


    def joint_targets_callback(self, msg):
        self.protocol.write_packet("SET_POSITION", msg.base, msg.shoulder, msg.elbow)
        pass

    # Start trajectory action
    # def trajectory_goal_callback(self, goal_request):

    #     #TODO: add conditions for rejecting trajectory 

    #     return GoalResponse.ACCEPT

    # # Cancel trajectory action
    # def trajectory_cancel_callback(self, goal_handle):
    #     return CancelResponse.ACCEPT

    # Start trajectory action
    # def trajectory_execute_callback(self, goal_handle):
    #     #Set trajectory action flags
    #     #self.active_trajectory.active_action = True
    #     self.active_trajectory.last_timestamp = -1

    #     #Hand over active goal_handle object for timer callback 
    #     #self.active_trajectory.goal_handle = goal_handle
    #     #self.active_trajectory.result = FollowTrajectory.Result()
    #     #self.active_trajectory.feedback = FollowTrajectory.Feedback()

    #     #Stuff with important variables 
    #     #self.active_trajectory
    #     #self.active_trajectory.time_parameterization_function = goal_handle.request.trajectory.time_parameterization_function
    #     #self.active_trajectory.length = goal_handle.request.trajectory.length
    #     #self.active_trajectory.angles = np.rad2deg(np.reshape(goal_handle.request.trajectory.angles, (3,self.active_trajectory.length)))
    #     pass

    # def trajectory_timer_callback(self):
    #     # NOTE: trajectory indexed by index+1, time_param indexed by index+0

    #     # check if trajectory is done & return upon sucessfult completion
    #     if(self.active_trajectory.index == self.active_trajectory.length-1):
    #         self.active_trajectory.goal_handle.succeed()
    #         self.active_trajectory.result.sucess = True
    #         return self.active_trajectory.result

    #     # cancel request, auto-accept 
    #     # if(self.active_trajectory.goal_handle.is_cancel_requested):
    #     #     self.active_trajectory.goal_handle.canceled()
    #     #     self.active_trajectory.result.success = False
    #     #     return self.active_trajectory.result

    #     # first point in trajectory
    #     if(self.active_trajectory.last_timestamp == -1):

    #         # send angles 
    #         current_angles = self.active_trajectory.angles[:, self.active_trajectory.index+1]
    #         self.protocol.write_packet("SET_POSITION", current_angles[0], current_angles[1], current_angles[2])

    #         # set time
    #         self.active_trajectory.last_timestamp = time.monotonic()

    #         # action feedback
    #         self.active_trajectory.feedback.progress = (self.active_trajectory.index+1) / self.active_trajectory.length
    #         self.active_trajectory.current_target_angles = current_angles
    #         self.active_trajectory.goal_handle.publish_feedback() 

    #     # rest of trajectory
    #     else:

    #         # # timing data
    #         # current_time = time.monotonic()
    #         # time_interval = current_time - self.active_trajectory.last_timestamp

    #         # # immediately break if interval is less than current time parameters
    #         # if(time_interval < self.active_trajectory.time_parameterization_function[self.active_trajectory.index]):
    #         #     return

    #         # # send angles
    #         # current_angles = self.active_trajectory.angles[:, self.active_trajectory.index+1]
    #         # self.protocol.write_packet("SET_POSITION", current_angles[0], current_angles[1], current_angles[2])

    #         # # iterate for next time step
    #         # self.active_trajectory.last_timestamp = time.monotonic()
    #         # self.active_trajectory.index += 1

    #         # # action feedback
    #         # self.active_trajectory.feedback.progress = (self.active_trajectory.index+1) / self.active_trajectory.length
    #         # self.active_trajectory.feedback.current_target_angles = current_angles 
    #         # self.active_trajectory.goal_handle.publish_feedback() 
    #         pass

        # pass

    

    pass


def main():
    rclpy.init()
    node = STM32Bridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
