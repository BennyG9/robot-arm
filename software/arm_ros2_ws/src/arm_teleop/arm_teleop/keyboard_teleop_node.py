import rclpy
from rclpy.node import Node

from arm_interfaces.srv import Calibrate
from arm_interfaces.srv import Home
from arm_interfaces.msg import JointTargets
from arm_interfaces.msg import JointStates

import time
import curses

class KeyboardTeleopNode(Node):

    def __init__(self):
        super().__init__('keyboard_teleop_node')

        #Services
        self.calibrate_client = self.create_client(Calibrate, "calibrate")
        self.home_client = self.create_client(Home, "home")

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
        self.current_states["base"] = msg.base
        self.current_states["shoulder"] = msg.shoulder
        self.current_states["elbow"] = msg.elbow
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
        #self.current_targets["base"] = 80.0
        #self.current_targets["shoulder"] = 78.0
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

    def TEST(self):

        pass

    def draw(self, stdscr):
        stdscr.clear()
        #stdscr.erase()
        stdscr.addstr(0, 0, "======== Robot Arm Teleop ========")
        stdscr.addstr(2, 0, f"Selected Joint : {self.selected_joint}")
        stdscr.addstr(3, 0, f"Increment      : {self.increment} deg")
        stdscr.addstr(5, 0, "Target Angles")
        stdscr.addstr(6, 0, "----------------------------------")
        stdscr.addstr(7, 0, f"Base      : {self.current_targets['base']:7.2f}")
        stdscr.addstr(8, 0, f"Shoulder  : {self.current_targets['shoulder']:7.2f}")
        stdscr.addstr(9, 0, f"Elbow     : {self.current_targets['elbow']:7.2f}")
        stdscr.addstr(11, 0, "Actual Angles")
        stdscr.addstr(12, 0, "----------------------------------")
        stdscr.addstr(13, 0, f"Base      : {self.current_states['base']:7.2f}")
        stdscr.addstr(14, 0, f"Shoulder  : {self.current_states['shoulder']:7.2f}")
        stdscr.addstr(15, 0, f"Elbow     : {self.current_states['elbow']:7.2f}")
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
