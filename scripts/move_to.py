import sys
import moveit_commander
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
    0.0,
    0.0
])

if __name__ == '__main__':
    pos = np.fromstring(sys.argv[1], sep=', ')
    print(pos)
    if pos.size != 7:
        print("Pose doesn't specify all 7 DoFs")
        exit(1)
    moveit_commander.roscpp_initialize([sys.argv[0]])
    panda_arm = moveit_commander.MoveGroupCommander("panda_arm")
    panda_arm.go(pos, wait=True)
    panda_arm.stop()

    # panda_hand = moveit_commander.MoveGroupCommander("panda_hand")
    # panda_hand.go(STARTING_POS_HAND, wait=True)
    # panda_hand.stop()
