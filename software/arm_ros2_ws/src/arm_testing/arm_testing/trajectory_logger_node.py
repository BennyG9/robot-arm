import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_prefix

from arm_interfaces.msg import JointStates 
from arm_interfaces.srv import RobotParameters 
from arm_interfaces.srv import StartLogger

from kinematics.forward_kinematics import forward_kinematics 

import time
import numpy as np
from pathlib import Path 
import csv
import json

# /service call gives trajectory data, sets logging flag/
# /waits for trajectory to start, keep certain number of starting angles logged/ 
# /logs trajectory while unstable/ 
# /stop logging when stable & @ end of trajectory/ 
# /save data to some file/ 

class TrajectoryLoggerNode(Node):

    stability_time_constant = 3.
    max_backlog = 15

    def __init__(self):
        super().__init__('trajectory_logger_node')

        #Directory Path for Trajectory Data
        WORKSPACE_ROOT = self.get_workspace_root()
        self.DATA_DIR = WORKSPACE_ROOT / 'data' / 'trajectory_tests'
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)

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

        #Logger Service
        self.logger_srv = self.create_service(
            StartLogger,
            "start_logger",
            self.start_logger_callback
        )
        self.logging_flag = False
        self.current_log = []
        self.planned_trajectory = None
        self.start_time = None

        #Joint State Subscriber 
        self.joint_sub = self.create_subscription(JointStates, "joint_states", self.joint_states_callback, 10)
        self.current_angles[0., 0., 0.]
        self.last_zero_update = None 

        #Main Loop
        self.timer = self.create_timer(0.001, self.timer_callback)
        self.stable = True

        self.get_logger().info("Trajectory Logger Initiated")
        pass


    def joint_states_callback(self, msg):
        #save angles 
        new_angles = [msg.base, msg.shoulder, msg.elbow]
        time_stamp = time.monotonic()

        #angle gradient 
        DQ = new_angles - self.current_angles

        #set last_zero_update flag to current time if angles NOT changing
        if(not any(DQ)):                                                          #might need to allow for floating point errors, tiny fluctuations?

            #only update if they were changing on last update
            if(self.last_zero_update == None):
                self.last_zero_update = time.monotonic()

        #set last_zero_update flag to None if published angles ARE changing 
        else:
            self.last_zero_update = None
            pass

        #save angles 
        self.current_angles = new_angles

        #update log 
        if(self.logging_flag):
            data = self.current_angles + [time_stamp - self.start_time]
            if(len(self.current_log) < self.max_backlog or not self.stable):
                self.current_log.append(data)
            else:
                for i in range(len(self.current_log)-1):
                    self.current_log[i] = self.current_log[i+1]
                self.current_log[len(self.current_log)-1] = data 
        pass


    def timer_callback(self):
        previous_stability = self.stable

        #set stability flag
        if(self.last_zero_update == None):
            self.stable = False 
        elif(time.monotonic() - self.last_zero_update > self.stability_time_constant):
            self.stable = True 

        #update logging flag on falling edge of stable signal, end of trajectory 
        if(self.stable and (not previous_stability) and self.logging_flag):
            self.logging_flag = False

            #actually log data at end of trajectory 
            self.log_trajectory()

            #clean up 
            self.current_log = []
            self.planned_trajectory = None
            self.start_time = None
        pass


    #service callback to initiate logger
    def start_logger_callback(self, request, response):
        #reject if already logging 
        if(self.logging_flag):
            response.success = False
        else:
            response.success = True

        #init log
        self.current_log = []
        self.logging_flag = True
        self.start_time = time.monotonic()

        #save planned trajectory 
        if(request.trajectory.length != 0):
            self.planned_trajectory = type("Trajectory", (), {
                "length": request.trajectory.length,
                "time_parameterizatiion_function": request.trajectory.time_parameterization_function,
                "angles": np.rad2deg(np.reshape(request.trajectory.angles, (3, request.trajectory.length)))
            })
        else:
            self.planned_trajectory = None
        return response 


    #saves data
    def log_trajectory(self):
        #get and update testing metadata
        metadata = None
        metadata_filepath = self.DATA_DIR / "metadata.json"
        with open(metadata_filepath, "r+", encoding="utf-8") as metadata_file:
            metadata = json.load(metadata_file)

            #increment log counter
            metadata["logged_tests"] = metadata["logged_tests"] + 1

            #save back to json file
            metadata_file.seek(0)
            json.dump(metadata, metadata_file, indent=4)
            metadata_file.truncate()

        #test directory path
        TEST_DIRECTORY = self.DATA_DIR / ("trajectory" + str(metadata["logged_tests"]))

        #save trajectory data
        planned_filepath = TEST_DIRECTORY / "planned.csv"
        with open(planned_filepath, "w", newline="") as planned_csv:
            writer = csv.writer(planned_csv)
            writer.writerow([
                "base_deg",
                "shoulder_deg",
                "elbow_deg",
                "dt"
            ])
            trajectory_data = np.column_stack((self.planned_trajectory.angles, self.planned_trajectory.time_parameterization_function.append(0.)))
            writer.writerows(trajectory_data)

        #save logged robot joint angles 
        executed_filepath = TEST_DIRECTORY / "executed.csv"
        with open(executed_filepath, "w", newline="") as executed_csv:
            writer = csv.writer(executed_csv)
            writer.writerow([
                "base_deg",
                "shoulder_deg",
                "elbow_deg",
                "time_stamp"
            ])
            writer.writerows(self.current_log)
        pass



    def get_end_coordinates(self, angles):
        frames = np.reshape(forward_kinematics(np.array(angles), self.parameters), (6,4,4))
        return (frames[5][:3,3].astype(float)).tolist()

    def get_workspace_root(self):
        package_prefix = path(get_package_prefix('arm_testing'))
        for path in package_prefix.parents:
            if (path / 'src').is_dir() and (path / 'install').is_dir():
                return path
        raise RuntimeError("Could not locate ROS workspace root dir")

    pass




def main():
    rclpy.init()
    node = TrajectoryLoggerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()







