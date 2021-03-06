# --- Builder for Gazebo packages ---
FROM osrf/ros:kinetic-desktop-full AS workspace-builder
COPY assets/panda_xacro/ /xacro 
COPY assets/catkin_ws/ /catkin_ws
RUN bash -c 'source /opt/ros/kinetic/setup.bash \
    && rosrun xacro xacro --inorder /xacro/panda_arm_hand.urdf.xacro > /catkin_ws/src/panda_description/urdf/panda.urdf' \
    && apt-get update \
    && apt-get install -y python-catkin-tools \
    && cd /catkin_ws \
    && bash -c 'source /opt/ros/kinetic/setup.bash && catkin build' \
    && rm -rf /var/lib/apt/lists/*


# --- Panda Gazebo Simulator ---
FROM osrf/ros:kinetic-desktop-full AS panda_gazebo
ENV WORLD_FILE=panda.world \
    USE_GUI=true
# install the missing dependencies and update gazebo to 7.16
RUN sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list' \
    && curl http://packages.osrfoundation.org/gazebo.key | apt-key add - \
    && apt-get update \
    && apt-get upgrade -y gazebo7 libgazebo7-dev \
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
COPY --from=workspace-builder /catkin_ws /catkin_ws
COPY assets/ros_entrypoint.sh /ros_entrypoint.sh
CMD roslaunch panda_gazebo panda.launch

# --- simulator + python ---
FROM panda_gazebo AS rospy3
RUN apt-get update \
    && apt-get install -y \
        python3-catkin-pkg-modules \
        python3-rospkg-modules \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /ros_scripts
CMD ["/bin/bash"]