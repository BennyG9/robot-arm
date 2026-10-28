import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from arm_interfaces.srv import RobotParameters 
from arm_interfaces.srv import Calibrate 
from arm_interfaces.srv import Home
from arm_interfaces.srv import GetTrajectory

from arm_interfaces.msg import JointStates 

from arm_interfaces.action import FollowTrajectory 


# TODO:
#       initial calibrate and home
#       random start? 
#       loop state machine
#       is stable signal
#       randomized trajectory request 
#       joint state logger
#       /actively executing flag/ 



class LinearTrajectoryTest(Node):

    def __init__(self):
        super.__init__("linear_trajectory_test_node")

        #Get Robot Parameters 
        self.parameters_client = self.create_client(RobotParameters, "robot_parameters")
        while(not self.parameters_client.wait_for_service(timeout_sec=1.0)):
            self.get_logger().info("Waiting for robot parameters service...")
        self.parameters = {}
        request = RobotParameters.Request()
        future = self.parameters_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        parameter_data = future.result()
        if(parameter_data is None):
            self.get_logger().error("Failed to retreive robot parameters")
        for i in range(len(parameter_data.names)):
            self.parameters[parameter_data.names[i]] = float(parameter_data.parameters[i])

        #Calibration
        self.calibrate_client = self.create_client(Calibrate, "calibrate")

        #Homing
        self.home_clinet = self.create_client(Home, "home")

        #Trajectory Generation + Execution
        self.traj_client = self.create_client(GetTrajectory, "get_trajectory")
        self._trajectory_client = ActionClient(
            self,
            FollowTrajectory,
            'follow_trajectory'
        )
        self.trajectory_active = False

        #Joint state subscriber 
        self.joint_sub = self.create_subscription(JointStates, "joint_states", self.joint_states_callback, 10)

        self.get_logger().info("Linear Trajectory Test Starting...")

        self.startup()
        pass


    #initialize variables and setup robot
    def startup(self):

        # calibrate
        cal_request = Calibrate.Request()
        self.calibrate_client.call_async(cal_request)

        # home
        home_request = Home.Request()
        self.home_clinet.call_async(home_request)

        pass

    def joint_states_callback(self, msg):
        pass


pass



def main():
    rclpy.init()
    node = LinearTrajectoryTest()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()