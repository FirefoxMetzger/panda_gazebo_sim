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

### Launch a Gazebo server and moveit
This will start Gazebo in server mode (verbose) loading an empty.world and spawning 
panda in it. It will also start moveit and the respective controller.
```
docker run -it panda_gazebo_sim roslaunch panda_gazebo panda_moveit.launch
```

### Launch Gazebo only (default)
This will start Gazebo in server mode(verbose) loading an empty.world and spawning 
panda in it.
```
docker run -it panda_gazebo_sim
```

## Your own Gazebo world
To rock your own gazebo world mount your custom worlds and models directories 
in the locations where they are stored in the image:
```
docker run \
    --volume="<absolute/path/to/your/panda.world>:/catkin_ws/src/panda_gazebo/worlds/" \
    --volume="<absolute/path/to/your/models/folder/>:/catkin_ws/src/panda_gazebo/models" \
    panda_gazebo_sim
```
Keep in mind that the world file has to be called `panda.world`.

## Issues and Suggestions
The issue page is open for any issues or feature suggestions. If you like this repo, 
consider giving it a star. Positive feedback lets me know that there is interest in this 
topic, and I will do more work like this.
