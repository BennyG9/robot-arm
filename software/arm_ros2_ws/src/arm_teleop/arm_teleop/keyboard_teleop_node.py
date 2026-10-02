import rclpy
from rclpy.node import Node

from arm_interfaces.srv import Calibrate
from arm_interfaces.srv import Home
from arm_interfaces.srv import InverseKinematics
from arm_interfaces.srv import ForwardKinematics 

from arm_interfaces.msg import JointTargets
from arm_interfaces.msg import JointStates

import time
import curses
import numpy as np

class KeyboardTeleopNode(Node):

    def __init__(self):
        super().__init__('keyboard_teleop_node')

        #Services
        self.calibrate_client = self.create_client(Calibrate, "calibrate")
        self.home_client = self.create_client(Home, "home")
        self.fk_client = self.create_client(ForwardKinematics, "forward_kinematics")
        self.current_coordinates = [0,0,0]

        self.ik_client = self.create_client(InverseKinematics, "inverse_kinematics")
        self.ik_test = {"base":0.0, "shoulder":0.0, "elbow": 0.0}

        #Joint Targets publisher
        self.joint_pub = self.create_publisher(JointTargets, "joint_targets", 10)

        #Joint State subscriber
        self.joint_sub = self.create_subscription(JointStates, "joint_states", self.joint_states_callback, 10)
        self.current_states = {"base":0.0, "shoulder":0.0, "elbow": 0.0}

        #Keyboard Control variables
        self.selected_joint = None
        self.current_targets = {"base":0.0, "shoulder":0.0, "elbow": 0.0}
        self.increment = 1.0
        self.joint_ranges = {"base":{"min":(-90.0), "max":(80.0)}, "shoulder":{"min":(-90.0), "max":(78.0)}, "elbow":{"min":(-90.0), "max":(119.0)}}

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
        self.get_ik_result()
        pass


    def handle_key(self, k):

        if(k == ord('c')):
            self.calibrate()

        elif(k == ord('h')):
            self.home()

        elif(k == ord('1')):
            self.selected_joint = "base"
        elif(k == ord('2')):
            self.selected_joint = "shoulder"
        elif(k == ord('3')):
            self.selected_joint = "elbow"

        elif(self.selected_joint != None and k == ord('w')):
            self.current_targets[self.selected_joint] += self.increment
            if(self.current_targets[self.selected_joint] > self.joint_ranges[self.selected_joint]["max"]):
                self.current_targets[self.selected_joint] = self.joint_ranges[self.selected_joint]["max"]
            self.send_targets()
        elif(self.selected_joint != None and k == ord('s')):
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

        elif(k == ord('t')):
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
        request = ForwardKinematics.Request()
        request.angles = [self.current_states["base"], self.current_states["shoulder"], self.current_states["elbow"]]
        future = self.fk_client.call_async(request)
        future.add_done_callback(self.fk_response_callback)
        pass

    def fk_response_callback(self, future):
        response = future.result()
        frames = np.reshape(response.frames, (6,4,4))
        self.current_coordinates = (frames[5][:3][3]).reshape(1,3);
        pass


    def get_ik_result(self):
        request = InverseKinematics.Request()
        request.coordinates = self.current_coordinates
        future = self.ik_client.call_async(request)
        future.add_done_callback(self.ik_response_callback)
        pass

    def ik_response_callback(self, future):
        response = future.response()
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

    def TEST(self):

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
        stdscr.addstr(23, 0, f"IK Results")
        stdscr.addstr(24, 0, f"----------------------------------")
        stdscr.addstr(25, 0, f"Base      : {self.ik_test['base']:7.2f}")
        stdscr.addstr(26, 0, f"Shoulder  : {self.ik_test['shoulder']:7.2f}")
        stdscr.addstr(27, 0, f"Elbow     : {self.ik_test['elbow']:7.2f}")

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
