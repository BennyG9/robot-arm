import json
import os

import math

# open JSON file
path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "robot.json")
with open(path, "r") as file:
    robot = json.load(file)

# create new .urdf.xacro file
path = os.path.join(os.path.dirname(__file__), "robot_variables.xacro")
with open(path, "w") as xacro:
    # headers
    xacro.write("<?xml version=\"1.0\"?>\n")
    xacro.write("<robot xmlns:xacro=\"http://www.ros.org/wiki/xacro\" name=\"robot_arm\">\n\n")

    # link variables 
    robot_links = list(robot["links"].items())
    for link_name, link_length in robot_links:
        # write link data
        xacro.write("\t<xacro:property name=\"" + link_name + "\" value=\"" + str(link_length) + "\"/>\n")
        pass
    xacro.write("\n")

    # joint variables
    for joint, joint_data in robot["joints"].items():
        joint_name = joint + "_joint"

        # write joint data
        xacro.write("\t<xacro:property name=\"" + joint_name + "_min\" value=\"" + str(math.radians(joint_data["min_angle"])) + "\"/>\n")
        xacro.write("\t<xacro:property name=\"" + joint_name + "_max\" value=\"" + str(math.radians(joint_data["max_angle"])) + "\"/>\n")
        xacro.write("\t<xacro:property name=\"" + joint_name + "_offset\" value=\"" + str(joint_data["l"]) + "\"/>\n\n")
        pass

    # end
    xacro.write("</robot>")
    pass