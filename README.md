# Franka Emika Panda Simulator

This is a Gazebo based docker image that has a model of the Franka Emika Panda robot 
pre-installed. The original .xacro files were taken from the official Framka Emika
[ros package repo](https://github.com/frankaemika/franka_ros) and are also published
under Apache 2.0.

## Installation

Building the image locally is straight forward
```
git clone https://github.com/FirefoxMetzger/panda_gazebo_sim.git 
cd panda_gazebo_sim
./build.sh
```

from here, you can run one of the different launch files the image provides.

### Launch Gazebo GUI and RViZ
If you want to use the GUI for either RViZ or Gazebo within the container, you will have 
to share your host's X server. There is a few ways of doing this, and the 
[ROS Wiki](http://wiki.ros.org/docker/Tutorials/GUI) has some insights on this as well. 

The simplest way to 'just mess with the image' is via:

```
xhost +local:root
docker run -it \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    panda_gazebo_sim roslaunch panda_gazebo panda_rviz.launch
xhost -local:root
```

### Launch gazebo and moveit

## Getting just the model
If you want to only get the (.sdf) models of the robot, you can build the docker image by
running the `build.sh`. It will create a tmp direcory in the project and within it there
are two folders. `panda_arm_hand` is the model with gripper attached, and `panda_arm` is 
the model without any endeffector.

## Issues
If you have any problems setting this up, please feel free to open an issue.

### Running your own environment
Running your own environment to simulate panda in is easy thanks to Docker's ability to 
mount volumes. Simply replace the worlds and models directory with your custom version.
```

```

The world file is stored located at
```
/catkin_ws/src/panda_gazebo/worlds/panda.world
```
and the models folder lives at
```
/catkin_ws/src/panda_gazebo/models
```