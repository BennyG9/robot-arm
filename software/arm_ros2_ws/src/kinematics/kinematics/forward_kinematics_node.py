import rclpy
from rclpy.node import Node

class FKNode(Node)

    def __init__(self):
        super().__init__('fk_node')

        self.get_logger().info("Forward Kinematics Initiated")
        pass

pass



def main():
    rclpy.init()
    node = FKNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()