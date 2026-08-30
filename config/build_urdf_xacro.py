import json
import os

# open JSON file
path = os.path.join(os.path.dirname(__file__), "robot.json")
with open(path, "r") as file:
    robot = json.load(file)

# create new .urdf.xacro file
path = os.path.join(os.path.dirname(__file__), "robot.urdf.xacro")
with open(path, "w") as xacro:
    # headers
    xacro.write("<?xml version=\"1.0\"?>\n")
    xacro.write("<robot xmlns:xacro=\"http://www.ros.org/wiki/xacro\" name=\"robot_arm\">\n\n")

    # end
    xacro.write("</robot>")
    pass