echo "Building Robot Description..."

# build variable environment
cd URDF
python3 build_urdf_xacro.py

#if [ -e "../../software/" ]; then
#    echo "path exists"
#else
#    echo "path does not exist"
#fi

# move description files to ROS package
cp -u robot_variables.xacro ../../software/arm_ros2_ws/src/arm_description/urdf/robot_variables.xacro
cp -u robot.urdf.xacro ../../software/arm_ros2_ws/src/arm_description/urdf/robot.urdf.xacro

# return
cd ..

echo "Built Robot Description"
