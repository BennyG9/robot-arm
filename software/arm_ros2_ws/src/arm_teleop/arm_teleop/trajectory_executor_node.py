import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse 

from arm_interfaces.action import FollowTrajectory
from arm_interfaces.msg import JointTargets

import numpy as np

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

        self.start_trajectory(goal_handle)

        result = await self.completion_future


        pass


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

        # First point in trajectory *********

        self.active = True
        pass


    # stop trajectory and clean up environment 
    def end_trajectory(self):

        pass
    

    # run execution code at fixed rate
    def timer_callback(self):

        pass





    pass