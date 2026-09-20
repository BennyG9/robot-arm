echo "Building Robot Description..."

# build variable environment
cd URDF
python3 build_urdf_xacro.py

# move description files to ROS package
cp robot_variables.xacro ../software/arm_ros2_ws/src/arm_description/urdf/robot_variables.xacro
cp robot.urdf.xacro ../software/arm_ros2_ws/src/arm_description/urdf/robot.urdf.xacro

# return
cd ..

echo "Built Robot Description"
