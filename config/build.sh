echo "Building Robot Description..."

# build variable environment
cd URDF
python3 build_urdf_xacro.py

# move description files to ROS package
mv robot_variables.xacro
mv robot.urdf.xacro

# return
cd ..

echo "Built Robot Description"