# build the catkin workspace
FROM osrf/ros:kinetic-desktop-full-xenial AS workspace-builder
COPY assets/panda_xacro/ /xacro 
COPY assets/catkin_ws/ /catkin_ws
RUN bash -c 'source /opt/ros/kinetic/setup.bash \
    && rosrun xacro xacro --inorder /xacro/panda_arm_hand.urdf.xacro > /catkin_ws/src/panda_description/urdf/panda.urdf' \
    && apt update \
    && apt install -y python-catkin-tools \
    && cd /catkin_ws \
    && catkin build \
    && rm -rf /var/lib/apt/lists/*

FROM osrf/ros:kinetic-desktop-full-xenial
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