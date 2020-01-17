FROM osrf/ros:kinetic-desktop-full-xenial

RUN apt-get update \
    && apt-get install -y \
        ros-kinetic-gazebo-ros \
        ros-kinetic-gazebo-ros-pkgs \
        ros-kinetic-gazebo-ros-control \
        ros-kinetic-joint-state-controller \
        ros-kinetic-effort-controllers \
        ros-kinetic-position-controllers \
        ros-kinetic-joint-trajectory-controller \ 
        ros-kinetic-ros-control \
        ros-kinetic-moveit\
    && rm -rf /var/lib/apt/lists/*

COPY assets/catkin_ws/src/panda_gazebo/models /root/.gazebo/models
COPY assets/catkin_ws/ /catkin_ws
COPY assets/ros_entrypoint.sh /ros_entrypoint.sh
CMD roslaunch panda_gazebo panda_moveit.launch