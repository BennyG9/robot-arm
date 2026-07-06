import rclpy
from rclpy.node import Node

from arm_interfaces.srv import Calibrate
from arm_interfaces.srv import Home

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

        self.get_logger().info("Keyboard Teleop Initiated")

        time.sleep(2)
        self.calibrate()
        time.sleep(1)
        self.home()
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

    pass


def main():
    rclpy.init()
    node = KeyboardTeleopNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
