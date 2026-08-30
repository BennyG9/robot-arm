echo "Building All..."

# build communications
cd communication
./build.sh
cd ..

# build robot description
cd config
./build.sh
cd ..

# source ROS2 foxy
source /opt/ros/foxy/setup.bash

# build ROS2 workspace
cd software/arm_ros2_ws
colcon build
cd ../..

echo "Built All"
