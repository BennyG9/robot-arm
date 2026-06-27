import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

from .protocol import Protocol

import time
import math

class STM32Bridge(Node):

    def __init__(self):
        super().__init__('stm32_bridge')

        #Serial communication
        self.protocol = Protocol()

        #Joint State publisher
        self.joint_pub = self.create_publisher(JointState, "joint_states", 10)

        #Communication loop
        self.timer = self.create_timer(0.1, self.read_serial)

        self.get_logger().info("STM32 Bridge Initiated")
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
            pass

        if(command == "JOINT_STATE"):
            self.publish_joint_states(args[0])
            pass

        elif(command == "ERROR_MSG"):
            pass

        pass

    def publish_joint_states(self, joint_angles):
        msg = JointState()

        msg.name = [
            "base_joint",
            "shoulder_joint",
        ]

        msg.position = [
            math.radians(joint_angles[0]),
            math.radians(joint_angles[1]),
        ]

        msg.velocity = []
        msg.effort = []

        self.joint_pub.publish(msg)
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
