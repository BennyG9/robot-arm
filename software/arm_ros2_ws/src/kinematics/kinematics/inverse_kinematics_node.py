import rclpy
from rclpy.node import Node

class IKNode(Node)

    def __init__(self):
        super().__init__('ik_node')

        self.get_logger().info("Inverse Kinematics Initiated")
        pass

pass



def main():
    rclpy.init()
    node = IKNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()