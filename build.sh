#!/bin/bash

# generate the .urdf
docker run --rm -v ${PWD}/assets/panda_xacro:/xacro osrf/ros:kinetic-desktop-full rosrun xacro xacro --inorder /xacro/panda_arm_hand.urdf.xacro > ${PWD}/assets/catkin_ws/src/panda_description/urdf/panda.urdf

# build the ROS packages
docker run --rm -it -v /home/isir/panda_sim_ros/assets/catkin_ws:/catkin_ws osrf/ros:kinetic-desktop-full-xenial bash -c "apt update && apt install -y python-catkin-tools && cd /catkin_ws && catkin build"

# Build the image
docker build -t panda_gazebo_sim:latest ${PWD}
