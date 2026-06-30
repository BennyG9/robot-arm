import rclpy
from rclpy.node import Node

from arm_interfaces.srv import Calibrate
from arm_interfaces.srv import Home

from pynput import keyboard

class KeyboardTeleopNode(Node):

    def KeyboardTeleopNode(self):
        super().__init__('keyboard_teleop_node')

        #Services
        self.calibrate_client = self.create_client(Calibrate, "calibrate")
        self.home_client = self.create_client(Home, "home")

        #Keyboard listener
        self.listener = keyboard.Listener(on_press=self.on_press)

        self.get_logger().info("Keyboard Teleop Initiated")
        pass


    def on_press(self, key):
        try:
            if(key.char == 'c'):
                self.calibrate()

            elif(key.char == 'h'):
                self.home()


            elif(key.char == 'q'):
                rclpy.shutdown()

        except AttributeError:
            pass
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
