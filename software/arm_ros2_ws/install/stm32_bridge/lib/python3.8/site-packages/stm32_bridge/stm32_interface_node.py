import rclpy
from rclpy.node import Node

from .protocol import Protocol

class STM32Bridge(Node):

    def __init__(self):

        #Serial communication
        self.protocol = Protocol()

        #Communication loop
        self.timer = self.create_timer(0.02, self.read_serial)

        self.get_logger().info("STM32 Bridge Initiated")
        pass

    def read_serial(self):

        packet = self.protocol.read_packet()

        if(packet == None):
            return
        if(packet == -1):
            print("CHECKSUM ERROR")
            return

        command, args = self.protocol.parse_packet(packet)

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
