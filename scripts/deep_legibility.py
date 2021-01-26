import sys
import moveit_commander
import numpy as np
import rospy
import json
import os


GOALS = json.load(os.path.abspath(__file__) + "named_keyframes.json")

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

    panda_hand = moveit_commander.MoveGroupCommander("panda_hand")
    panda_hand.go(STARTING_POS_HAND, wait=True)
    panda_hand.stop()
