import sys
import moveit_commander
import numpy as np
import rospy
import json
import os

location = os.path.dirname(os.path.abspath(__file__))
with open(location + "/named_keyframes.json", "r") as json_file:
    GOALS = json.load(json_file)

STARTING_POS_HAND = np.array([
    0.0,
    0.0
])

if __name__ == '__main__':
    moveit_commander.roscpp_initialize([sys.argv[0]])
    # rospy.init_node("move_node", anonymous=True)
    panda_arm = moveit_commander.MoveGroupCommander("panda_arm")

    if sys.argv[1] == "initial":
        poses = np.load(location+"/initial_trajectory.npy").reshape((-1, 7))
    elif sys.argv[1] == "deep":
        poses = np.load(location+"/optimized_trajectory.npy").reshape((-1, 7))
    elif sys.argv[1] == "dragan":
        pass


    for pose in poses:
        panda_arm.go(pose, wait=True)
    panda_arm.stop()
