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
    if len(sys.argv) != 2:
        print("Specify the pose to move to.")
        print("Valid Values: " + str(GOALS.keys()))
        exit(1)

    pos = sys.argv[1]
    if pos not in GOALS:
        print("Specify the pose to move to.")
        print("Valid Values: " + str(GOALS.keys()))
        exit(1)

    pos = GOALS[pos]
    moveit_commander.roscpp_initialize([sys.argv[0]])
    rospy.init_node("move_node", anonymous=True)
    panda_arm = moveit_commander.MoveGroupCommander("panda_arm")
    panda_arm.go(pos, wait=True)
    panda_arm.stop()

    pose = panda_arm.get_current_pose().pose
    print("Current Pose: ", pose.position.x, pose.position.y, pose.position.z)
