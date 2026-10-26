import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient 

from arm_interfaces.srv import Calibrate
from arm_interfaces.srv import Home
from arm_interfaces.srv import InverseKinematics
from arm_interfaces.srv import ForwardKinematics 
from arm_interfaces.srv import RobotParameters
from arm_interfaces.srv import GetTrajectory

from arm_interfaces.msg import JointTargets
from arm_interfaces.msg import JointStates

from arm_interfaces.action import FollowTrajectory

from kinematics.forward_kinematics import forward_kinematics

import time
import curses
import numpy as np

class KeyboardTeleopNode(Node):

    def __init__(self):
        super().__init__('keyboard_teleop_node')

        #Calibrate service 
        self.calibrate_client = self.create_client(Calibrate, "calibrate")

        #Homing service 
        self.home_client = self.create_client(Home, "home")

        #Forward Kinematics 
        self.fk_client = self.create_client(ForwardKinematics, "fk")
        self.current_coordinates = [0.0,0.0,0.0]

        #Inverse Kinematics 
        self.ik_client = self.create_client(InverseKinematics, "ik")
        self.ik_test = {"base":0.0, "shoulder":0.0, "elbow": 0.0}

        #Joint Targets publisher
        self.joint_pub = self.create_publisher(JointTargets, "joint_targets", 10)

        #Joint State subscriber
        self.joint_sub = self.create_subscription(JointStates, "joint_states", self.joint_states_callback, 10)
        self.current_states = {"base":0.0, "shoulder":0.0, "elbow": 0.0}

        #Trajectory Service + Action
        self.traj_client = self.create_client(GetTrajectory, 'get_trajectory')
        self._trajectory_client = ActionClient(
            self,
            FollowTrajectory,
            'follow_trajectory'
        )
        self.trajectory_active = False
        self.trajectory_status = ""
        self.trajectory_progress = 0.

        #Keyboard Control Variables
        self.selected_joint = None
        self.current_targets = {"base":0.0, "shoulder":0.0, "elbow": 0.0}
        self.increment = 1.0
        self.joint_ranges = {"base":{"min":(-90.0), "max":(80.0)}, "shoulder":{"min":(-90.0), "max":(78.0)}, "elbow":{"min":(-90.0), "max":(119.0)}}

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

        self.get_logger().info("Keyboard Teleop Initiated")
        pass


    def joint_states_callback(self, msg):
        # save current angles
        self.current_states["base"] = msg.base
        self.current_states["shoulder"] = msg.shoulder
        self.current_states["elbow"] = msg.elbow

        # save corresponding cartesian coordinate 
        self.log_coordinates()

        # test IK
        #self.get_ik_result()
        pass


    def handle_key(self, k):

        if((not self.trajectory_active) and k == ord('c')):
            self.calibrate()

        elif(not self.trajectory_active) and k == ord('h')):
            self.home()

        elif(k == ord('1')):
            self.selected_joint = "base"
        elif(k == ord('2')):
            self.selected_joint = "shoulder"
        elif(k == ord('3')):
            self.selected_joint = "elbow"

        elif((not self.trajectory_active) and self.selected_joint != None and k == ord('w')):
            self.current_targets[self.selected_joint] += self.increment
            if(self.current_targets[self.selected_joint] > self.joint_ranges[self.selected_joint]["max"]):
                self.current_targets[self.selected_joint] = self.joint_ranges[self.selected_joint]["max"]
            self.send_targets()
        elif((not self.trajectory_active) and self.selected_joint != None and k == ord('s')):
            self.current_targets[self.selected_joint] -= self.increment
            if(self.current_targets[self.selected_joint] < self.joint_ranges[self.selected_joint]["min"]):
                self.current_targets[self.selected_joint] = self.joint_ranges[self.selected_joint]["min"]
            self.send_targets()
            
        elif(k == ord(']')):
            self.increment += 1.0
            if(self.increment > 180.0): self.increment = 180.0
        elif(k == ord('[')):
            self.increment -= 1.0
            if(self.increment < 1.0): self.increment = 1.0 

        elif((not self.trajectory_active) and k == ord('t')):
            self.TEST()

        elif(k == ord('q')):
            self.get_logger().info("Closing Teleop")
            return False
        return True


    def home(self):
        request = Home.Request()
        self.home_client.call_async(request)
        self.current_targets["base"] = 0.0
        self.current_targets["shoulder"] = 0.0
        self.current_targets["elbow"] = 0.0
        pass

    def calibrate(self):
        request = Calibrate.Request()
        self.calibrate_client.call_async(request)
        for joint, joint_range in self.joint_ranges.items():
            self.current_targets[joint] = joint_range["max"]
        pass

    def send_targets(self):
        msg = JointTargets()
        msg.base = self.current_targets["base"]
        msg.shoulder = self.current_targets["shoulder"]
        msg.elbow = self.current_targets["elbow"]
        self.joint_pub.publish(msg)
        pass


    def log_coordinates(self):
        # Using ROS2 Service Call
        # request = ForwardKinematics.Request()
        # request.angles = [self.current_states["base"], self.current_states["shoulder"], self.current_states["elbow"]]
        # future = self.fk_client.call_async(request)
        # future.add_done_callback(self.fk_response_callback)
        
        # Using Exposed Kinematics Functions Directly
        angles = [self.current_states["base"], self.current_states["shoulder"], self.current_states["elbow"]]
        frames = forward_kinematics(angles, self.parameters)
        pos = np.reshape(frames[5][:3,3], (3))
        self.current_coordinates = [100*float(pos[0]), 100*float(pos[1]), 100*float(pos[2])]
        pass

    def fk_response_callback(self, future):
        response = future.result()
        frames = np.reshape(response.frames, (6,4,4))
        coordinates = np.reshape(frames[5][:3,3], (3))
        self.current_coordinates = [float(coordinates[0]), float(coordinates[1]), float(coordinates[2])]
        pass

    def get_end_coordinates(self, angles):
        angles = np.array(angles)
        frames = np.reshape(forward_kinematics(angles, self.parameters), (6,4,4))
        return (frames[5][:3,3].astype(float)).tolist()


    def get_ik_result(self):
        #cc = "   ".join(str(item) for item in self.current_coordinates)
        #self.get_logger().error(cc)
        request = InverseKinematics.Request()
        request.coordinates = self.current_coordinates
        future = self.ik_client.call_async(request)
        future.add_done_callback(self.ik_response_callback)
        pass

    def ik_response_callback(self, future):
        response = future.result()
        configurations = np.reshape(response.configurations, (4,3))
        
        best_config = configurations[0]
        min_normsq = (best_config[0]-self.current_states["base"])**2 + (best_config[1]-self.current_states["shoulder"])**2 + (best_config[2]-self.current_states["elbow"])**2
        for i in range(1,len(configurations)):
            current_normsq = (configurations[i][0]-self.current_states["base"])**2 + (configurations[i][1]-self.current_states["shoulder"])**2 + (configurations[i][2]-self.current_states["elbow"])**2
            if(current_normsq < min_normsq):
                min_normsq = current_normsq
                best_config = configurations[i]
            pass
        self.ik_test["base"] = best_config[0]
        self.ik_test["shoulder"] = best_config[1]
        self.ik_test["elbow"] = best_config[2]
        pass

    def linear_trajectory(self, pos2):
        self.trajectory_active = True
        self.trajectory_status = "Requesting Trajectory Data"
        self.trajectory_progress = 0.

        current_angles = [self.current_states["base"], self.current_states["shoulder"], self.current_states["elbow"]]
        request = GetTrajectory.Request()
        request.trajectory_type = "linear"
        request.starting_angles = (np.radians(current_angles).astype(float)).tolist()
        request.pos1 = self.get_end_coordinates(current_angles)
        request.pos2 = pos2
        request.radius = 0.0
        request.resolution = 200

        future = self.traj_client.call_async(request)
        future.add_done_callback(self.linear_trajectory_callback)
        pass

    def linear_trajectory_callback(self, future):
        trajectory = future.result().trajectory 

        self.trajectory_status = "Requesting ROS Action"

        goal = FollowTrajectory.Goal()
        goal.trajectory = trajectory

        self._trajectory_client.wait_for_server()

        send_goal_future = self._trajectory_client.send_goal_async(goal, feedback_callback=self.trajectory_feedback_callback)
        send_goal_future.add_done_callback(self.trajectory_response_callback)
        pass

    def trajectory_response_callback(self, future):
        goal_handle = future.result()

        if(not goal_handle.accepted):
            self.trajectory_status = "ROS Action NOT Accepted"
            self.get_logger().warning("Trajectory Not Accepted...")
            return

        self.trajectory_status = "ROS Action Accepted"
        self.get_logger().info("Trajectory Accepted")

        result_future = goal_handle.get_result_async()
        self.trajectory_status = "Executing Trajectory"

        result_future.add_done_callback(self.trajectory_result_callback)
        pass

    def trajectory_feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback

        # update current targets 
        self.current_targets["base"] = feedback.current_target_angles[0]
        self.current_targets["shoulder"] = feedback.current_target_angles[1]
        self.current_targets["elbow"] = feedback.current_target_angles[2]

        # update progress tracker
        self.trajectory_progress = feedback.progress * 100
        pass

    def trajectory_result_callback(self, future):
        self.trajectory_status = "Trajectory Done"

        wrapped_result = future.result()
        result = wrapped_result.result

        if(wrapped_result.status == 4 and result.success):
            self.get_logger().info("Trajectory Completed Successfully")

        else:
            self.get_logger().warning("Trajectory Quit")

        self.trajectory_active = False
        self.trajectory_progress = 0.0
        self.trajectory_status = ""
        pass

    def TEST(self):
        end_angles = [45.0, 30.0, -60.0]

        end_pos = self.get_end_coordinates(end_angles)

        self.linear_trajectory(end_pos)
        pass

    def draw(self, stdscr):
        stdscr.clear()

        # operation data
        stdscr.addstr(0, 0, "======== Robot Arm Teleop ========")
        stdscr.addstr(2, 0, f"Selected Joint : {self.selected_joint}")
        stdscr.addstr(3, 0, f"Increment      : {self.increment} deg")

        # target angles
        stdscr.addstr(5, 0, "Target Angles")
        stdscr.addstr(6, 0, "----------------------------------")
        stdscr.addstr(7, 0, f"Base      : {self.current_targets['base']:7.2f}")
        stdscr.addstr(8, 0, f"Shoulder  : {self.current_targets['shoulder']:7.2f}")
        stdscr.addstr(9, 0, f"Elbow     : {self.current_targets['elbow']:7.2f}")

        # measured angles
        stdscr.addstr(11, 0, "Actual Angles")
        stdscr.addstr(12, 0, "----------------------------------")
        stdscr.addstr(13, 0, f"Base      : {self.current_states['base']:7.2f}")
        stdscr.addstr(14, 0, f"Shoulder  : {self.current_states['shoulder']:7.2f}")
        stdscr.addstr(15, 0, f"Elbow     : {self.current_states['elbow']:7.2f}")

        # end-effector cartesian coordinates
        stdscr.addstr(17, 0, "End Coordinates")
        stdscr.addstr(18, 0, "----------------------------------")
        stdscr.addstr(19, 0, f"X         : {self.current_coordinates[0]:7.2f}")
        stdscr.addstr(20, 0, f"Y         : {self.current_coordinates[1]:7.2f}")
        stdscr.addstr(21, 0, f"Z         : {self.current_coordinates[2]:7.2f}")

        # ik test
        #stdscr.addstr(23, 0, f"({self.ik_test['base']:7.2f}, {self.ik_test['shoulder']:7.2f}, {self.ik_test['elbow']:7.2f})")

        # trajectory, only if active
        if(self.trajectory_active):
            stdscr.addstr(23, 0, f"Trajectory Status: {self.trajectory_progress:7.2f}%, {self.trajectory_status}")

        stdscr.refresh()
        pass

    def run(self, stdscr):
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        stdscr.nodelay(True)
        stdscr.keypad(True)
        while(rclpy.ok()):
            rclpy.spin_once(self, timeout_sec=0.001)
            key = stdscr.getch()
            if(key != -1):
                if(not self.handle_key(key)): break
            self.draw(stdscr)
            time.sleep(0.05)
    pass

def main():
    rclpy.init()
    node = KeyboardTeleopNode()
#    rclpy.spin(node)
    curses.wrapper(node.run)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
