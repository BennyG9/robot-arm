import rclpy
from rclpy.node import Node

class STM32Bridge(Node):

    def __init__(self):

        #Serial communication
        self.serial = SerialCom(port="/dev/ttyACM0")

        #Communication loop
        self.timer = self.create_timer(0.02, self.read_serial)

        self.get_logger().info("STM32 Bridge Initiated")
        pass

    def read_serial(self):
        line = self.serial.read_line()

        if(line == None):
            return

        

        pass

    pass


def main():
    rclpy.init()
    node = STM32Bridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
