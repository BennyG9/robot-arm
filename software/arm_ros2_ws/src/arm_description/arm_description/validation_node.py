import rclpy
from rclpy.node import Node

from arm_interfaces.srv import ValidateAngles
from arm_interfaces.srv import RobotParameters
from arm_description.validation import validate_angles

class ValidationNode(Node):

    def __init__(self):
        super().__init__('validation_node')

        # validate angles service
        self.validate_angles_srv = self.create_service(
            ValidateAngles,
            "validate_angles",
            self.validate_angles_callback
        )

        # grab robot config data
        self.parameters_client = self.create_client(RobotParameters, "robot_parameters")
        while(not self.parameters_client.wait_for_service(timeout_sec=1.0)):
            self.get_logger().info("Waiting for robot parameters service...")
        self.parameters = {}
        request = RobotParameters.request()
        self.future = self.parameters_client.call_async(request)
        parameter_data = self.result
        if(parameter_data is None):
            self.get_logger().error("Failed to retreive robot parameters")
        for i in range(len(parameter_data.names)):
            self.parameters[parameter_data.names[i]] = float(parameter_data.parameters[i])

        self.get_logger().info("Validation Initiated")
        pass


    def validate_angles_callback(self, request, response):
        valid = validate_angles(request.angles, self.parameters)
        response.valid = valid
        return response
pass



def main():
    rclpy.init()
    node = ValidationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
