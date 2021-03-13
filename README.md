# Franka Emika Panda Simulator

**⚠️ This simulator has been archived in favor of Ignition Gazebo ⚠️**

Gazebo has reached its end-of-life and has been superseeded by
[Ignition](https://ignitionrobotics.org/home). Consequentially, I migrated this
simulator to Ignition and the new source code to run simulations can be found
in a new repository: https://github.com/FirefoxMetzger/panda-ignition-sim

The purpose of this repo is to provide an easy-access simulator for the Franka
Emika Panda robot. It does so using Gazebo, ROS1, and Docker. This allows to
quickly start and stop a simulator without having to struggle too much setting
up dependencies. It also allows to run multiple simulators in parallel (with or
without GUI) to explore learning based approaches to robot control.

**Features**

- Easy setup to control the robot in python (rospy)
- ~Process isolation to allow multiple simulators on a single node (no GUI)~
- Freely configurable (and scriptable) world
- Easy migration and sharing
- Runs on Windows, Mac OS, and Linux

Know of any features that could be added? Found a bug? Please open an issue in this repo.
Additionally, if you like this repo, consider giving it a star. Positive feedback lets 
me know that there is interest in this topic, and I will do more work like this.

## Installation
You should have Docker, Docker-compose, and git installed on your system before
installing this Simulator. Each project is heavily in use and there are tons of
good tutorials online.

First install and build the images:
```
git clone https://github.com/FirefoxMetzger/panda_gazebo_sim.git 
docker-compose build
```

ROS is a fairly large image, and we are compiling some code during the build.
The first build may take a bit longer while caches are being populated.

If you wish to use the Gazebo GUI to show the world and the robot moving around
in it, you will have to share your display with the docker container running
Gazebo.

### On Linux
The ROS Docker documentation has a section on [how to set this
up](http://wiki.ros.org/docker/Tutorials/GUI#The_simple_way). You will have to
decide for the level of security; if you are just briefly playing around with
it, the first option may suffice. If you are planning something more
sophisticated, you may wish to use the options listed further down.

### On Windows
On Windows it depends a bit on how you run Docker for Windows. On a resonably
modern system you will have access to WSL, and I highly recommend you use this
as a backend to run docker containers. 

To forward the GUI from docker's linux host to Windows, you will have to (for
now) perform X11 forwarding using a 3d party program. Several good options exist
and in the near future this step will become obsolete as WSL annonoced that it
will add GUI support. You can get an overview of your options
[here](https://techcommunity.microsoft.com/t5/windows-dev-appconsult/running-wsl-gui-apps-on-windows-10/ba-p/1493242),
though I think that the best option currently is to use vcXsrv.

### Web Client
A feature that I am working on currently is to add
[GzWeb](http://gazebosim.org/gzweb.html) to the stack. This will make using a
GUI much simpler, because it will run directly in your browser of choice.

## Workflows
### Scripting

```
docker-compose run rospy
```

This will start the simulator in the background and drop you into a shell within
the ROS ecosystem. The ``scripts`` folder of this repo will be mounted into the
shell's container and you can run the python scripts inside to control the
robot. Take a look at the examples and feel free to add scripts based on your
needs.

### RViZ (requires GUI)

```
docker-compose run rviz
```

This will start the simulator in the background and launch RViZ. You can 
then control the simulated robot by planning movements in RViZ.


### Clean-Up
```
docker-compose down
```

This will clean up any residuals and temorary files created by the simulator,
such as dangling containers, volumes, virtual networks, etc.

## Configuration

There are several useful configuration options for the simulator. These are set
by either (a) temorarily overwriting the default values set in the
docker-compose file (see below), or (b) permanently adjusting the
docker-compose.


### Turning off the GUI
TODO: Write documentation

### Multiple Simulators (process-level parallelization)
TODO: Write documentation

### Changing Worlds/Environments
TODO: Write documentation

### Your own Gazebo world
TODO: Update Documentation

To rock your own gazebo world mount your custom worlds and models directories 
in the locations where they are stored in the image:
```
docker run \
    --volume="<absolute/path/to/your/panda.world>:/catkin_ws/src/panda_gazebo/worlds/" \
    --volume="<absolute/path/to/your/models/folder/>:/catkin_ws/src/panda_gazebo/models" \
    panda_gazebo_sim
```
Keep in mind that the world file has to be called `panda.world`.


## Other repos you may find useful

[Official Franka Emika ROS Package](https://github.com/frankaemika/franka_ros)
[A more sophisticated Panda Simulator](https://github.com/justagist/panda_simulator)
[Another Panda Simulator](https://github.com/erdalpekel/panda_simulation)
