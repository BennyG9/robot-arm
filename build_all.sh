echo "Building All..."

# build communications
cd communication
./build.sh
cd ..

# build ROS2 workspace
cd software/arm_ros2_ws
colcon build
cd ../..

echo "Built All"
