import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from arm_interfaces.srv import Calibrate
from arm_interfaces.srv import Home

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

        #Services
        self.calibrate_srv = self.create_service(
            Calibrate,
            "calibrate",
            self.calibrate_callback
        )

        self.home_srv = self.create_service(
            Home,
            "home",
            self.home_callback
        )

        #Communication loop
        self.timer = self.create_timer(0.0001, self.read_serial)

        #Clear serial
        self.protocol.clear_serial()

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
            self.get_logger().info("ERROR CODE: " + str(args[0][0]))
            #print("ERROR CODE: " + str(args[[0]]))
            pass

        pass


    def calibrate_callback(self, request, response):
        self.get_logger().info("Calibrate Command Sent")
        self.protocol.write_packet("CALIBRATE")
        response.success = True
        return response


    def home_callback(self, request, response):
        self.get_logger().info("Home Command Sent")
        self.protocol.write_packet("HOME")
        response.success = True
        return response


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
