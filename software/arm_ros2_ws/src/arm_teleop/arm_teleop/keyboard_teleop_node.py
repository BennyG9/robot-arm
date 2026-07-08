import rclpy
from rclpy.node import Node

from arm_interfaces.srv import Calibrate
from arm_interfaces.srv import Home
from arm_interfaces.msg import JointTargets

from pynput import keyboard
import time

class KeyboardTeleopNode(Node):

    def __init__(self):
        super().__init__('keyboard_teleop_node')

        #Services
        self.calibrate_client = self.create_client(Calibrate, "calibrate")
        self.home_client = self.create_client(Home, "home")

        #Keyboard listener loop
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

        #Joint Targets publisher
        self.joint_pub = self.create_publisher(JointTargets, "joint_targets", 10)

        self.get_logger().info("Keyboard Teleop Initiated")
        pass


    def on_press(self, key):
        try:
            k = key.char
        except:
            return

        if(k == 'c'):
            self.calibrate()

        elif(k == 'h'):
            self.home()

        elif(k == 'q'):
            self.get_logger().info("Closing Teleop")
            rclpy.shutdown()
        pass


    def home(self):
        request = Home.Request()
        self.home_client.call_async(request)
        pass

    def calibrate(self):
        request = Calibrate.Request()
        self.calibrate_client.call_async(request)
        pass

    def TEST(self):
        msg = JointTargets()
        msg.base = 45.0
        msg.shoulder = 45.0
        self.joint_pub.publish(msg)
        pass

    pass


def main():
    rclpy.init()
    node = KeyboardTeleopNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
