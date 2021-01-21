import sys
import moveit_commander
import geometry_msgs.msg
from moveit_commander.conversions import pose_to_list

import numpy as np


STARTING_POS = np.array([
    1.5144076375347826,
    -0.6726638697722728,
    0.18543326279796127,
    -2.9585892121572526,
    0.12056011035042515,
    2.3006689352724274,
    0.7933720851335472
])

STARTING_POS_HAND = np.array([
    0.1,
    0.1
])


def all_close(goal, actual, tolerance):
    """
    Convenience method for testing if a list of values are within a tolerance of
    their counterparts in another list
    @param: goal       A list of floats, a Pose or a PoseStamped
    @param: actual     A list of floats, a Pose or a PoseStamped
    @param: tolerance  A float @returns: bool
    """
    all_equal = True
    if type(goal) is list:
        for index in range(len(goal)):
            if abs(actual[index] - goal[index]) > tolerance:
                return False

    elif type(goal) is geometry_msgs.msg.PoseStamped:
        return all_close(goal.pose, actual.pose, tolerance)

    elif type(goal) is geometry_msgs.msg.Pose:
        return all_close(pose_to_list(goal), pose_to_list(actual), tolerance)

    return True


if __name__ == '__main__':
    moveit_commander.roscpp_initialize(sys.argv)
    panda_arm = moveit_commander.MoveGroupCommander("panda_arm")
    panda_arm.go(STARTING_POS, wait=True)
    panda_arm.stop()

    panda_hand = moveit_commander.MoveGroupCommander("panda_hand")
    panda_hand.go(STARTING_POS_HAND, wait=True)
    panda_hand.stop()