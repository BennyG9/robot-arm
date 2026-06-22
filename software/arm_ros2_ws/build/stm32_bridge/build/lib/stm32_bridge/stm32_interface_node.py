import rclpy
from rclpy.node import Node

from .protocol import Protocol

class STM32Bridge(Node):

    def __init__(self):
        super().__init__('stm32_bridge')

        #Serial communication
        self.protocol = Protocol()

        #Communication loop
        self.timer = self.create_timer(0.02, self.read_serial)

        self.get_logger().info("STM32 Bridge Initiated")

        self.protocol.write_packet("ERROR_MSG", 1)

        pass

    def read_serial(self):

        # check for packet
        packet = self.protocol.read_packet()

        if(packet == None):
            return
        if(packet == -1):
            print("CHECKSUM ERROR")
            return

        # parse packet
        command, args = self.protocol.parse_packet(packet)

        # executables
        if(self.protocol.get_direction(command) == "JETSON_TO_STM32"):
            print("DIRECTIONALITY ERRROR")

        if(command == "JOINT_STATE"):
            print(args)

        elif(command == "ERROR_MSG"):
            print("REPORTED ERROR")


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
