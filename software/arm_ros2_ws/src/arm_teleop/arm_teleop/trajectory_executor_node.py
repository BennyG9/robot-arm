import rclpy
from rclpy.node import Node
from rclpy.task import Future
from rclpy.action import ActionServer, GoalResponse, CancelResponse 

from arm_interfaces.action import FollowTrajectory
from arm_interfaces.msg import JointTargets

import numpy as np
import time 

class TrajectoryExecutorNode(Node):

    def __init__(self):
        super().__init__('trajectory_executor_node')

        #Joint Targets publisher
        self.joint_pub = self.create_publisher(JointTargets, 'joint_targets', 10)

        #Trajectory Action
        self._action_server = ActionServer(
            self,
            FollowTrajectory,
            'follow_trajectory',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

        #Trajectory execution timer
        self.timer = self.create_timer(0.001, self.timer_callback)

        #Trajectory variables 
        self.active = False
        self.completion_future = None
        self.goal_handle = None
        self.last_timestamp = -1
        self.result = None
        self.feedback = None
        self.index = -1
        self.trajectory = type("Trajectory", (), 
            {
                "angles": None,
                "time_parameterization_function": None,
                "length": -1
            }
        )

        self.get_logger().info("Trajectory Action Server Initiated")
        pass


    async def execute_callback(self, goal_handle):

        # set trajectory variables 
        self.start_trajectory(goal_handle)

        # wait for completion flag asynchronously 
        done = await self.completion_future

        # save return result and reset
        result = self.result.success
        self.end_trajectory()

        return result


    def goal_callback(self, goal_handle):
        # ADD CONDITIONS FOR REJECTING ACTION REQUEST
        return GoalResponse.ACCEPT


    def cancel_callback(self, goal_handle):
        # ADD CONDITIONS FOR REJECTING CANCEL REQUEST
        return CancelResponse.ACCEPT


    # initialize all trajectory variables 
    def start_trajectory(self, goal_handle):

        # Action objects
        self.completion_future = Future()
        self.goal_handle = goal_handle
        self.result = FollowTrajectory.Result()
        self.feedback = FollowTrajectory.Feedback()

        # Trajectory Data
        trajectory_data = goal_handle.request.trajectory
        self.trajectory.angles = np.rad2deg(np.reshape(trajectory_data.angles, (3,trajectory_data.length)))
        self.trajectory.time_parameterization_function = trajectory_data.time_parameterization_function
        self.trajectory.length = trajectory_data.length
        self.index = 0

        # Publish first point in trajectory 
        current_angles = self.trajectory.angles[:, self.index]
        msg = JointTargets()
        msg.base, msg.shoulder, msg.elbow = current_angles[0], current_angles[1], current_angles[2]
        #*********self.joint_pub.publish(msg)

        self.active = True
        pass


    # stop trajectory and clean up environment 
    def end_trajectory(self):
        self.active = False

        # Action objects
        self.completion_future = None
        self.goal_handle = None
        self.result = None
        self.feedback = None

        # Trajectory data
        self.trajectory.angles = None
        self.trajectory.time_parameterization_function = None
        self.trajectory.length = None
        self.index = -1
        self.last_timestamp = -1
        pass
    

    # run execution code at fixed rate
    def timer_callback(self):

        # check for active flag 
        if(not self.active):
            return

        # check for cancel request
        if(self.goal_handle.is_cancel_requested):
            self.goal_handle.canceled()
            self.result.success = False
            self.completion_future.set_result(True)
            return

        # Trajectory after first point

        # timing 
        current_time = time.monotonic()
        time_interval = current_time - self.last_timestamp
        if(time_interval < self.trajectory.time_parameterization_function[self.index]):
            return

        # publish new target angles 
        current_angles = self.trajectory.angles[:, self.index+1]
        msg = JointTargets()
        msg.base, msg.shoulder, msg.elbow = current_angles[0], current_angles[1], current_angles[2]
        #*********self.joint_pub.publish(msg)

        # iterate for next time step
        self.last_timestamp = time.monotonic()
        self.index += 1

        # check for end of trajectory
        if(self.index+1 == self.trajectory.length):
            self.goal_handle.succeed()
            self.result.success = True
            self.completion_future.set_result(True)
            return

        # action feedback 
        self.feedback.progress = (self.index + 1) / self.trajectory.length
        self.feedback.current_target_angles = current_angles 
        self.goal_handle.publish_feedback()
        pass

    pass